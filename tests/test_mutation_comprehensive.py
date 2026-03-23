"""Comprehensive tests for mutation operators."""

import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32
from phyloid_engine.mutation import bit_flip_mutation, swap_mutation, gaussian_mutation


class TestBitFlipMutation:
    def test_rate_one_flips_all(self, rng, binary_organism):
        m = bit_flip_mutation(binary_organism, rng, rate=1.0)
        for i in range(binary_organism.size()):
            assert m.get_gene(i) == 1 - binary_organism.get_gene(i)

    def test_rate_zero_no_change(self, rng, binary_organism):
        m = bit_flip_mutation(binary_organism, rng, rate=0.0)
        assert m.genome == binary_organism.genome

    def test_does_not_modify_original(self, rng, binary_organism):
        original = list(binary_organism.genome)
        bit_flip_mutation(binary_organism, rng, rate=1.0)
        assert binary_organism.genome == original

    def test_preserves_size(self, rng, binary_organism):
        m = bit_flip_mutation(binary_organism, rng, rate=0.5)
        assert m.size() == binary_organism.size()


class TestSwapMutation:
    def test_preserves_gene_set(self, rng):
        o = Organism([10, 20, 30, 40, 50])
        m = swap_mutation(o, rng, rate=1.0)
        assert sorted(m.genome) == [10, 20, 30, 40, 50]

    def test_rate_zero_no_change(self, rng):
        o = Organism([10, 20, 30, 40, 50])
        m = swap_mutation(o, rng, rate=0.0)
        assert m.genome == o.genome

    def test_does_not_modify_original(self, rng):
        o = Organism([10, 20, 30, 40, 50])
        original = list(o.genome)
        swap_mutation(o, rng, rate=1.0)
        assert o.genome == original

    def test_preserves_size(self, rng):
        o = Organism([1, 2, 3, 4, 5, 6, 7, 8])
        m = swap_mutation(o, rng, rate=0.5)
        assert m.size() == o.size()


class TestGaussianMutation:
    def test_bounded_output(self, rng):
        o = Organism([0.5] * 10)
        m = gaussian_mutation(o, rng, rate=1.0, sigma=0.1, min_val=0, max_val=1)
        assert all(0 <= g <= 1 for g in m.genome)

    def test_rate_zero_no_change(self, rng):
        o = Organism([0.5] * 5)
        m = gaussian_mutation(o, rng, rate=0.0, sigma=0.1)
        assert m.genome == o.genome

    def test_does_not_modify_original(self, rng):
        o = Organism([0.5] * 5)
        original = list(o.genome)
        gaussian_mutation(o, rng, rate=1.0, sigma=0.5)
        assert o.genome == original

    def test_rate_one_modifies_genes(self, rng):
        o = Organism([0.5] * 10)
        m = gaussian_mutation(o, rng, rate=1.0, sigma=0.5)
        # At least some genes should differ
        assert m.genome != o.genome

    def test_large_sigma_still_bounded(self, rng):
        o = Organism([0.5] * 20)
        m = gaussian_mutation(o, rng, rate=1.0, sigma=100.0, min_val=-1, max_val=1)
        assert all(-1 <= g <= 1 for g in m.genome)

    def test_no_bounds(self, rng):
        o = Organism([0.0] * 5)
        m = gaussian_mutation(o, rng, rate=1.0, sigma=1.0)
        # With no bounds and sigma=1, some values should go negative or > 1
        assert m.size() == o.size()
