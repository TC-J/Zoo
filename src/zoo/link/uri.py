from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from zoo.link.errors import LinkError

_SCHEMES = frozenset({"memory", "ipc", "tcp"})
_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


@dataclass(frozen=True)
class ParsedUri:
    scheme: str
    original: str
    name: str | None = None
    host: str | None = None
    port: int | None = None


def parse_link_uri(uri: str) -> ParsedUri:
    if not uri or not isinstance(uri, str):
        raise LinkError("link uri must be a non-empty string")

    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    if scheme not in _SCHEMES:
        raise LinkError(
            f"unsupported link uri {uri!r}; use memory://name, ipc://name, or tcp://host:port"
        )

    if scheme in {"memory", "ipc"}:
        name = f"{parsed.netloc}{parsed.path}".strip("/")
        if not name:
            raise LinkError(f"{scheme}:// needs a name")
        return ParsedUri(scheme=scheme, original=uri, name=name)

    host = parsed.hostname
    port = parsed.port
    if not host or port is None:
        raise LinkError("tcp:// needs a host and port, for example tcp://127.0.0.1:0")
    return ParsedUri(scheme="tcp", original=uri, host=host, port=port)


def ipc_endpoint(name: str) -> tuple[str, str]:
    """Return `(address, family)` for an `ipc://` name on this OS."""
    safe = _safe_ipc_name(name)
    if os.name == "nt":
        return rf"\\.\pipe\zoo.{safe}", "AF_PIPE"
    path = _unix_ipc_dir() / safe
    return str(path), "AF_UNIX"


def prepare_ipc_bind(address: str, family: str) -> None:
    if family != "AF_UNIX":
        return
    path = Path(address)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()


def _safe_ipc_name(name: str) -> str:
    parts = [p for p in re.split(r"[/\\]+", name) if p]
    if not parts:
        raise LinkError("ipc:// needs a name")
    cleaned = []
    for part in parts:
        token = _UNSAFE.sub("-", part).strip(".-")
        if not token or token in {".", ".."}:
            raise LinkError(f"invalid ipc name: {name!r}")
        cleaned.append(token)
    return ".".join(cleaned)


def _unix_ipc_dir() -> Path:
    from platformdirs import user_runtime_dir

    root = Path(user_runtime_dir(appname="zoo", appauthor="zoo"))
    return root / "ipc"
