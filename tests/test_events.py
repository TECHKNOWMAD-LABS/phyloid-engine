import sys

sys.path.insert(0, "python")

from phyloid_engine.events import EventEmitter


def test_emit_receive():
    ee = EventEmitter()
    received = []
    ee.on("test", lambda d: received.append(d))
    ee.emit("test", 42)
    assert received == [42]


def test_once_fires_once():
    ee = EventEmitter()
    count = []
    ee.once("x", lambda: count.append(1))
    ee.emit("x")
    ee.emit("x")
    assert len(count) == 1
