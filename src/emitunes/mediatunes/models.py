from collections.abc import AsyncIterable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Object:
    """Object model."""

    name: str
    modified: datetime | None
    size: int | None
    metadata: dict[str, str] | None
    type: str | None


@dataclass
class ListRequest:
    """Request for listing objects."""

    prefix: str | None = None
    recursive: bool = True


@dataclass
class ListResponse:
    """Response for listing objects."""

    objects: AsyncIterable[Object]


@dataclass
class UploadRequest:
    """Request for uploading an object."""

    name: str
    data: AsyncIterable[bytes]
    type: str | None = None
    chunk: int = 5 * (1024**2)


@dataclass
class UploadResponse:
    """Response for uploading an object."""

    object: Object


@dataclass
class GetRequest:
    """Request for getting an object."""

    name: str


@dataclass
class GetResponse:
    """Response for getting an object."""

    object: Object


@dataclass
class DownloadRequest:
    """Request for downloading object's data."""

    name: str
    chunk: int = 5 * (1024**2)


@dataclass
class DownloadResponse:
    """Response for downloading object's data."""

    data: AsyncIterable[bytes]


@dataclass
class CopyRequest:
    """Request for copying an object."""

    source: str
    destination: str


@dataclass
class CopyResponse:
    """Response for copying an object."""

    object: Object


@dataclass
class DeleteRequest:
    """Request for deleting an object."""

    name: str


@dataclass
class DeleteResponse:
    """Response for deleting an object."""

    object: Object
