from litestar.datastructures import State as LitestarState

from emitunes.config.models import Config


class State(LitestarState):
    """Use this class as a type hint for the state of your application.

    Attributes:
        config: Configuration for the application.
    """

    config: Config
