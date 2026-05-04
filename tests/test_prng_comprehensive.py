"""Comprehensive tests for Mulberry32 PRNG."""

import sys

sys.path.insert(0, "python")

from phyloid_engine.prng import Mulberry32, _to_u32, _to_i32, _imul


class TestMulberry32:
    def test_deterministic_same_seed(self, rng):
        rng2 = Mulberry32(42)
        for _ in range(100):
            assert rng.next() == rng2.next()

    def test_different_seeds_differ(self):
        a = Mulberry32(1)
        b = Mulberry32(2)
        results_a = [a.next() for _ in range(10)]
        results_b = [b.next() for _ in range(10)]
        assert results_a != results_b

    def test_values_in_unit_range(self, rng):
        for _ in range(5000):
            v = rng.next()
            assert 0.0 <= v < 1.0

    def test_next_int_bounds(self, rng):
        for _ in range(1000):
            v = rng.next_int(5, 15)
            assert 5 <= v < 15

    def test_next_int_single_value_range(self, rng):
        # When min == max-1, only one possible value
        for _ in range(10):
            assert rng.next_int(7, 8) == 7

    def test_next_int_negative_range(self, rng):
        for _ in range(100):
            v = rng.next_int(-10, 0)
            assert -10 <= v < 0

    def test_reset_restores_sequence(self, rng):
        first = [rng.next() for _ in range(20)]
        rng.reset()
        second = [rng.next() for _ in range(20)]
        assert first == second

    def test_seed_property(self):
        rng = Mulberry32(12345)
        assert rng.seed == 12345

    def test_seed_zero(self):
        rng = Mulberry32(0)
        v = rng.next()
        assert 0.0 <= v < 1.0

    def test_seed_max_u32(self):
        rng = Mulberry32(0xFFFFFFFF)
        v = rng.next()
        assert 0.0 <= v < 1.0

    def test_large_seed_wraps(self):
        rng = Mulberry32(0x100000000)  # Should wrap to 0
        rng0 = Mulberry32(0)
        assert rng.next() == rng0.next()

    def test_distribution_not_degenerate(self, rng):
        """Values should spread across [0,1), not cluster."""
        values = [rng.next() for _ in range(1000)]
        buckets = [0] * 10
        for v in values:
            buckets[int(v * 10)] += 1
        # Each bucket should have at least some values
        assert all(b > 30 for b in buckets)

    def test_next_int_uses_full_range(self, rng):
        seen = set()
        for _ in range(200):
            seen.add(rng.next_int(0, 5))
        assert seen == {0, 1, 2, 3, 4}


class TestInternalHelpers:
    def test_to_u32(self):
        assert _to_u32(0) == 0
        assert _to_u32(0xFFFFFFFF) == 0xFFFFFFFF
        assert _to_u32(0x100000000) == 0
        assert _to_u32(-1) == 0xFFFFFFFF

    def test_to_i32(self):
        assert _to_i32(0) == 0
        assert _to_i32(0x7FFFFFFF) == 0x7FFFFFFF
        assert _to_i32(0x80000000) == -2147483648
        assert _to_i32(0xFFFFFFFF) == -1

    def test_imul(self):
        assert _imul(2, 3) == 6
        assert _imul(0, 100) == 0
        assert _imul(0xFFFFFFFF, 0xFFFFFFFF) == 1  # (-1)*(-1)
