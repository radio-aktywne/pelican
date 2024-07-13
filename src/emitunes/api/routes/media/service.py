from emitunes.api.routes.media import errors as e
from emitunes.api.routes.media import models as m
from emitunes.media import errors as me
from emitunes.media import models as mm
from emitunes.media.service import MediaService


class Service:
    """Service for the media endpoint."""

    def __init__(self, media: MediaService) -> None:
        self._media = media

    async def list(
        self,
        limit: m.ListLimitParameter,
        offset: m.ListOffsetParameter,
        where: m.ListWhereParameter,
        include: m.ListIncludeParameter,
        order: m.ListOrderParameter,
    ) -> m.ListResponse:
        """List media."""

        request = mm.CountRequest(
            where=where,
        )

        try:
            response = await self._media.count(request)
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        count = response.count

        request = mm.ListRequest(
            limit=limit,
            offset=offset,
            where=where,
            include=include,
            order=order,
        )

        try:
            response = await self._media.list(request)
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        return m.ListResponse(
            count=count,
            limit=limit,
            offset=offset,
            media=response.media,
        )

    async def get(
        self,
        id: m.GetIdParameter,
        include: m.GetIncludeParameter,
    ) -> m.GetResponse:
        """Get media."""

        request = mm.GetRequest(
            where={
                "id": str(id),
            },
            include=include,
        )

        try:
            response = await self._media.get(request)
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
            raise e.NotFoundError(id)

        return media

    async def create(
        self,
        data: m.CreateRequest,
        include: m.CreateIncludeParameter,
    ) -> m.CreateResponse:
        """Create media."""

        request = mm.CreateRequest(
            data=data,
            include=include,
        )

        try:
            response = await self._media.create(request)
        except me.ValidationError as error:
            raise e.ValidationError(error.message) from error
        except me.DatatunesError as error:
            raise e.DatatunesError(error.message) from error
        except me.MediatunesError as error:
            raise e.MediatunesError(error.message) from error
        except me.ServiceError as error:
            raise e.ServiceError(error.message) from error

        return response.media

    async def update(
        self,
        id: m.UpdateIdParameter,
        data: m.UpdateRequest,
        include: m.UpdateIncludeParameter,
    ) -> m.UpdateResponse:
        """Update media."""

        request = mm.UpdateRequest(
            data=data,
            where={
                "id": str(id),
            },
            include=include,
        )

        try:
            response = await self._media.update(request)
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
            raise e.NotFoundError(id)

        return media

    async def delete(
        self,
        id: m.DeleteIdParameter,
    ) -> m.DeleteResponse:
        """Delete media."""

        request = mm.DeleteRequest(
            where={
                "id": str(id),
            },
        )

        try:
            response = await self._media.delete(request)
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
            raise e.NotFoundError(id)

        return None
