from litestar.datastructures import State as LitestarState

from emitunes.config.models import Config
from emitunes.datatunes.service import DatatunesService
from emitunes.mediatunes.service import MediatunesService


class State(LitestarState):
    """Use this class as a type hint for the state of your application.

    Attributes:
        config: Configuration for the application.
        datatunes: Service for datatunes database.
        mediatunes: Service for mediatunes database.
    """

    config: Config
    datatunes: DatatunesService
    mediatunes: MediatunesService
