import os
import subprocess

from pelican.config.models import Config


class GraphiteMigrator:
    """Migrator class for graphite database migrations."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def _get_command(self) -> list[str]:
        return ["prisma", "migrate", "deploy"]

    def _get_connection_string(self) -> str:
        return self._config.graphite.sql.url

    def _get_env(self) -> dict[str, str]:
        env = os.environ.copy()

        return env | {
            "PRISMA_DB_URL": self._get_connection_string(),
        }

    def migrate(self) -> None:
        """Apply migrations."""

        try:
            subprocess.run(
                self._get_command(),
                env=self._get_env(),
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as ex:
            message = ex.stderr.decode() if ex.stderr else "Unknown error."
            raise RuntimeError(message) from ex
