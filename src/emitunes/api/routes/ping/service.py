from emitunes.api.routes.ping import models as m


class Service:
    """Service for the ping endpoint."""

    async def ping(self, request: m.PingRequest) -> m.PingResponse:
        """Do nothing."""

        return m.PingResponse()
