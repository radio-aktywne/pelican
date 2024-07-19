from typing import Union

from prisma import models as pm
from prisma import types as pt

# Monkey-patching to simplify types
pt.PlaylistWhereUniqueInput = Union[
    pt._PlaylistWhereUnique_id_Input, pt._PlaylistWhereUnique_name_Input
]
pt.PlaylistOrderByInput = pt._Playlist_id_OrderByInput | pt._Playlist_name_OrderByInput

pt.MediaWhereUniqueInput = (
    pt._MediaWhereUnique_id_Input | pt._MediaWhereUnique_name_Input
)
pt.MediaOrderByInput = pt._Media_id_OrderByInput | pt._Media_name_OrderByInput

pt.BindingWhereUniqueInput = (
    pt._BindingWhereUnique_id_Input | pt._BindingCompoundplaylistId_rankKey
)
pt.BindingOrderByInput = (
    pt._Binding_id_OrderByInput
    | pt._Binding_playlistId_OrderByInput
    | pt._Binding_mediaId_OrderByInput
    | pt._Binding_rank_OrderByInput
)

models = pm
types = pt
