"""Comprehensive tests for EventEmitter."""

import sys

sys.path.insert(0, "python")


class TestEventEmitterOn:
    def test_basic_emit_receive(self, emitter):
        received = []
        emitter.on("test", lambda d: received.append(d))
        emitter.emit("test", 42)
        assert received == [42]

    def test_multiple_listeners(self, emitter):
        a, b = [], []
        emitter.on("e", lambda x: a.append(x))
        emitter.on("e", lambda x: b.append(x))
        emitter.emit("e", "hello")
        assert a == ["hello"]
        assert b == ["hello"]

    def test_multiple_args(self, emitter):
        received = []
        emitter.on("e", lambda *args: received.append(args))
        emitter.emit("e", 1, 2, 3)
        assert received == [(1, 2, 3)]

    def test_no_args(self, emitter):
        count = []
        emitter.on("e", lambda: count.append(1))
        emitter.emit("e")
        assert len(count) == 1

    def test_chainable(self, emitter):
        result = emitter.on("e", lambda: None)
        assert result is emitter


class TestEventEmitterOnce:
    def test_fires_once(self, emitter):
        count = []
        emitter.once("x", lambda: count.append(1))
        emitter.emit("x")
        emitter.emit("x")
        emitter.emit("x")
        assert len(count) == 1

    def test_chainable(self, emitter):
        result = emitter.once("e", lambda: None)
        assert result is emitter


class TestEventEmitterOff:
    def test_remove_specific_listener(self, emitter):
        received = []

        def fn(d):
            return received.append(d)

        emitter.on("e", fn)
        emitter.off("e", fn)
        emitter.emit("e", 1)
        assert received == []

    def test_remove_all_listeners_for_event(self, emitter):
        a, b = [], []
        emitter.on("e", lambda: a.append(1))
        emitter.on("e", lambda: b.append(1))
        emitter.off("e")
        emitter.emit("e")
        assert a == []
        assert b == []

    def test_off_nonexistent_event(self, emitter):
        # Should not raise
        emitter.off("nonexistent")

    def test_chainable(self, emitter):
        result = emitter.off("e")
        assert result is emitter


class TestEventEmitterWildcard:
    def test_wildcard_receives_all(self, emitter):
        received = []
        emitter.on("*", lambda event, *args: received.append((event, args)))
        emitter.emit("foo", 1)
        emitter.emit("bar", 2)
        assert received == [("foo", (1,)), ("bar", (2,))]

    def test_wildcard_once(self, emitter):
        received = []
        emitter.once("*", lambda event, *args: received.append(event))
        emitter.emit("a")
        emitter.emit("b")
        assert received == ["a"]


class TestEventEmitterListenerCount:
    def test_count_zero(self, emitter):
        assert emitter.listener_count("none") == 0

    def test_count_multiple(self, emitter):
        emitter.on("e", lambda: None)
        emitter.on("e", lambda: None)
        assert emitter.listener_count("e") == 2

    def test_count_after_off(self, emitter):
        def fn():
            return None

        emitter.on("e", fn)
        emitter.off("e", fn)
        assert emitter.listener_count("e") == 0


class TestEventEmitterEmit:
    def test_emit_returns_self(self, emitter):
        result = emitter.emit("e")
        assert result is emitter

    def test_emit_no_listeners(self, emitter):
        # Should not raise
        emitter.emit("nonexistent", 1, 2, 3)
