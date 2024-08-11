from collections.abc import AsyncGenerator
from typing import Annotated

from litestar import Controller as BaseController
from litestar import Request, handlers
from litestar.channels import ChannelsPlugin
from litestar.datastructures import ResponseHeader
from litestar.di import Provide
from litestar.exceptions import InternalServerException
from litestar.params import Body, Parameter
from litestar.response import Response, Stream
from litestar.status_codes import HTTP_204_NO_CONTENT

from emitunes.api.exceptions import BadRequestException, NotFoundException
from emitunes.api.routes.media import errors as e
from emitunes.api.routes.media import models as m
from emitunes.api.routes.media.service import Service
from emitunes.api.validator import Validator
from emitunes.services.media.service import MediaService
from emitunes.state import State
from emitunes.utils.time import httpstringify


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(
        self,
        state: State,
        channels: ChannelsPlugin,
    ) -> Service:
        return Service(
            media=MediaService(
                datatunes=state.datatunes,
                mediatunes=state.mediatunes,
                channels=channels,
            )
        )

    def build(self) -> dict[str, Provide]:
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the media endpoint."""

    dependencies = DependenciesBuilder().build()

    @handlers.get(
        summary="List media",
    )
    async def list(
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

        where = Validator(m.ListRequestWhere).json(where) if where else None
        include = Validator(m.ListRequestInclude).json(include) if include else None
        order = Validator(m.ListRequestOrder).json(order) if order else None

        req = m.ListRequest(
            limit=limit,
            offset=offset,
            where=where,
            include=include,
            order=order,
        )

        try:
            res = await service.list(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex

        results = res.results

        return Response(results)

    @handlers.get(
        "/{id:uuid}",
        summary="Get media",
    )
    async def get(
        self,
        service: Service,
        id: Annotated[
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

        include = Validator(m.GetRequestInclude).json(include) if include else None

        req = m.GetRequest(
            id=id,
            include=include,
        )

        try:
            res = await service.get(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

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

        data = Validator(m.CreateRequestData).object(data)
        include = Validator(m.CreateRequestInclude).json(include) if include else None

        req = m.CreateRequest(
            data=data,
            include=include,
        )

        try:
            res = await service.create(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex

        media = res.media

        return Response(media)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update media",
    )
    async def update(
        self,
        service: Service,
        id: Annotated[
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

        data = Validator(m.UpdateRequestData).object(data)
        include = Validator(m.UpdateRequestInclude).json(include) if include else None

        req = m.UpdateRequest(
            data=data,
            id=id,
            include=include,
        )

        try:
            res = await service.update(req)
        except e.ValidationError as ex:
            raise BadRequestException(extra=str(ex)) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        media = res.media

        return Response(media)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete media",
    )
    async def delete(
        self,
        service: Service,
        id: Annotated[
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
            raise BadRequestException(extra=str(ex)) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        return Response(None)

    @handlers.put(
        "/{id:uuid}/content",
        summary="Upload media content",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def upload(
        self,
        service: Service,
        id: Annotated[
            m.UploadRequestId,
            Parameter(
                description="Identifier of the media to upload content for.",
            ),
        ],
        type: Annotated[
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
            raise BadRequestException(extra=str(ex)) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

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
    )
    async def download(
        self,
        service: Service,
        id: Annotated[
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
            raise BadRequestException(extra=str(ex)) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        type = res.type
        size = res.size
        tag = res.tag
        modified = res.modified
        data = res.data

        headers = {
            "Content-Type": type,
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
    )
    async def headdownload(
        self,
        service: Service,
        id: Annotated[
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
            raise BadRequestException(extra=str(ex)) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException(extra=str(ex)) from ex

        type = res.type
        size = res.size
        tag = res.tag
        modified = res.modified

        headers = {
            "Content-Type": type,
            "Content-Length": str(size),
            "ETag": tag,
            "Last-Modified": httpstringify(modified),
        }
        return Response(
            None,
            headers=headers,
        )
