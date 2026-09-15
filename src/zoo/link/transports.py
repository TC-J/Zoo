from __future__ import annotations

import queue
import socket
import threading
from multiprocessing.connection import Client as _connect
from multiprocessing.connection import Connection
from multiprocessing.connection import Listener as _bind
from typing import Protocol

from zoo.link.errors import LinkError, LinkTimeout
from zoo.link.uri import ParsedUri, ipc_endpoint, prepare_ipc_bind

_CLOSED = object()
_memory_bindings: dict[str, MemoryBinding] = {}
_memory_lock = threading.Lock()


class Transport(Protocol):
    def send(self, message: object) -> None: ...
    def recv(self, timeout: float | None = None) -> object: ...
    def close(self) -> None: ...


class LinkBinding(Protocol):
    uri: str

    def create(self, timeout: float | None = None) -> Transport: ...
    def close(self) -> None: ...


class LinkImplementation(Protocol):
    @staticmethod
    def create(parsed: ParsedUri) -> LinkBinding: ...

    @staticmethod
    def locate(parsed: ParsedUri) -> Transport: ...


class MemoryTransport:
    def __init__(self, outgoing: queue.Queue, incoming: queue.Queue) -> None:
        self._out = outgoing
        self._in = incoming
        self._closed = False

    @classmethod
    def pair(cls) -> tuple[MemoryTransport, MemoryTransport]:
        left_to_right: queue.Queue = queue.Queue()
        right_to_left: queue.Queue = queue.Queue()
        return (
            cls(outgoing=left_to_right, incoming=right_to_left),
            cls(outgoing=right_to_left, incoming=left_to_right),
        )

    def send(self, message: object) -> None:
        if self._closed:
            raise LinkError("link is closed")
        try:
            self._out.put(message)
        except Exception as exc:
            raise LinkError("send failed") from exc

    def recv(self, timeout: float | None = None) -> object:
        if self._closed:
            raise LinkError("link is closed")
        try:
            message = self._in.get(timeout=timeout)
        except queue.Empty:
            raise LinkTimeout("recv timed out") from None
        if message is _CLOSED:
            self._closed = True
            raise LinkError("link is closed")
        return message

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._out.put_nowait(_CLOSED)
        except Exception:
            pass


class MemoryBinding:
    def __init__(self, name: str) -> None:
        self._name = name
        self.uri = f"memory://{name}"
        self._pending: queue.Queue = queue.Queue()
        self._closed = False
        with _memory_lock:
            if name in _memory_bindings:
                raise LinkError(f"already serving {self.uri}")
            _memory_bindings[name] = self

    def _locate(self) -> MemoryTransport:
        if self._closed:
            raise LinkError(f"nothing is bound at {self.uri}")
        located, created = MemoryTransport.pair()
        self._pending.put(created)
        return located

    def create(self, timeout: float | None = None) -> MemoryTransport:
        if self._closed:
            raise LinkError("binding is closed")
        try:
            return self._pending.get(timeout=timeout)
        except queue.Empty:
            raise LinkTimeout("link creation timed out") from None

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        with _memory_lock:
            if _memory_bindings.get(self._name) is self:
                del _memory_bindings[self._name]


class MemoryLinks:
    @staticmethod
    def create(parsed: ParsedUri) -> MemoryBinding:
        if not parsed.name:
            raise LinkError("memory:// needs a name")
        return MemoryBinding(parsed.name)

    @staticmethod
    def locate(parsed: ParsedUri) -> MemoryTransport:
        if not parsed.name:
            raise LinkError("memory:// needs a name")
        uri = f"memory://{parsed.name}"
        with _memory_lock:
            binding = _memory_bindings.get(parsed.name)
        if binding is None:
            raise LinkError(f"nothing is bound at {uri}")
        return binding._locate()


class ConnectionBinding:
    def __init__(self, address: str | tuple, family: str, uri: str) -> None:
        try:
            self._binding = _bind(address, family=family, backlog=16, authkey=None)
        except OSError as exc:
            raise LinkError(f"could not create binding at {uri}") from exc
        self.uri = uri
        if family == "AF_INET":
            host, port = self._binding.address
            self.uri = f"tcp://{host}:{port}"
        self._closed = False

    def create(self, timeout: float | None = None) -> ConnectionTransport:
        if self._closed:
            raise LinkError("binding is closed")
        try:
            connection = _receive_connection(self._binding, timeout)
        except LinkTimeout:
            raise
        except Exception as exc:
            raise LinkError("link creation failed") from exc
        return ConnectionTransport(connection)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._binding.close()
        except OSError:
            pass


class ConnectionLinks:
    @staticmethod
    def create(parsed: ParsedUri) -> ConnectionBinding:
        if parsed.scheme == "ipc":
            if not parsed.name:
                raise LinkError("ipc:// needs a name")
            address, family = ipc_endpoint(parsed.name)
            prepare_ipc_bind(address, family)
            return ConnectionBinding(address, family, uri=f"ipc://{parsed.name}")
        if parsed.host is None or parsed.port is None:
            raise LinkError("tcp:// needs a host and port")
        return ConnectionBinding(
            (parsed.host, parsed.port), "AF_INET", uri=parsed.original
        )

    @staticmethod
    def locate(parsed: ParsedUri) -> ConnectionTransport:
        if parsed.scheme == "ipc":
            if not parsed.name:
                raise LinkError("ipc:// needs a name")
            address, family = ipc_endpoint(parsed.name)
        else:
            if parsed.host is None or parsed.port is None:
                raise LinkError("tcp:// needs a host and port")
            address, family = (parsed.host, parsed.port), "AF_INET"
        try:
            connection = _connect(address, family=family, authkey=None)
        except (ConnectionRefusedError, FileNotFoundError, OSError) as exc:
            raise LinkError(f"could not locate {parsed.original}") from exc
        return ConnectionTransport(connection)


def implementation_for(parsed: ParsedUri) -> LinkImplementation:
    if parsed.scheme == "memory":
        return MemoryLinks
    return ConnectionLinks


class ConnectionTransport:
    def __init__(self, connection: Connection) -> None:
        self._conn = connection
        self._closed = False

    def send(self, message: object) -> None:
        if self._closed:
            raise LinkError("link is closed")
        try:
            self._conn.send(message)
        except Exception as exc:
            raise LinkError("send failed") from exc

    def recv(self, timeout: float | None = None) -> object:
        if self._closed:
            raise LinkError("link is closed")
        try:
            if timeout is not None and not self._conn.poll(timeout):
                raise LinkTimeout("recv timed out")
            return self._conn.recv()
        except LinkTimeout:
            raise
        except (EOFError, OSError, BrokenPipeError) as exc:
            self._closed = True
            raise LinkError("link is closed") from exc
        except Exception as exc:
            raise LinkError("recv failed") from exc

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._conn.close()
        except OSError:
            pass


def _binding_socket(binding: _bind) -> socket.socket | None:
    inner = getattr(binding, "_listener", None)
    sock = getattr(inner, "_socket", None)
    return sock if isinstance(sock, socket.socket) else None


def _receive_connection(binding: _bind, timeout: float | None) -> Connection:
    sock = _binding_socket(binding)
    if sock is not None:
        previous = sock.gettimeout()
        sock.settimeout(timeout)
        try:
            return binding.accept()
        except TimeoutError as exc:
            raise LinkTimeout("accept timed out") from exc
        finally:
            try:
                sock.settimeout(previous)
            except OSError:
                pass

    if timeout is None:
        return binding.accept()

    box: list[Connection] = []
    errors: list[BaseException] = []

    def run() -> None:
        try:
            box.append(binding.accept())
        except Exception as exc:
            errors.append(exc)

    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    worker.join(timeout)
    if worker.is_alive():
        raise LinkTimeout("link creation timed out")
    if errors:
        raise errors[0]
    return box[0]
