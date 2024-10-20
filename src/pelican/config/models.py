from pydantic import BaseModel, Field

from pelican.config.base import BaseConfig


class ServerConfig(BaseModel):
    """Configuration for the server."""

    host: str = "0.0.0.0"
    """Host to run the server on."""

    port: int = Field(10200, ge=0, le=65535)
    """Port to run the server on."""

    trusted: str | list[str] | None = "*"
    """Trusted IP addresses."""


class GraphiteSQLConfig(BaseModel):
    """Configuration for the SQL API of the graphite database."""

    host: str = "localhost"
    """Host of the SQL API."""

    port: int = Field(10220, ge=1, le=65535)
    """Port of the SQL API."""

    password: str = "password"
    """Password to authenticate with the SQL API."""

    @property
    def url(self) -> str:
        """URL to connect to the SQL API."""

        return f"postgres://user:{self.password}@{self.host}:{self.port}/database"


class GraphiteConfig(BaseModel):
    """Configuration for the graphite database."""

    sql: GraphiteSQLConfig = GraphiteSQLConfig()
    """Configuration for the SQL API of the graphite database."""


class MiniumS3Config(BaseModel):
    """Configuration for the S3 API of the minium database."""

    secure: bool = False
    """Whether to use a secure connection."""

    host: str = "localhost"
    """Host of the S3 API."""

    port: int | None = Field(10210, ge=1, le=65535)
    """Port of the S3 API."""

    user: str = "readwrite"
    """Username to authenticate with the S3 API."""

    password: str = "password"
    """Password to authenticate with the S3 API."""

    @property
    def bucket(self) -> str:
        """Bucket to store media in."""

        return "default"

    @property
    def endpoint(self) -> str:
        """Endpoint to connect to the S3 API."""

        if self.port is None:
            return self.host

        return f"{self.host}:{self.port}"


class MiniumConfig(BaseModel):
    """Configuration for the minium database."""

    s3: MiniumS3Config = MiniumS3Config()
    """Configuration for the S3 API of the minium database."""


class Config(BaseConfig):
    """Configuration for the service."""

    server: ServerConfig = ServerConfig()
    """Configuration for the server."""

    graphite: GraphiteConfig = GraphiteConfig()
    """Configuration for the graphite database."""

    minium: MiniumConfig = MiniumConfig()
    """Configuration for the minium database."""

    debug: bool = False
    """Enable debug mode."""
