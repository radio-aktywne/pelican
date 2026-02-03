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
from pelican.models.base import Jsonable, Serializable
from pelican.services.media.service import MediaService
from pelican.state import State
from pelican.utils.time import httpstringify


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State, channels: ChannelsPlugin) -> Service:
        return Service(
            media=MediaService(
                graphite=state.graphite, minium=state.minium, channels=channels
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
            Jsonable[m.ListRequestLimit] | None,
            Parameter(
                description="Maximum number of media to return. Default is 10.",
            ),
        ] = None,
        offset: Annotated[
            Jsonable[m.ListRequestOffset] | None,
            Parameter(
                description="Number of media to skip.",
            ),
        ] = None,
        where: Annotated[
            Jsonable[m.ListRequestWhere] | None,
            Parameter(
                description="Filter to apply to find media.",
            ),
        ] = None,
        include: Annotated[
            Jsonable[m.ListRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
        order: Annotated[
            Jsonable[m.ListRequestOrder] | None,
            Parameter(
                description="Order to apply to the results.",
            ),
        ] = None,
    ) -> Response[Serializable[m.ListResponseResults]]:
        """List media that match the request."""
        request = m.ListRequest(
            limit=limit.root if limit else 10,
            offset=offset.root if offset else None,
            where=where.root if where else None,
            include=include.root if include else None,
            order=order.root if order else None,
        )

        try:
            response = await service.list(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        return Response(Serializable(response.results))

    @handlers.get(
        "/{id:str}",
        summary="Get media",
    )
    async def get(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.GetRequestId],
            Parameter(
                description="Identifier of the media to get.",
            ),
        ],
        include: Annotated[
            Jsonable[m.GetRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.GetResponseMedia]]:
        """Get media by ID."""
        request = m.GetRequest(id=id.root, include=include.root if include else None)

        try:
            response = await service.get(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.media))

    @handlers.post(
        summary="Create media",
    )
    async def create(
        self,
        service: Service,
        data: Annotated[
            Serializable[m.CreateRequestData],
            Body(
                description="Data to create media.",
            ),
        ],
        include: Annotated[
            Jsonable[m.CreateRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.CreateResponseMedia]]:
        """Create new media."""
        request = m.CreateRequest(
            data=data.root, include=include.root if include else None
        )

        try:
            response = await service.create(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex

        return Response(Serializable(response.media))

    @handlers.patch(
        "/{id:str}",
        summary="Update media",
    )
    async def update(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.UpdateRequestId],
            Parameter(
                description="Identifier of the media to update.",
            ),
        ],
        data: Annotated[
            Serializable[m.UpdateRequestData],
            Body(
                description="Data to update media.",
            ),
        ],
        include: Annotated[
            Jsonable[m.UpdateRequestInclude] | None,
            Parameter(
                description="Relations to include in the response.",
            ),
        ] = None,
    ) -> Response[Serializable[m.UpdateResponseMedia]]:
        """Update media by ID."""
        request = m.UpdateRequest(
            data=data.root, id=id.root, include=include.root if include else None
        )

        try:
            response = await service.update(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.media))

    @handlers.delete(
        "/{id:str}",
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
            Serializable[m.DeleteRequestId],
            Parameter(
                description="Identifier of the media to delete.",
            ),
        ],
    ) -> Response[None]:
        """Delete media by ID."""
        request = m.DeleteRequest(id=id.root)

        try:
            await service.delete(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex

        return Response(None)

    @handlers.put(
        "/{id:str}/content",
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
            Serializable[m.UploadRequestId],
            Parameter(
                description="Identifier of the media to upload content for.",
            ),
        ],
        type: Annotated[  # noqa: A002
            Jsonable[m.UploadRequestType],
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

        req = m.UploadRequest(id=id.root, type=type.root, data=_stream(request))

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
        "/{id:str}/content",
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
            Serializable[m.DownloadRequestId],
            Parameter(
                description="Identifier of the media to download content for.",
            ),
        ],
    ) -> Stream:
        """Download media content by ID."""
        request = m.DownloadRequest(id=id.root)

        try:
            response = await service.download(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException from ex

        return Stream(
            response.data,
            headers={
                "Content-Type": response.type,
                "Content-Length": str(response.size),
                "ETag": response.tag,
                "Last-Modified": httpstringify(response.modified),
            },
        )

    @handlers.head(
        "/{id:str}/content",
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
            Serializable[m.DownloadRequestId],
            Parameter(
                description="Identifier of the media to get content headers for.",
            ),
        ],
    ) -> Response[None]:
        """Get media content headers by ID."""
        request = m.DownloadRequest(id=id.root)

        try:
            response = await service.download(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException from ex

        return Response(
            None,
            headers={
                "Content-Type": response.type,
                "Content-Length": str(response.size),
                "ETag": response.tag,
                "Last-Modified": httpstringify(response.modified),
            },
        )
