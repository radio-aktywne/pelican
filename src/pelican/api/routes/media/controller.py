from collections.abc import Mapping
from dataclasses import dataclass
from typing import Annotated, Any, cast

from litestar import Controller as BaseController
from litestar import Request, handlers
from litestar.datastructures import ResponseHeader
from litestar.di import Provide
from litestar.openapi.spec import (
    OpenAPIFormat,
    OpenAPIMediaType,
    OpenAPIResponse,
    OpenAPIType,
    Operation,
    RequestBody,
    Schema,
)
from litestar.params import Body, Parameter
from litestar.response import Response, Stream
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from pydantic import TypeAdapter

from pelican.api.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from pelican.api.routes.media import errors as e
from pelican.api.routes.media import models as m
from pelican.api.routes.media.service import Service
from pelican.models.base import Jsonable, Serializable
from pelican.services.entities.media.service import MediaService
from pelican.state import State


@dataclass
class UploadOperation(Operation):
    """OpenAPI Operation for uploading media content by ID."""

    def __post_init__(self) -> None:
        self.request_body = RequestBody(
            content={
                "*/*": OpenAPIMediaType(
                    schema=Schema(type=OpenAPIType.STRING, format=OpenAPIFormat.BINARY)
                )
            },
            required=True,
        )


@dataclass
class DownloadOperation(Operation):
    """OpenAPI Operation for downloading media content by ID."""

    def __post_init__(self) -> None:
        if (
            self.responses
            and str(HTTP_200_OK) in self.responses
            and (response := self.responses[str(HTTP_200_OK)])
            and isinstance(response, OpenAPIResponse)
            and (content := response.content)
            and "*/*" in content
            and (schema := content["*/*"].schema)
            and isinstance(schema, Schema)
        ):
            schema.type = OpenAPIType.STRING
            schema.format = OpenAPIFormat.BINARY


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State) -> Service:
        return Service(media=MediaService(graphite=state.graphite, minium=state.minium))

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
        raises=[BadRequestException],
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
        raises=[BadRequestException, NotFoundException],
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
        except e.NotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.media))

    @handlers.post(
        summary="Create media",
        raises=[BadRequestException, ConflictException],
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
        except e.ConflictError as ex:
            raise ConflictException from ex
        except e.ValidationError as ex:
            raise BadRequestException from ex

        return Response(Serializable(response.media))

    @handlers.patch(
        "/{id:str}",
        summary="Update media",
        raises=[BadRequestException, NotFoundException, ConflictException],
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
        except e.ConflictError as ex:
            raise ConflictException from ex
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.NotFoundError as ex:
            raise NotFoundException from ex

        return Response(Serializable(response.media))

    @handlers.delete(
        "/{id:str}",
        summary="Delete media",
        raises=[BadRequestException, NotFoundException],
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
    ) -> None:
        """Delete media by ID."""
        request = m.DeleteRequest(id=id.root)

        try:
            await service.delete(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.NotFoundError as ex:
            raise NotFoundException from ex

    @handlers.put(
        "/{id:str}/content",
        summary="Upload media content",
        status_code=HTTP_204_NO_CONTENT,
        raises=[BadRequestException, NotFoundException],
        operation_class=UploadOperation,
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
    ) -> None:
        """Upload media content by ID."""
        data = request.stream()

        try:
            req = m.UploadRequest(id=id.root, type=type.root, data=data)

            try:
                await service.upload(req)
            except e.ValidationError as ex:
                raise BadRequestException from ex
            except e.NotFoundError as ex:
                raise NotFoundException from ex
        finally:
            await data.aclose()

    @handlers.get(
        "/{id:str}/content",
        summary="Download media content",
        status_code=HTTP_200_OK,
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                required=True,
                documentation_only=True,
            ),
            ResponseHeader(
                name="Content-Length",
                required=True,
                documentation_only=True,
            ),
            ResponseHeader(
                name="ETag",
                required=True,
                documentation_only=True,
            ),
            ResponseHeader(
                name="Last-Modified",
                required=True,
                documentation_only=True,
            ),
        ],
        media_type="*/*",
        raises=[BadRequestException, NotFoundException],
        operation_class=DownloadOperation,
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
        except e.NotFoundError as ex:
            raise NotFoundException from ex

        def dump(value: Any, type: Any) -> str:  # noqa: A002
            return str(TypeAdapter(type).dump_python(value, mode="json"))

        try:
            headers = {
                "Content-Type": dump(response.type, m.DownloadResponseType),
                "Content-Length": dump(response.size, m.DownloadResponseSize),
                "ETag": dump(response.tag, m.DownloadResponseTag),
                "Last-Modified": dump(response.modified, m.DownloadResponseModified),
            }

            return Stream(response.data, headers=headers)
        except:
            await response.data.aclose()
            raise

    @handlers.head(
        "/{id:str}/content",
        summary="Get media content headers",
        response_description="Request fulfilled, headers follow",
        response_headers=[
            ResponseHeader(
                name="Content-Type",
                required=True,
                documentation_only=True,
            ),
            ResponseHeader(
                name="Content-Length",
                required=True,
                documentation_only=True,
            ),
            ResponseHeader(
                name="ETag",
                required=True,
                documentation_only=True,
            ),
            ResponseHeader(
                name="Last-Modified",
                required=True,
                documentation_only=True,
            ),
        ],
        raises=[BadRequestException, NotFoundException],
    )
    async def headdownload(
        self,
        service: Service,
        id: Annotated[  # noqa: A002
            Serializable[m.HeadDownloadRequestId],
            Parameter(
                description="Identifier of the media to get content headers for.",
            ),
        ],
    ) -> None:
        """Get media content headers by ID."""
        request = m.HeadDownloadRequest(id=id.root)

        try:
            response = await service.headdownload(request)
        except e.ValidationError as ex:
            raise BadRequestException from ex
        except e.NotFoundError as ex:
            raise NotFoundException from ex

        def dump(value: Any, type: Any) -> str:  # noqa: A002
            return str(TypeAdapter(type).dump_python(value, mode="json"))

        headers = {
            "Content-Type": dump(response.type, m.HeadDownloadResponseType),
            "Content-Length": dump(response.size, m.HeadDownloadResponseSize),
            "ETag": dump(response.tag, m.HeadDownloadResponseTag),
            "Last-Modified": dump(response.modified, m.HeadDownloadResponseModified),
        }

        return cast("None", Response(None, headers=headers))
