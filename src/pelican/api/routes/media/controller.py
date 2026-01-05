from collections.abc import AsyncGenerator, Mapping
from typing import Annotated

from litestar import Controller as BaseController
from litestar import Request, handlers
from litestar.channels import ChannelsPlugin
from litestar.datastructures import ResponseHeader
from litestar.di import Provide
from litestar.exceptions import InternalServerException
from litestar.openapi import ResponseSpec
from litestar.params import Body, Parameter
from litestar.response import Response, Stream
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT

from pelican.api.exceptions import BadRequestException, NotFoundException
from pelican.api.routes.media import errors as e
from pelican.api.routes.media import models as m
from pelican.api.routes.media.service import Service
from pelican.api.validator import Validator
from pelican.services.media.service import MediaService
from pelican.state import State
from pelican.utils.time import httpstringify


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(
        self,
        state: State,
        channels: ChannelsPlugin,
    ) -> Service:
        return Service(
            media=MediaService(
                graphite=state.graphite,
                minium=state.minium,
                channels=channels,
            )
        )

    def build(self) -> Mapping[str, Provide]:
        """Build the dependencies."""
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the media endpoint."""

    dependencies = DependenciesBuilder().build()

    @handlers.get(
        summary="List media",
    )
    async def list(  # noqa: PLR0913
        self,
        service: Service,
        limit: Annotated[
            m.ListRequestLimit,
            Parameter(
                description="Maximum number of media to return.",
            ),
        ] = 10,
        offset: Annotated[
            m.ListRequestOffset,
            Parameter(
                description="Number of media to skip.",
            ),
        ] = None,
        where: Annotated[
            str | None,
            Parameter(
                description="Filter to apply to find media.",
            ),
        ] = None,
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
        order: Annotated[
            str | None,
            Parameter(
                description="Order to apply to the results.",
            ),
        ] = None,
    ) -> Response[m.ListResponseResults]:
        """List media that match the request."""
        parsed_where = (
            Validator[m.ListRequestWhere].validate_json(where) if where else None
        )
        parsed_include = (
            Validator[m.ListRequestInclude].validate_json(include) if include else None
        )
        parsed_order = (
            Validator[m.ListRequestOrder].validate_json(order) if order else None
        )

        req = m.ListRequest(
            limit=limit,
            offset=offset,
            where=parsed_where,
            include=parsed_include,
            order=parsed_order,
        )

        try:
            res = await service.list(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        results = res.results

        return Response(results)

    @handlers.get(
        "/{id:uuid}",
        summary="Get media",
    )
    async def get(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.GetRequestId,
            Parameter(
                description="Identifier of the media to get.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.GetResponseMedia]:
        """Get media by ID."""
        parsed_include = (
            Validator[m.GetRequestInclude].validate_json(include) if include else None
        )

        req = m.GetRequest(
            id=id,
            include=parsed_include,
        )

        try:
            res = await service.get(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex

        media = res.media

        return Response(media)

    @handlers.post(
        summary="Create media",
    )
    async def create(
        self,
        service: Service,
        data: Annotated[
            m.CreateRequestData,
            Body(
                description="Data to create media.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.CreateResponseMedia]:
        """Create new media."""
        parsed_data = Validator[m.CreateRequestData].validate_object(data)
        parsed_include = (
            Validator[m.CreateRequestInclude].validate_json(include)
            if include
            else None
        )

        req = m.CreateRequest(
            data=parsed_data,
            include=parsed_include,
        )

        try:
            res = await service.create(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        media = res.media

        return Response(media)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update media",
    )
    async def update(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.UpdateRequestId,
            Parameter(
                description="Identifier of the media to update.",
            ),
        ],
        data: Annotated[
            m.UpdateRequestData,
            Body(
                description="Data to update media.",
            ),
        ],
        include: Annotated[
            str | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[m.UpdateResponseMedia]:
        """Update media by ID."""
        parsed_data = Validator[m.UpdateRequestData].validate_object(data)
        parsed_include = (
            Validator[m.UpdateRequestInclude].validate_json(include)
            if include
            else None
        )

        req = m.UpdateRequest(
            data=parsed_data,
            id=id,
            include=parsed_include,
        )

        try:
            res = await service.update(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex

        media = res.media

        return Response(media)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete media",
        responses={
            HTTP_204_NO_CONTENT: ResponseSpec(
                None, description="Request fulfilled, nothing follows"
            )
        },
    )
    async def delete(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.DeleteRequestId,
            Parameter(
                description="Identifier of the media to delete.",
            ),
        ],
    ) -> Response[None]:
        """Delete media by ID."""
        req = m.DeleteRequest(
            id=id,
        )

        try:
            await service.delete(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex

        return Response(None)

    @handlers.put(
        "/{id:uuid}/content",
        summary="Upload media content",
        status_code=HTTP_204_NO_CONTENT,
        responses={
            HTTP_204_NO_CONTENT: ResponseSpec(
                None, description="Request fulfilled, nothing follows"
            )
        },
    )
    async def upload(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.UploadRequestId,
            Parameter(
                description="Identifier of the media to upload content for.",
            ),
        ],
        type: Annotated[  # noqa: A002
            m.UploadRequestType,
            Parameter(
                header="Content-Type",
                description="Content type.",
            ),
        ],
        request: Request,
    ) -> Response[None]:
        """Upload media content by ID."""

        async def _stream(request: Request) -> AsyncGenerator[bytes]:
            stream = request.stream()
            while True:
                try:
                    chunk = await anext(stream)
                except (StopAsyncIteration, InternalServerException):
                    break

                yield chunk

        req = m.UploadRequest(
            id=id,
            type=type,
            data=_stream(request),
        )

        try:
            await service.upload(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException from ex
        return Response(None)

    @handlers.get(
        "/{id:uuid}/content",
        summary="Download media content",
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                description="Content type.",
                documentation_only=True,
            ),
            ResponseHeader(
                name="Content-Length",
                description="Content length.",
                documentation_only=True,
            ),
            ResponseHeader(
                name="ETag",
                description="Entity tag.",
                documentation_only=True,
            ),
            ResponseHeader(
                name="Last-Modified",
                description="Last modified.",
                documentation_only=True,
            ),
        ],
        responses={
            HTTP_200_OK: ResponseSpec(
                Stream,
                description="Request fulfilled, stream follows",
                generate_examples=False,
                media_type="*/*",
            )
        },
    )
    async def download(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.DownloadRequestId,
            Parameter(
                description="Identifier of the media to download content for.",
            ),
        ],
    ) -> Stream:
        """Download media content by ID."""
        req = m.DownloadRequest(
            id=id,
        )

        try:
            res = await service.download(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException from ex

        content_type = res.type
        size = res.size
        tag = res.tag
        modified = res.modified
        data = res.data

        headers = {
            "Content-Type": content_type,
            "Content-Length": str(size),
            "ETag": tag,
            "Last-Modified": httpstringify(modified),
        }
        return Stream(
            data,
            headers=headers,
        )

    @handlers.head(
        "/{id:uuid}/content",
        summary="Get media content headers",
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                description="Content type.",
                documentation_only=True,
            ),
            ResponseHeader(
                name="Content-Length",
                description="Content length.",
                documentation_only=True,
            ),
            ResponseHeader(
                name="ETag",
                description="Entity tag.",
                documentation_only=True,
            ),
            ResponseHeader(
                name="Last-Modified",
                description="Last modified.",
                documentation_only=True,
            ),
        ],
        responses={
            HTTP_200_OK: ResponseSpec(
                None, description="Request fulfilled, nothing follows"
            )
        },
    )
    async def headdownload(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            m.DownloadRequestId,
            Parameter(
                description="Identifier of the media to get content headers for.",
            ),
        ],
    ) -> Response[None]:
        """Get media content headers by ID."""
        req = m.DownloadRequest(
            id=id,
        )

        try:
            res = await service.download(req)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException from ex

        content_type = res.type
        size = res.size
        tag = res.tag
        modified = res.modified

        headers = {
            "Content-Type": content_type,
            "Content-Length": str(size),
            "ETag": tag,
            "Last-Modified": httpstringify(modified),
        }
        return Response(
            None,
            headers=headers,
        )
