from pydantic import BaseModel, Field

from emitunes.config.base import BaseConfig


class ServerConfig(BaseModel):
    """Configuration for the server."""

    host: str = Field(
        "0.0.0.0",
        title="Host",
        description="Host to run the server on.",
    )
    port: int = Field(
        42000,
        ge=0,
        le=65535,
        title="Port",
        description="Port to run the server on.",
    )
    trusted: str | list[str] | None = Field(
        "*",
        title="Trusted",
        description="Trusted IP addresses.",
    )


class DatatunesSQLConfig(BaseModel):
    """Configuration for the SQL API of the datatunes database."""

    host: str = Field(
        "localhost",
        title="Host",
        description="Host of the SQL API.",
    )
    port: int = Field(
        41000,
        ge=1,
        le=65535,
        title="Port",
        description="Port of the SQL API .",
    )
    password: str = Field(
        "password",
        title="Password",
        description="Password to authenticate with the SQL API.",
    )

    @property
    def url(self) -> str:
        return f"postgres://user:{self.password}@{self.host}:{self.port}/database"


class DatatunesConfig(BaseModel):
    """Configuration for the datatunes database."""

    sql: DatatunesSQLConfig = Field(
        DatatunesSQLConfig(),
        title="SQL",
        description="Configuration for the SQL API of the datatunes database.",
    )


class MediatunesS3Config(BaseModel):
    """Configuration for the S3 API of the mediatunes database."""

    secure: bool = Field(
        False,
        title="Secure",
        description="Whether to use a secure connection.",
    )
    host: str = Field(
        "localhost",
        title="Host",
        description="Host of the S3 API.",
    )
    port: int | None = Field(
        40000,
        ge=1,
        le=65535,
        title="Port",
        description="Port of the S3 API.",
    )
    user: str = Field(
        "readwrite",
        title="User",
        description="Username to authenticate with the S3 API.",
    )
    password: str = Field(
        "password",
        title="Password",
        description="Password to authenticate with the S3 API.",
    )

    @property
    def bucket(self) -> str:
        return "default"

    @property
    def endpoint(self) -> str:
        if self.port is None:
            return self.host

        return f"{self.host}:{self.port}"


class MediatunesConfig(BaseModel):
    """Configuration for the mediatunes database."""

    s3: MediatunesS3Config = Field(
        MediatunesS3Config(),
        title="S3",
        description="Configuration for the S3 API of the mediatunes database.",
    )


class Config(BaseConfig):
    """Configuration for the application."""

    server: ServerConfig = Field(
        ServerConfig(),
        title="Server",
        description="Configuration for the server.",
    )
    datatunes: DatatunesConfig = Field(
        DatatunesConfig(),
        title="Datatunes",
        description="Configuration for the datatunes database.",
    )
    mediatunes: MediatunesConfig = Field(
        MediatunesConfig(),
        title="Datatimes",
        description="Configuration for the mediatunes database.",
    )
