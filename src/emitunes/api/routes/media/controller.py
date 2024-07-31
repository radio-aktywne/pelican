from collections.abc import AsyncGenerator
from typing import Annotated

from litestar import Controller as BaseController
from litestar import Request, handlers
from litestar.channels import ChannelsPlugin
from litestar.datastructures import ResponseHeader
from litestar.di import Provide
from litestar.exceptions import InternalServerException
from litestar.params import Parameter
from litestar.response import Response, Stream
from litestar.status_codes import HTTP_204_NO_CONTENT
from pydantic import Json, TypeAdapter
from pydantic import ValidationError as PydanticValidationError

from emitunes.api.exceptions import BadRequestException, NotFoundException
from emitunes.api.routes.media import errors as e
from emitunes.api.routes.media import models as m
from emitunes.api.routes.media.service import Service
from emitunes.media.service import MediaService
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

    def _validate_pydantic[T](self, t: type[T], v: str) -> T:
        try:
            return TypeAdapter(t).validate_python(v)
        except PydanticValidationError as ex:
            raise BadRequestException(extra=ex.errors(include_context=False)) from ex

    def _validate_json[T](self, t: type[T], v: str) -> T:
        try:
            return TypeAdapter(Json[t]).validate_strings(v)
        except PydanticValidationError as ex:
            raise BadRequestException(extra=ex.errors(include_context=False)) from ex

    @handlers.get(
        summary="List media",
        description="List media that match the request.",
    )
    async def list(
        self,
        service: Service,
        limit: Annotated[
            m.ListRequestLimit,
            Parameter(description="Maximum number of media to return.", default=10),
        ] = 10,
        offset: Annotated[
            m.ListRequestOffset,
            Parameter(description="Number of media to skip."),
        ] = None,
        where: Annotated[
            str | None,
            Parameter(description="Filter to apply to media."),
        ] = None,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with media."),
        ] = None,
        order: Annotated[
            str | None,
            Parameter(description="Order to apply to media."),
        ] = None,
    ) -> Response[m.ListResponseResults]:
        where = self._validate_json(m.ListRequestWhere, where) if where else None
        include = (
            self._validate_json(m.ListRequestInclude, include) if include else None
        )
        order = self._validate_json(m.ListRequestOrder, order) if order else None

        try:
            response = await service.list(
                m.ListRequest(
                    limit=limit,
                    offset=offset,
                    where=where,
                    include=include,
                    order=order,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex

        results = response.results

        return Response(results)

    @handlers.get(
        "/{id:uuid}",
        summary="Get media",
        description="Get media by ID.",
    )
    async def get(
        self,
        service: Service,
        id: m.GetRequestId,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with media."),
        ] = None,
    ) -> Response[m.GetResponseMedia]:
        include = self._validate_json(m.GetRequestInclude, include) if include else None

        try:
            response = await service.get(
                m.GetRequest(
                    id=id,
                    include=include,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        media = response.media

        return Response(media)

    @handlers.post(
        summary="Create media",
        description="Create media.",
    )
    async def create(
        self,
        service: Service,
        data: m.CreateRequestData,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with media."),
        ] = None,
    ) -> Response[m.CreateResponseMedia]:
        data = self._validate_pydantic(m.CreateRequestData, data)
        include = (
            self._validate_json(m.CreateRequestInclude, include) if include else None
        )

        try:
            response = await service.create(
                m.CreateRequest(
                    data=data,
                    include=include,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex

        media = response.media

        return Response(media)

    @handlers.patch(
        "/{id:uuid}",
        summary="Update media",
        description="Update media by ID.",
    )
    async def update(
        self,
        service: Service,
        id: m.UpdateRequestId,
        data: m.UpdateRequestData,
        include: Annotated[
            str | None,
            Parameter(description="Relations to include with media."),
        ] = None,
    ) -> Response[m.UpdateResponseMedia]:
        data = self._validate_pydantic(m.UpdateRequestData, data)
        include = (
            self._validate_json(m.UpdateRequestInclude, include) if include else None
        )

        try:
            response = await service.update(
                m.UpdateRequest(
                    data=data,
                    id=id,
                    include=include,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        media = response.media

        return Response(media)

    @handlers.delete(
        "/{id:uuid}",
        summary="Delete media",
        description="Delete media by ID.",
    )
    async def delete(
        self,
        service: Service,
        id: m.DeleteRequestId,
    ) -> Response[None]:
        try:
            await service.delete(
                m.DeleteRequest(
                    id=id,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        return Response(None)

    @handlers.put(
        "/{id:uuid}/content",
        summary="Upload media content",
        description="Upload media content by ID.",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def upload(
        self,
        service: Service,
        id: m.UploadRequestId,
        type: Annotated[
            str,
            Parameter(header="Content-Type", description="Content type."),
        ],
        request: Request,
    ) -> Response[None]:

        async def _stream(request: Request) -> AsyncGenerator[bytes]:
            stream = request.stream()
            while True:
                try:
                    chunk = await anext(stream)
                except (StopAsyncIteration, InternalServerException):
                    break

                yield chunk

        try:
            await service.upload(
                m.UploadRequest(
                    id=id,
                    content=m.UploadRequestContent(
                        type=type,
                        data=_stream(request),
                    ),
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        return Response(None)

    @handlers.get(
        "/{id:uuid}/content",
        summary="Download media content",
        description="Download media content by ID.",
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
        id: m.DownloadRequestId,
    ) -> Stream:
        try:
            response = await service.download(
                m.DownloadRequest(
                    id=id,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        content = response.content
        type = content.type
        size = content.size
        tag = content.tag
        modified = content.modified
        data = content.data

        headers = {
            "Content-Type": type,
            "Content-Length": str(size),
            "ETag": tag,
            "Last-Modified": httpstringify(modified),
        }
        return Stream(data, headers=headers)

    @handlers.head(
        "/{id:uuid}/content",
        summary="Get media content headers",
        description="Get media content headers by ID.",
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
        id: m.DownloadRequestId,
    ) -> Response[None]:
        try:
            response = await service.download(
                m.DownloadRequest(
                    id=id,
                )
            )
        except e.ValidationError as ex:
            raise BadRequestException(extra=ex.message) from ex
        except e.MediaNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex
        except e.ContentNotFoundError as ex:
            raise NotFoundException(extra=ex.message) from ex

        content = response.content
        type = content.type
        size = content.size
        tag = content.tag
        modified = content.modified

        headers = {
            "Content-Type": type,
            "Content-Length": str(size),
            "ETag": tag,
            "Last-Modified": httpstringify(modified),
        }
        return Response(None, headers=headers)
