from litestar.datastructures import State as LitestarState

from pelican.config.models import Config
from pelican.services.graphite.service import GraphiteService
from pelican.services.minium.service import MiniumService


class State(LitestarState):
    """Use this class as a type hint for the state of the service."""

    config: Config
    """Configuration for the service."""

    graphite: GraphiteService
    """Service for graphite database."""

    minium: MiniumService
    """Service for minium database."""
