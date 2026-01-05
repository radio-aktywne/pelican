from collections.abc import Iterable


class M3U:
    """Playlist in M3U format."""

    def __init__(self, entries: Iterable[str]) -> None:
        self._entries = entries

    def __str__(self) -> str:
        return "\n".join([*list(self._entries), ""])
