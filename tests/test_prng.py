import sys

sys.path.insert(0, "python")

from phyloid_engine.prng import Mulberry32


def test_deterministic_output():
    a = Mulberry32(42)
    b = Mulberry32(42)
    for _ in range(20):
        assert a.next() == b.next()


def test_values_in_range():
    rng = Mulberry32(123)
    for _ in range(1000):
        v = rng.next()
        assert 0 <= v < 1


def test_reset():
    rng = Mulberry32(99)
    first = [rng.next() for _ in range(3)]
    rng.reset()
    second = [rng.next() for _ in range(3)]
    assert first == second
