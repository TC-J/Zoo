from __future__ import annotations

from typing import Self

from zoo.link.errors import LinkError
from zoo.link.transports import (
    LinkBinding,
    MemoryTransport,
    Transport,
    implementation_for,
)
from zoo.link.uri import parse_link_uri


class Link:
    """A two-ended "wire"-like abstraction. Same send/recv API for memory, ipc, and tcp."""
    # TODO: add abstractions for windows named pipes, linux pipes, lock files, all ipc mechanisms

    def __init__(
        self,
        transport: Transport,
        uri: str,
        owner: object | None = None,
    ) -> None:
        self._transport = transport
        self._uri = uri
        self.owner = owner
        self._closed = False

    @property
    def uri(self) -> str:
        return self._uri

    @classmethod
    def pair(cls, owner: object | None = None) -> tuple[Link, Link]:
        left, right = MemoryTransport.pair()
        return (
            cls(left, uri="memory://pair", owner=owner),
            cls(right, uri="memory://pair", owner=owner),
        )

    @classmethod
    def create(cls, uri: str, owner: object | None = None) -> LinkBindingHandle:
        parsed = parse_link_uri(uri)
        binding = implementation_for(parsed).create(parsed)
        return LinkBindingHandle(binding, owner=owner)

    @classmethod
    def locate(cls, uri: str, owner: object | None = None) -> Link:
        parsed = parse_link_uri(uri)
        transport: Transport = implementation_for(parsed).locate(parsed)
        return cls(transport, uri=uri, owner=owner)

    def send(self, message: object) -> None:
        self._ensure_open()
        self._transport.send(message)

    def recv(self, timeout: float | None = None) -> object:
        self._ensure_open()
        return self._transport.recv(timeout)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._transport.close()

    def _ensure_open(self) -> None:
        if self._closed:
            raise LinkError("link is closed")

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class LinkBindingHandle:
    """A named link binding that creates connected wires."""

    def __init__(self, binding: LinkBinding, owner: object | None = None) -> None:
        self._binding = binding
        self.owner = owner
        self._closed = False

    @property
    def uri(self) -> str:
        return self._binding.uri

    def create(self, timeout: float | None = None) -> Link:
        if self._closed:
            raise LinkError("binding is closed")
        transport = self._binding.create(timeout)
        return Link(transport, uri=self.uri, owner=self.owner)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._binding.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
