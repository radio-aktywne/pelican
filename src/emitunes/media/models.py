from dataclasses import dataclass

from prisma import models as pm
from prisma import types as pt

# Monkey-patching to simplify types
pt.MediaWhereUniqueInput = (
    pt._MediaWhereUnique_id_Input | pt._MediaWhereUnique_name_Input
)
pt.MediaOrderByInput = (
    pt._Media_id_OrderByInput
    | pt._Media_name_OrderByInput
    | pt._Media_type_OrderByInput
)

Media = pm.Media

MediaWhereInput = pt.MediaWhereInput

MediaInclude = pt.MediaInclude

MediaWhereUniqueInput = pt.MediaWhereUniqueInput

MediaOrderByInput = pt.MediaOrderByInput

MediaCreateInput = pt.MediaCreateInput

MediaUpdateInput = pt.MediaUpdateInput


@dataclass
class CountRequest:
    """Request to count media."""

    where: MediaWhereInput | None = None


@dataclass
class CountResponse:
    """Response for counting media."""

    count: int


@dataclass
class ListRequest:
    """Request to list media."""

    limit: int | None = None
    offset: int | None = None
    where: MediaWhereInput | None = None
    include: MediaInclude | None = None
    order: MediaOrderByInput | list[MediaOrderByInput] | None = None


@dataclass
class ListResponse:
    """Response for listing media."""

    media: list[Media]


@dataclass
class GetRequest:
    """Request to get media."""

    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass
class GetResponse:
    """Response for getting media."""

    media: Media | None


@dataclass
class CreateRequest:
    """Request to create media."""

    data: MediaCreateInput
    include: MediaInclude | None = None


@dataclass
class CreateResponse:
    """Response for creating media."""

    media: Media


@dataclass
class UpdateRequest:
    """Request to update media."""

    data: MediaUpdateInput
    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass
class UpdateResponse:
    """Response for updating media."""

    media: Media | None


@dataclass
class DeleteRequest:
    """Request to delete media."""

    where: MediaWhereUniqueInput
    include: MediaInclude | None = None


@dataclass
class DeleteResponse:
    """Response for deleting media."""

    media: Media | None
