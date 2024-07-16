from emitunes.api.routes.media import errors as e
from emitunes.api.routes.media import models as m
from emitunes.media import errors as me
from emitunes.media import models as mm
from emitunes.media.service import MediaService


class Service:
    """Service for the media endpoint."""

    def __init__(self, media: MediaService) -> None:
        self._media = media

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List media."""

        limit = request.limit
        offset = request.offset
        where = request.where
        include = request.include
        order = request.order

        try:
            response = await self._media.count(
                mm.CountRequest(
                    where=where,
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        count = response.count

        try:
            response = await self._media.list(
                mm.ListRequest(
                    limit=limit,
                    offset=offset,
                    where=where,
                    include=include,
                    order=order,
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        results = m.ListResponseResults(
            count=count,
            limit=limit,
            offset=offset,
            media=media,
        )
        return m.ListResponse(
            results=results,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get media."""

        id = request.id
        include = request.include

        try:
            response = await self._media.get(
                mm.GetRequest(
                    where={
                        "id": str(id),
                    },
                    include=include,
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        if media is None:
            raise e.MediaNotFoundError(id)

        return m.GetResponse(
            media=media,
        )

    async def create(self, request: m.CreateRequest) -> m.CreateResponse:
        """Create media."""

        data = request.data
        include = request.include

        try:
            response = await self._media.create(
                mm.CreateRequest(
                    data=data,
                    include=include,
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        return m.CreateResponse(
            media=media,
        )

    async def update(self, request: m.UpdateRequest) -> m.UpdateResponse:
        """Update media."""

        data = request.data
        id = request.id
        include = request.include

        try:
            response = await self._media.update(
                mm.UpdateRequest(
                    data=data,
                    where={
                        "id": str(id),
                    },
                    include=include,
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        if media is None:
            raise e.MediaNotFoundError(id)

        return m.UpdateResponse(
            media=media,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete media."""

        id = request.id

        try:
            response = await self._media.delete(
                mm.DeleteRequest(
                    where={
                        "id": str(id),
                    },
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        if media is None:
            raise e.MediaNotFoundError(id)

        return m.DeleteResponse()

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload media content."""

        id = request.id
        content = request.content

        try:
            response = await self._media.upload(
                mm.UploadRequest(
                    where={
                        "id": str(id),
                    },
                    content=content,
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        if media is None:
            raise e.MediaNotFoundError(id)

        return m.UploadResponse()

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download media content."""

        id = request.id

        try:
            response = await self._media.download(
                mm.DownloadRequest(
                    where={
                        "id": str(id),
                    },
                )
            )
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        media = response.media

        if media is None:
            raise e.MediaNotFoundError(id)

        content = response.content

        if content is None:
            raise e.ContentNotFoundError(id)

        return m.DownloadResponse(
            content=content,
        )
