# ruff: noqa: D101, SLF001

from collections.abc import Sequence
from typing import TypedDict

from prisma import enums, fields, models, types  # noqa: F401


class StringWithAggregatesFilter(types.StringFilter, total=False):
    _max: types.StringFilter
    _min: types.StringFilter
    _sum: types.StringFilter
    _avg: types.StringFilter
    _count: types.IntFilter


types.StringWithAggregatesFilter = StringWithAggregatesFilter


class DateTimeWithAggregatesFilter(types.DateTimeFilter, total=False):
    _max: types.DateTimeFilter
    _min: types.DateTimeFilter
    _sum: types.DateTimeFilter
    _avg: types.DateTimeFilter
    _count: types.IntFilter


types.DateTimeWithAggregatesFilter = DateTimeWithAggregatesFilter


class BooleanWithAggregatesFilter(types.BooleanFilter, total=False):
    _max: types.BooleanFilter
    _min: types.BooleanFilter
    _sum: types.BooleanFilter
    _avg: types.BooleanFilter
    _count: types.IntFilter


types.BooleanWithAggregatesFilter = BooleanWithAggregatesFilter


class FloatWithAggregatesFilter(types.FloatFilter, total=False):
    _max: types.FloatFilter
    _min: types.FloatFilter
    _sum: types.FloatFilter
    _avg: types.FloatFilter
    _count: types.IntFilter


types.FloatWithAggregatesFilter = FloatWithAggregatesFilter


BytesFilter = TypedDict(
    "BytesFilter",
    {
        "equals": fields.Base64,
        "in": Sequence[fields.Base64],
        "not_in": Sequence[fields.Base64],
        "not": fields.Base64 | types.BytesFilter,
    },
    total=False,
)


types.BytesFilter = BytesFilter


class BytesWithAggregatesFilter(types.BytesFilter, total=False):
    _max: types.BytesFilter
    _min: types.BytesFilter
    _sum: types.BytesFilter
    _avg: types.BytesFilter
    _count: types.IntFilter


types.BytesWithAggregatesFilter = BytesWithAggregatesFilter


JsonFilter = TypedDict(
    "JsonFilter",
    {
        "equals": fields.Json,
        "not": fields.Json,
    },
    total=False,
)


types.JsonFilter = JsonFilter


class JsonWithAggregatesFilter(types.JsonFilter, total=False):
    _max: types.JsonFilter
    _min: types.JsonFilter
    _sum: types.JsonFilter
    _avg: types.JsonFilter
    _count: types.IntFilter


types.JsonWithAggregatesFilter = JsonWithAggregatesFilter


class DecimalWithAggregatesFilter(types.StringFilter, total=False):
    _max: types.DecimalFilter
    _min: types.DecimalFilter
    _sum: types.DecimalFilter
    _avg: types.DecimalFilter
    _count: types.IntFilter


types.DecimalWithAggregatesFilter = DecimalWithAggregatesFilter


class _BytesListFilterEqualsInput(TypedDict):
    equals: Sequence[fields.Base64] | None


types._BytesListFilterEqualsInput = _BytesListFilterEqualsInput


class _BytesListFilterHasInput(TypedDict):
    has: fields.Base64


types._BytesListFilterHasInput = _BytesListFilterHasInput


class _BytesListFilterHasEveryInput(TypedDict):
    has_every: Sequence[fields.Base64]


types._BytesListFilterHasEveryInput = _BytesListFilterHasEveryInput


class _BytesListFilterHasSomeInput(TypedDict):
    has_some: Sequence[fields.Base64]


types._BytesListFilterHasSomeInput = _BytesListFilterHasSomeInput


class _BytesListUpdateSet(TypedDict):
    set: Sequence[fields.Base64]


types._BytesListUpdateSet = _BytesListUpdateSet


BytesListUpdate = Sequence[fields.Base64] | types._BytesListUpdateSet


types.BytesListUpdate = BytesListUpdate


class _JsonListFilterEqualsInput(TypedDict):
    equals: Sequence[fields.Json] | None


types._JsonListFilterEqualsInput = _JsonListFilterEqualsInput


class _JsonListFilterHasInput(TypedDict):
    has: fields.Json


types._JsonListFilterHasInput = _JsonListFilterHasInput


class _JsonListFilterHasEveryInput(TypedDict):
    has_every: Sequence[fields.Json]


types._JsonListFilterHasEveryInput = _JsonListFilterHasEveryInput


class _JsonListFilterHasSomeInput(TypedDict):
    has_some: Sequence[fields.Json]


types._JsonListFilterHasSomeInput = _JsonListFilterHasSomeInput


class _JsonListUpdateSet(TypedDict):
    set: Sequence[fields.Json]


types._JsonListUpdateSet = _JsonListUpdateSet


JsonListUpdate = Sequence[fields.Json] | types._JsonListUpdateSet


class MediaOptionalCreateInput(TypedDict, total=False):
    id: str
    bindings: types.BindingCreateManyNestedWithoutRelationsInput


types.MediaOptionalCreateInput = MediaOptionalCreateInput


class MediaCreateNestedWithoutRelationsInput(TypedDict, total=False):
    create: types.MediaCreateWithoutRelationsInput
    connect: types.MediaWhereUniqueInput


types.MediaCreateNestedWithoutRelationsInput = MediaCreateNestedWithoutRelationsInput


class MediaCreateManyNestedWithoutRelationsInput(TypedDict, total=False):
    create: (
        types.MediaCreateWithoutRelationsInput
        | Sequence[types.MediaCreateWithoutRelationsInput]
    )
    connect: types.MediaWhereUniqueInput | Sequence[types.MediaWhereUniqueInput]


types.MediaCreateManyNestedWithoutRelationsInput = (
    MediaCreateManyNestedWithoutRelationsInput
)


types.MediaWhereUniqueInput = (
    types._MediaWhereUnique_id_Input | types._MediaWhereUnique_name_Input
)


class MediaUpdateInput(TypedDict, total=False):
    id: str
    name: str
    bindings: types.BindingUpdateManyWithoutRelationsInput


types.MediaUpdateInput = MediaUpdateInput


class MediaUpdateManyWithoutRelationsInput(TypedDict, total=False):
    create: Sequence[types.MediaCreateWithoutRelationsInput]
    connect: Sequence[types.MediaWhereUniqueInput]
    set: Sequence[types.MediaWhereUniqueInput]
    disconnect: Sequence[types.MediaWhereUniqueInput]
    delete: Sequence[types.MediaWhereUniqueInput]


types.MediaUpdateManyWithoutRelationsInput = MediaUpdateManyWithoutRelationsInput


class MediaUpdateOneWithoutRelationsInput(TypedDict, total=False):
    create: types.MediaCreateWithoutRelationsInput
    connect: types.MediaWhereUniqueInput
    disconnect: bool
    delete: bool


types.MediaUpdateOneWithoutRelationsInput = MediaUpdateOneWithoutRelationsInput


class MediaUpsertInput(TypedDict):
    create: types.MediaCreateInput
    update: types.MediaUpdateInput


types.MediaUpsertInput = MediaUpsertInput


class _MediaIdOrderByInput(TypedDict, total=True):
    id: types.SortOrder


types._Media_id_OrderByInput = _MediaIdOrderByInput


class _MediaNameOrderByInput(TypedDict, total=True):
    name: types.SortOrder


types._Media_name_OrderByInput = _MediaNameOrderByInput


types.MediaOrderByInput = types._Media_id_OrderByInput | types._Media_name_OrderByInput


MediaRelationFilter = TypedDict(
    "MediaRelationFilter",
    {
        "is": types.MediaWhereInput,
        "is_not": types.MediaWhereInput,
    },
    total=False,
)


types.MediaRelationFilter = MediaRelationFilter


class MediaListRelationFilter(TypedDict, total=False):
    some: types.MediaWhereInput
    none: types.MediaWhereInput
    every: types.MediaWhereInput


types.MediaListRelationFilter = MediaListRelationFilter


class MediaInclude(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromMedia


types.MediaInclude = MediaInclude


class MediaIncludeFromMedia(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromMedia


types.MediaIncludeFromMedia = MediaIncludeFromMedia


class MediaArgsFromMedia(TypedDict, total=False):
    include: types.MediaIncludeFromMedia


types.MediaArgsFromMedia = MediaArgsFromMedia


class FindManyMediaArgsFromMedia(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.MediaOrderByInput | Sequence[types.MediaOrderByInput]
    where: types.MediaWhereInput
    cursor: types.MediaWhereUniqueInput
    distinct: Sequence[types.MediaScalarFieldKeys]
    include: types.MediaIncludeFromMedia


types.FindManyMediaArgsFromMedia = FindManyMediaArgsFromMedia


class PlaylistIncludeFromMedia(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromMedia


types.PlaylistIncludeFromMedia = PlaylistIncludeFromMedia


class PlaylistArgsFromMedia(TypedDict, total=False):
    include: types.PlaylistIncludeFromPlaylist


types.PlaylistArgsFromMedia = PlaylistArgsFromMedia


class FindManyPlaylistArgsFromMedia(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.PlaylistOrderByInput | Sequence[types.PlaylistOrderByInput]
    where: types.PlaylistWhereInput
    cursor: types.PlaylistWhereUniqueInput
    distinct: Sequence[types.PlaylistScalarFieldKeys]
    include: types.PlaylistIncludeFromPlaylist


types.FindManyPlaylistArgsFromMedia = FindManyPlaylistArgsFromMedia


class BindingIncludeFromMedia(TypedDict, total=False):
    playlist: bool | types.PlaylistArgsFromMedia
    media: bool | types.MediaArgsFromMedia


types.BindingIncludeFromMedia = BindingIncludeFromMedia


class BindingArgsFromMedia(TypedDict, total=False):
    include: types.BindingIncludeFromBinding


types.BindingArgsFromMedia = BindingArgsFromMedia


class FindManyBindingArgsFromMedia(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.BindingOrderByInput | Sequence[types.BindingOrderByInput]
    where: types.BindingWhereInput
    cursor: types.BindingWhereUniqueInput
    distinct: Sequence[types.BindingScalarFieldKeys]
    include: types.BindingIncludeFromBinding


types.FindManyBindingArgsFromMedia = FindManyBindingArgsFromMedia


class MediaWhereInput(TypedDict, total=False):
    id: str | types.StringFilter
    name: str | types.StringFilter
    bindings: types.BindingListRelationFilter
    AND: Sequence[types.MediaWhereInput]
    OR: Sequence[types.MediaWhereInput]
    NOT: Sequence[types.MediaWhereInput]


types.MediaWhereInput = MediaWhereInput


class MediaScalarWhereWithAggregatesInput(TypedDict, total=False):
    id: str | types.StringWithAggregatesFilter
    name: str | types.StringWithAggregatesFilter
    AND: Sequence[types.MediaScalarWhereWithAggregatesInput]
    OR: Sequence[types.MediaScalarWhereWithAggregatesInput]
    NOT: Sequence[types.MediaScalarWhereWithAggregatesInput]


types.MediaScalarWhereWithAggregatesInput = MediaScalarWhereWithAggregatesInput


class MediaGroupByOutput(TypedDict, total=False):
    id: str
    name: str
    _sum: types.MediaSumAggregateOutput
    _avg: types.MediaAvgAggregateOutput
    _min: types.MediaMinAggregateOutput
    _max: types.MediaMaxAggregateOutput
    _count: types.MediaCountAggregateOutput


types.MediaGroupByOutput = MediaGroupByOutput


class PlaylistOptionalCreateInput(TypedDict, total=False):
    id: str
    bindings: types.BindingCreateManyNestedWithoutRelationsInput


types.PlaylistOptionalCreateInput = PlaylistOptionalCreateInput


class PlaylistCreateNestedWithoutRelationsInput(TypedDict, total=False):
    create: types.PlaylistCreateWithoutRelationsInput
    connect: types.PlaylistWhereUniqueInput


types.PlaylistCreateNestedWithoutRelationsInput = (
    PlaylistCreateNestedWithoutRelationsInput
)


class PlaylistCreateManyNestedWithoutRelationsInput(TypedDict, total=False):
    create: (
        types.PlaylistCreateWithoutRelationsInput
        | Sequence[types.PlaylistCreateWithoutRelationsInput]
    )
    connect: types.PlaylistWhereUniqueInput | Sequence[types.PlaylistWhereUniqueInput]


types.PlaylistCreateManyNestedWithoutRelationsInput = (
    PlaylistCreateManyNestedWithoutRelationsInput
)


types.PlaylistWhereUniqueInput = (
    types._PlaylistWhereUnique_id_Input | types._PlaylistWhereUnique_name_Input
)


class PlaylistUpdateInput(TypedDict, total=False):
    id: str
    name: str
    bindings: types.BindingUpdateManyWithoutRelationsInput


types.PlaylistUpdateInput = PlaylistUpdateInput


class PlaylistUpdateManyWithoutRelationsInput(TypedDict, total=False):
    create: Sequence[types.PlaylistCreateWithoutRelationsInput]
    connect: Sequence[types.PlaylistWhereUniqueInput]
    set: Sequence[types.PlaylistWhereUniqueInput]
    disconnect: Sequence[types.PlaylistWhereUniqueInput]
    delete: Sequence[types.PlaylistWhereUniqueInput]


types.PlaylistUpdateManyWithoutRelationsInput = PlaylistUpdateManyWithoutRelationsInput


class PlaylistUpdateOneWithoutRelationsInput(TypedDict, total=False):
    create: types.PlaylistCreateWithoutRelationsInput
    connect: types.PlaylistWhereUniqueInput
    disconnect: bool
    delete: bool


types.PlaylistUpdateOneWithoutRelationsInput = PlaylistUpdateOneWithoutRelationsInput


class PlaylistUpsertInput(TypedDict):
    create: types.PlaylistCreateInput
    update: types.PlaylistUpdateInput


types.PlaylistUpsertInput = PlaylistUpsertInput


class _PlaylistIdOrderByInput(TypedDict, total=True):
    id: types.SortOrder


types._Playlist_id_OrderByInput = _PlaylistIdOrderByInput


class _PlaylistNameOrderByInput(TypedDict, total=True):
    name: types.SortOrder


types._Playlist_name_OrderByInput = _PlaylistNameOrderByInput


types.PlaylistOrderByInput = (
    types._Playlist_id_OrderByInput | types._Playlist_name_OrderByInput
)


PlaylistRelationFilter = TypedDict(
    "PlaylistRelationFilter",
    {
        "is": types.PlaylistWhereInput,
        "is_not": types.PlaylistWhereInput,
    },
    total=False,
)


types.PlaylistRelationFilter = PlaylistRelationFilter


class PlaylistListRelationFilter(TypedDict, total=False):
    some: types.PlaylistWhereInput
    none: types.PlaylistWhereInput
    every: types.PlaylistWhereInput


types.PlaylistListRelationFilter = PlaylistListRelationFilter


class PlaylistInclude(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromPlaylist


types.PlaylistInclude = PlaylistInclude


class MediaIncludeFromPlaylist(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromPlaylist


types.MediaIncludeFromPlaylist = MediaIncludeFromPlaylist


class MediaArgsFromPlaylist(TypedDict, total=False):
    include: types.MediaIncludeFromMedia


types.MediaArgsFromPlaylist = MediaArgsFromPlaylist


class FindManyMediaArgsFromPlaylist(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.MediaOrderByInput | Sequence[types.MediaOrderByInput]
    where: types.MediaWhereInput
    cursor: types.MediaWhereUniqueInput
    distinct: Sequence[types.MediaScalarFieldKeys]
    include: types.MediaIncludeFromMedia


types.FindManyMediaArgsFromPlaylist = FindManyMediaArgsFromPlaylist


class PlaylistIncludeFromPlaylist(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromPlaylist


types.PlaylistIncludeFromPlaylist = PlaylistIncludeFromPlaylist


class PlaylistArgsFromPlaylist(TypedDict, total=False):
    include: types.PlaylistIncludeFromPlaylist


types.PlaylistArgsFromPlaylist = PlaylistArgsFromPlaylist


class FindManyPlaylistArgsFromPlaylist(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.PlaylistOrderByInput | Sequence[types.PlaylistOrderByInput]
    where: types.PlaylistWhereInput
    cursor: types.PlaylistWhereUniqueInput
    distinct: Sequence[types.PlaylistScalarFieldKeys]
    include: types.PlaylistIncludeFromPlaylist


types.FindManyPlaylistArgsFromPlaylist = FindManyPlaylistArgsFromPlaylist


class BindingIncludeFromPlaylist(TypedDict, total=False):
    playlist: bool | types.PlaylistArgsFromPlaylist
    media: bool | types.MediaArgsFromPlaylist


types.BindingIncludeFromPlaylist = BindingIncludeFromPlaylist


class BindingArgsFromPlaylist(TypedDict, total=False):
    include: types.BindingIncludeFromBinding


types.BindingArgsFromPlaylist = BindingArgsFromPlaylist


class FindManyBindingArgsFromPlaylist(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.BindingOrderByInput | Sequence[types.BindingOrderByInput]
    where: types.BindingWhereInput
    cursor: types.BindingWhereUniqueInput
    distinct: Sequence[types.BindingScalarFieldKeys]
    include: types.BindingIncludeFromBinding


types.FindManyBindingArgsFromPlaylist = FindManyBindingArgsFromPlaylist


class PlaylistWhereInput(TypedDict, total=False):
    id: str | types.StringFilter
    name: str | types.StringFilter
    bindings: types.BindingListRelationFilter
    AND: Sequence[types.PlaylistWhereInput]
    OR: Sequence[types.PlaylistWhereInput]
    NOT: Sequence[types.PlaylistWhereInput]


types.PlaylistWhereInput = PlaylistWhereInput


class PlaylistScalarWhereWithAggregatesInput(TypedDict, total=False):
    id: str | types.StringWithAggregatesFilter
    name: str | types.StringWithAggregatesFilter
    AND: Sequence[types.PlaylistScalarWhereWithAggregatesInput]
    OR: Sequence[types.PlaylistScalarWhereWithAggregatesInput]
    NOT: Sequence[types.PlaylistScalarWhereWithAggregatesInput]


types.PlaylistScalarWhereWithAggregatesInput = PlaylistScalarWhereWithAggregatesInput


class PlaylistGroupByOutput(TypedDict, total=False):
    id: str
    name: str
    _sum: types.PlaylistSumAggregateOutput
    _avg: types.PlaylistAvgAggregateOutput
    _min: types.PlaylistMinAggregateOutput
    _max: types.PlaylistMaxAggregateOutput
    _count: types.PlaylistCountAggregateOutput


types.PlaylistGroupByOutput = PlaylistGroupByOutput


class BindingOptionalCreateInput(TypedDict, total=False):
    id: str
    playlistId: str
    mediaId: str
    playlist: types.PlaylistCreateNestedWithoutRelationsInput
    media: types.MediaCreateNestedWithoutRelationsInput


types.BindingOptionalCreateInput = BindingOptionalCreateInput


class BindingCreateNestedWithoutRelationsInput(TypedDict, total=False):
    create: types.BindingCreateWithoutRelationsInput
    connect: types.BindingWhereUniqueInput


types.BindingCreateNestedWithoutRelationsInput = (
    BindingCreateNestedWithoutRelationsInput
)


class BindingCreateManyNestedWithoutRelationsInput(TypedDict, total=False):
    create: (
        types.BindingCreateWithoutRelationsInput
        | Sequence[types.BindingCreateWithoutRelationsInput]
    )
    connect: types.BindingWhereUniqueInput | Sequence[types.BindingWhereUniqueInput]


types.BindingCreateManyNestedWithoutRelationsInput = (
    BindingCreateManyNestedWithoutRelationsInput
)


types.BindingWhereUniqueInput = (
    types._BindingWhereUnique_id_Input | types._BindingCompoundplaylistId_rankKey
)


class BindingUpdateInput(TypedDict, total=False):
    id: str
    rank: str
    playlist: types.PlaylistUpdateOneWithoutRelationsInput
    media: types.MediaUpdateOneWithoutRelationsInput


types.BindingUpdateInput = BindingUpdateInput


class BindingUpdateManyWithoutRelationsInput(TypedDict, total=False):
    create: Sequence[types.BindingCreateWithoutRelationsInput]
    connect: Sequence[types.BindingWhereUniqueInput]
    set: Sequence[types.BindingWhereUniqueInput]
    disconnect: Sequence[types.BindingWhereUniqueInput]
    delete: Sequence[types.BindingWhereUniqueInput]


types.BindingUpdateManyWithoutRelationsInput = BindingUpdateManyWithoutRelationsInput


class BindingUpdateOneWithoutRelationsInput(TypedDict, total=False):
    create: types.BindingCreateWithoutRelationsInput
    connect: types.BindingWhereUniqueInput
    disconnect: bool
    delete: bool


types.BindingUpdateOneWithoutRelationsInput = BindingUpdateOneWithoutRelationsInput


class BindingUpsertInput(TypedDict):
    create: types.BindingCreateInput
    update: types.BindingUpdateInput


types.BindingUpsertInput = BindingUpsertInput


class _BindingIdOrderByInput(TypedDict, total=True):
    id: types.SortOrder


types._Binding_id_OrderByInput = _BindingIdOrderByInput


class _BindingPlaylistIdOrderByInput(TypedDict, total=True):
    playlistId: types.SortOrder


types._Binding_playlistId_OrderByInput = _BindingPlaylistIdOrderByInput


class _BindingMediaIdOrderByInput(TypedDict, total=True):
    mediaId: types.SortOrder


types._Binding_mediaId_OrderByInput = _BindingMediaIdOrderByInput


class _BindingRankOrderByInput(TypedDict, total=True):
    rank: types.SortOrder


types._Binding_rank_OrderByInput = _BindingRankOrderByInput


types.BindingOrderByInput = (
    types._Binding_id_OrderByInput
    | types._Binding_playlistId_OrderByInput
    | types._Binding_mediaId_OrderByInput
    | types._Binding_rank_OrderByInput
)


BindingRelationFilter = TypedDict(
    "BindingRelationFilter",
    {
        "is": types.BindingWhereInput,
        "is_not": types.BindingWhereInput,
    },
    total=False,
)


types.BindingRelationFilter = BindingRelationFilter


class BindingListRelationFilter(TypedDict, total=False):
    some: types.BindingWhereInput
    none: types.BindingWhereInput
    every: types.BindingWhereInput


types.BindingListRelationFilter = BindingListRelationFilter


class BindingInclude(TypedDict, total=False):
    playlist: bool | types.PlaylistArgsFromBinding
    media: bool | types.MediaArgsFromBinding


types.BindingInclude = BindingInclude


class MediaIncludeFromBinding(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromBinding


types.MediaIncludeFromBinding = MediaIncludeFromBinding


class MediaArgsFromBinding(TypedDict, total=False):
    include: types.MediaIncludeFromMedia


types.MediaArgsFromBinding = MediaArgsFromBinding


class FindManyMediaArgsFromBinding(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.MediaOrderByInput | Sequence[types.MediaOrderByInput]
    where: types.MediaWhereInput
    cursor: types.MediaWhereUniqueInput
    distinct: Sequence[types.MediaScalarFieldKeys]
    include: types.MediaIncludeFromMedia


types.FindManyMediaArgsFromBinding = FindManyMediaArgsFromBinding


class PlaylistIncludeFromBinding(TypedDict, total=False):
    bindings: bool | types.FindManyBindingArgsFromBinding


types.PlaylistIncludeFromBinding = PlaylistIncludeFromBinding


class PlaylistArgsFromBinding(TypedDict, total=False):
    include: types.PlaylistIncludeFromPlaylist


types.PlaylistArgsFromBinding = PlaylistArgsFromBinding


class FindManyPlaylistArgsFromBinding(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.PlaylistOrderByInput | Sequence[types.PlaylistOrderByInput]
    where: types.PlaylistWhereInput
    cursor: types.PlaylistWhereUniqueInput
    distinct: Sequence[types.PlaylistScalarFieldKeys]
    include: types.PlaylistIncludeFromPlaylist


types.FindManyPlaylistArgsFromBinding = FindManyPlaylistArgsFromBinding


class BindingIncludeFromBinding(TypedDict, total=False):
    playlist: bool | types.PlaylistArgsFromBinding
    media: bool | types.MediaArgsFromBinding


types.BindingIncludeFromBinding = BindingIncludeFromBinding


class BindingArgsFromBinding(TypedDict, total=False):
    include: types.BindingIncludeFromBinding


types.BindingArgsFromBinding = BindingArgsFromBinding


class FindManyBindingArgsFromBinding(TypedDict, total=False):
    take: int
    skip: int
    order_by: types.BindingOrderByInput | Sequence[types.BindingOrderByInput]
    where: types.BindingWhereInput
    cursor: types.BindingWhereUniqueInput
    distinct: Sequence[types.BindingScalarFieldKeys]
    include: types.BindingIncludeFromBinding


types.FindManyBindingArgsFromBinding = FindManyBindingArgsFromBinding


class BindingWhereInput(TypedDict, total=False):
    id: str | types.StringFilter
    playlistId: str | types.StringFilter
    mediaId: str | types.StringFilter
    rank: str | types.StringFilter
    playlist: types.PlaylistRelationFilter
    media: types.MediaRelationFilter
    AND: Sequence[types.BindingWhereInput]
    OR: Sequence[types.BindingWhereInput]
    NOT: Sequence[types.BindingWhereInput]


types.BindingWhereInput = BindingWhereInput


class BindingScalarWhereWithAggregatesInput(TypedDict, total=False):
    id: str | types.StringWithAggregatesFilter
    playlistId: str | types.StringWithAggregatesFilter
    mediaId: str | types.StringWithAggregatesFilter
    rank: str | types.StringWithAggregatesFilter
    AND: Sequence[types.BindingScalarWhereWithAggregatesInput]
    OR: Sequence[types.BindingScalarWhereWithAggregatesInput]
    NOT: Sequence[types.BindingScalarWhereWithAggregatesInput]


types.BindingScalarWhereWithAggregatesInput = BindingScalarWhereWithAggregatesInput


class BindingGroupByOutput(TypedDict, total=False):
    id: str
    playlistId: str
    mediaId: str
    rank: str
    _sum: types.BindingSumAggregateOutput
    _avg: types.BindingAvgAggregateOutput
    _min: types.BindingMinAggregateOutput
    _max: types.BindingMaxAggregateOutput
    _count: types.BindingCountAggregateOutput
