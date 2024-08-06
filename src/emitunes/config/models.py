from pydantic import BaseModel, Field

from emitunes.config.base import BaseConfig


class ServerConfig(BaseModel):
    """Configuration for the server."""

    host: str = "0.0.0.0"
    """Host to run the server on."""

    port: int = Field(42000, ge=0, le=65535)
    """Port to run the server on."""

    trusted: str | list[str] | None = "*"
    """Trusted IP addresses."""


class DatatunesSQLConfig(BaseModel):
    """Configuration for the SQL API of the datatunes database."""

    host: str = "localhost"
    """Host of the SQL API."""

    port: int = Field(41000, ge=1, le=65535)
    """Port of the SQL API."""

    password: str = "password"
    """Password to authenticate with the SQL API."""

    @property
    def url(self) -> str:
        """URL to connect to the SQL API."""

        return f"postgres://user:{self.password}@{self.host}:{self.port}/database"


class DatatunesConfig(BaseModel):
    """Configuration for the datatunes database."""

    sql: DatatunesSQLConfig = DatatunesSQLConfig()
    """Configuration for the SQL API of the datatunes database."""


class MediatunesS3Config(BaseModel):
    """Configuration for the S3 API of the mediatunes database."""

    secure: bool = False
    """Whether to use a secure connection."""

    host: str = "localhost"
    """Host of the S3 API."""

    port: int | None = Field(40000, ge=1, le=65535)
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


class MediatunesConfig(BaseModel):
    """Configuration for the mediatunes database."""

    s3: MediatunesS3Config = MediatunesS3Config()
    """Configuration for the S3 API of the mediatunes database."""


class Config(BaseConfig):
    """Configuration for the application."""

    server: ServerConfig = ServerConfig()
    """Configuration for the server."""

    datatunes: DatatunesConfig = DatatunesConfig()
    """Configuration for the datatunes database."""

    mediatunes: MediatunesConfig = MediatunesConfig()
    """Configuration for the mediatunes database."""

    debug: bool = False
    """Enable debug mode."""
