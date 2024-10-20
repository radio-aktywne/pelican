from litestar.datastructures import State as LitestarState

from emitunes.config.models import Config
from emitunes.services.datatunes.service import DatatunesService
from emitunes.services.mediatunes.service import MediatunesService


class State(LitestarState):
    """Use this class as a type hint for the state of the service."""

    config: Config
    """Configuration for the service."""

    datatunes: DatatunesService
    """Service for datatunes database."""

    mediatunes: MediatunesService
    """Service for mediatunes database."""
