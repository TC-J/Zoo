from __future__ import annotations

import threading
import unittest
import uuid

from zoo.link import Link, LinkBindingHandle, LinkError, LinkTimeout


def _unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


class PairTests(unittest.TestCase):
    def test_send_recv_both_directions(self) -> None:
        alice, bob = Link.pair()
        self.addCleanup(alice.close)
        self.addCleanup(bob.close)
        alice.send({"ping": True})
        bob.send("pong")
        self.assertEqual(bob.recv(timeout=1), {"ping": True})
        self.assertEqual(alice.recv(timeout=1), "pong")

    def test_recv_timeout(self) -> None:
        alice, bob = Link.pair()
        self.addCleanup(alice.close)
        self.addCleanup(bob.close)
        with self.assertRaises(LinkTimeout):
            bob.recv(timeout=0.05)

    def test_context_manager_closes(self) -> None:
        alice, bob = Link.pair()
        self.addCleanup(bob.close)
        with alice:
            alice.send(1)
            self.assertEqual(bob.recv(timeout=1), 1)
        with self.assertRaises(LinkError):
            alice.send(2)

    def test_peer_close_unblocks_recv(self) -> None:
        alice, bob = Link.pair()
        self.addCleanup(bob.close)
        alice.close()
        with self.assertRaises(LinkError):
            bob.recv(timeout=1)

    def test_owner_is_stored(self) -> None:
        owner = object()
        alice, bob = Link.pair(owner=owner)
        self.addCleanup(alice.close)
        self.addCleanup(bob.close)
        self.assertIs(alice.owner, owner)
        self.assertIs(bob.owner, owner)
        self.assertEqual(alice.uri, "memory://pair")


class MemoryBindingTests(unittest.TestCase):
    def test_named_memory_create_locate(self) -> None:
        uri = f"memory://{_unique('feeder')}"
        with Link.create(uri) as binding:
            with Link.locate(uri) as home:
                with binding.create(timeout=1) as peer:
                    home.send("hay")
                    self.assertEqual(peer.recv(timeout=1), "hay")
                    peer.send({"ok": True})
                    self.assertEqual(home.recv(timeout=1), {"ok": True})

    def test_memory_from_two_threads(self) -> None:
        uri = f"memory://{_unique('threads')}"
        received: list = []

        def animal() -> None:
            with Link.locate(uri) as home:
                received.append(home.recv(timeout=2))

        with Link.create(uri) as binding:
            worker = threading.Thread(target=animal)
            worker.start()
            with binding.create(timeout=2) as peer:
                peer.send("from-gate")
            worker.join(timeout=3)
        self.assertEqual(received, ["from-gate"])

    def test_duplicate_memory_serve_fails(self) -> None:
        uri = f"memory://{_unique('dup')}"
        with Link.create(uri):
            with self.assertRaises(LinkError):
                Link.create(uri)

    def test_dial_memory_nobody(self) -> None:
        with self.assertRaises(LinkError):
            Link.locate(f"memory://{_unique('missing')}")


class IpcTests(unittest.TestCase):
    def test_ipc_serve_dial(self) -> None:
        uri = f"ipc://{_unique('feeder')}"
        received: list = []

        def create_one(binding: LinkBindingHandle) -> None:
            with binding.create(timeout=5) as peer:
                received.append(peer.recv(timeout=5))
                peer.send("ack")

        with Link.create(uri) as binding:
            worker = threading.Thread(target=create_one, args=(binding,))
            worker.start()
            with Link.locate(binding.uri) as home:
                home.send("hay")
                self.assertEqual(home.recv(timeout=5), "ack")
            worker.join(timeout=6)
        self.assertEqual(received, ["hay"])

    def test_ipc_dial_nobody(self) -> None:
        with self.assertRaises(LinkError):
            Link.locate(f"ipc://{_unique('missing')}")


class TcpTests(unittest.TestCase):
    def test_tcp_ephemeral_port_serve_dial(self) -> None:
        received: list = []

        def create_one(binding: LinkBindingHandle) -> None:
            with binding.create(timeout=5) as peer:
                received.append(peer.recv(timeout=5))

        with Link.create("tcp://127.0.0.1:0") as binding:
            host, port_s = binding.uri.removeprefix("tcp://").rsplit(":", 1)
            self.assertEqual(host, "127.0.0.1")
            self.assertNotEqual(int(port_s), 0)
            worker = threading.Thread(target=create_one, args=(binding,))
            worker.start()
            with Link.locate(binding.uri) as home:
                home.send({"via": "tcp"})
            worker.join(timeout=6)
        self.assertEqual(received, [{"via": "tcp"}])

    def test_tcp_accept_timeout(self) -> None:
        with Link.create("tcp://127.0.0.1:0") as binding:
            with self.assertRaises(LinkTimeout):
                binding.create(timeout=0.05)

    def test_tcp_dial_nobody(self) -> None:
        with self.assertRaises(LinkError):
            Link.locate("tcp://127.0.0.1:1")


class UriTests(unittest.TestCase):
    def test_invalid_uri(self) -> None:
        for uri in ("", "feeder", "http://x", "memory://", "ipc://", "tcp://127.0.0.1"):
            with self.subTest(uri=uri):
                with self.assertRaises(LinkError):
                    Link.create(uri)

    def test_tcp_requires_port(self) -> None:
        with self.assertRaises(LinkError):
            Link.locate("tcp://127.0.0.1")


if __name__ == "__main__":
    unittest.main()
