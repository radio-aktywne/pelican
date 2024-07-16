from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class Object:
    """Object model."""

    name: str
    modified: datetime | None
    size: int | None
    metadata: dict[str, str] | None
    type: str | None


@dataclass(kw_only=True)
class UploadContent:
    """Content model for upload."""

    type: str
    data: AsyncIterator[bytes]


@dataclass(kw_only=True)
class DownloadContent:
    """Content model for download."""

    type: str
    size: int
    tag: str
    modified: datetime
    data: AsyncIterator[bytes]


@dataclass(kw_only=True)
class ListRequest:
    """Request for listing objects."""

    prefix: str | None = None
    recursive: bool = True


@dataclass(kw_only=True)
class ListResponse:
    """Response for listing objects."""

    objects: AsyncIterator[Object]


@dataclass(kw_only=True)
class UploadRequest:
    """Request for uploading an object."""

    name: str
    content: UploadContent
    chunk: int = 5 * (1024**2)


@dataclass(kw_only=True)
class UploadResponse:
    """Response for uploading an object."""

    object: Object


@dataclass(kw_only=True)
class GetRequest:
    """Request for getting an object."""

    name: str


@dataclass(kw_only=True)
class GetResponse:
    """Response for getting an object."""

    object: Object


@dataclass(kw_only=True)
class DownloadRequest:
    """Request for downloading object's data."""

    name: str
    chunk: int = 5 * (1024**2)


@dataclass(kw_only=True)
class DownloadResponse:
    """Response for downloading object's data."""

    content: DownloadContent


@dataclass(kw_only=True)
class CopyRequest:
    """Request for copying an object."""

    source: str
    destination: str


@dataclass(kw_only=True)
class CopyResponse:
    """Response for copying an object."""

    object: Object


@dataclass(kw_only=True)
class DeleteRequest:
    """Request for deleting an object."""

    name: str


@dataclass(kw_only=True)
class DeleteResponse:
    """Response for deleting an object."""

    object: Object
