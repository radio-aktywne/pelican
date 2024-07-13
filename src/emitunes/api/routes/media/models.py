from typing import TypeAlias
from uuid import UUID

from pydantic import Field

from emitunes.media import models as mm
from emitunes.models.base import SerializableModel

ListLimitParameter = int | None

ListOffsetParameter = int | None

ListWhereParameter = mm.MediaWhereInput | None

ListIncludeParameter = mm.MediaInclude | None

ListOrderParameter = mm.MediaOrderByInput | list[mm.MediaOrderByInput] | None


class ListResponse(SerializableModel):
    """Response from GET /media."""

    count: int = Field(
        ...,
        title="ListResponse.Count",
        description="Total number of media that matched the query.",
    )
    limit: int | None = Field(
        ...,
        title="ListResponse.Limit",
        description="Maximum number of returned media.",
    )
    offset: int | None = Field(
        ...,
        title="ListResponse.Offset",
        description="Number of media skipped.",
    )
    media: list[mm.Media] = Field(
        ...,
        title="ListResponse.Media",
        description="Media that matched the request.",
    )


GetIdParameter = UUID

GetIncludeParameter = mm.MediaInclude | None

GetResponse = mm.Media

CreateIncludeParameter = mm.MediaInclude | None

CreateRequest = mm.MediaCreateInput

CreateResponse = mm.Media

UpdateIdParameter = UUID

UpdateIncludeParameter = mm.MediaInclude | None

UpdateRequest = mm.MediaUpdateInput

UpdateResponse = mm.Media

DeleteIdParameter = UUID

DeleteResponse: TypeAlias = None
