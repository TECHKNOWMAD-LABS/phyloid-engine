from __future__ import annotations

from typing import Any, Callable


class EventEmitter:
    """Pub/sub event bus with wildcard support and chainable API."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = {}
        self._once: set[Callable[..., Any]] = set()

    def on(self, event: str, fn: Callable[..., Any]) -> EventEmitter:
        self._listeners.setdefault(event, []).append(fn)
        return self

    def once(self, event: str, fn: Callable[..., Any]) -> EventEmitter:
        self._once.add(fn)
        return self.on(event, fn)

    def off(self, event: str, fn: Callable[..., Any] | None = None) -> EventEmitter:
        if event not in self._listeners:
            return self
        if fn:
            self._listeners[event] = [f for f in self._listeners[event] if f is not fn]
        else:
            del self._listeners[event]
        return self

    def emit(self, event: str, *args: Any) -> EventEmitter:
        fns = list(self._listeners.get(event, []))
        wildcard = list(self._listeners.get("*", []))
        for fn in fns:
            fn(*args)
            if fn in self._once:
                self.off(event, fn)
                self._once.discard(fn)
        for fn in wildcard:
            fn(event, *args)
            if fn in self._once:
                self.off("*", fn)
                self._once.discard(fn)
        return self

    def listener_count(self, event: str) -> int:
        return len(self._listeners.get(event, []))
