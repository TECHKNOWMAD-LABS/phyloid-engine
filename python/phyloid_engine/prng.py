"""Mulberry32 seeded PRNG — deterministic, identical output in JS and Python."""

import math

_MASK = 0xFFFFFFFF


def _to_u32(x: int) -> int:
    return x & _MASK


def _to_i32(x: int) -> int:
    x = x & _MASK
    return x - 0x100000000 if x >= 0x80000000 else x


def _imul(a: int, b: int) -> int:
    """Emulate Math.imul — 32-bit integer multiply."""
    a, b = _to_i32(a), _to_i32(b)
    result = (a * b) & _MASK
    return _to_i32(result)


class Mulberry32:
    def __init__(self, seed: int) -> None:
        self._initial = _to_u32(seed)
        self._state = self._initial

    def next(self) -> float:
        self._state = _to_u32(self._state + 0x6D2B79F5)
        t = _to_i32(self._state)
        t = _imul(t ^ _to_i32(_to_u32(t) >> 15), _to_i32(1 | _to_u32(t)))
        t = _to_i32(_to_u32(_to_i32(_to_u32(t) + _to_u32(_imul(
            _to_i32(_to_u32(t) ^ _to_i32(_to_u32(t) >> 7)),
            _to_i32(61 | _to_u32(t))
        )))) ^ _to_u32(t))
        return _to_u32(t ^ _to_i32(_to_u32(t) >> 14)) / 4294967296

    def next_int(self, min_val: int, max_val: int) -> int:
        return min_val + math.floor(self.next() * (max_val - min_val))

    def reset(self) -> None:
        self._state = self._initial

    @property
    def seed(self) -> int:
        return self._initial
