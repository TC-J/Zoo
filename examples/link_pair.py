"""Round-trips through Zoo Link: pair, ipc, and tcp."""

from __future__ import annotations

import threading

from zoo.link import Link, LinkBindingHandle


def _created(binding: LinkBindingHandle, inbox: list) -> None:
    with binding.create(timeout=5) as peer:
        inbox.append(peer.recv(timeout=5))


def main() -> None:
    alice, bob = Link.pair()
    alice.send({"ping": True})
    print("pair:", bob.recv())
    alice.close()
    bob.close()

    with Link.create("memory://demo-feeder") as binding:
        with Link.locate("memory://demo-feeder") as home:
            with binding.create(timeout=2) as peer:
                home.send("hay")
                print("memory:", peer.recv(timeout=2))

    inbox: list = []
    with Link.create("ipc://demo-feeder") as binding:
        waiter = threading.Thread(target=_created, args=(binding, inbox), daemon=True)
        waiter.start()
        with Link.locate(binding.uri) as home:
            home.send("ipc-hay")
        waiter.join(timeout=5)
    print("ipc:", inbox[0])

    inbox = []
    with Link.create("tcp://127.0.0.1:0") as binding:
        waiter = threading.Thread(target=_created, args=(binding, inbox), daemon=True)
        waiter.start()
        with Link.locate(binding.uri) as home:
            home.send("tcp-hay")
        waiter.join(timeout=5)
    print("tcp:", inbox[0])


if __name__ == "__main__":
    main()
