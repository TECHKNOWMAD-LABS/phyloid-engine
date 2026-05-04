"""Comprehensive tests for crossover operators."""

import sys

sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32
from phyloid_engine.crossover import (
    single_point_crossover,
    two_point_crossover,
    uniform_crossover,
)


class TestSinglePointCrossover:
    def test_produces_two_children(self, rng):
        a = Organism([1, 1, 1, 1, 1])
        b = Organism([2, 2, 2, 2, 2])
        c1, c2 = single_point_crossover(a, b, rng)
        assert c1.size() == 5
        assert c2.size() == 5

    def test_children_have_parent_genes(self, rng):
        a = Organism([1, 1, 1, 1, 1])
        b = Organism([2, 2, 2, 2, 2])
        c1, c2 = single_point_crossover(a, b, rng)
        for g in c1.genome:
            assert g in (1, 2)
        for g in c2.genome:
            assert g in (1, 2)

    def test_does_not_modify_parents(self, rng):
        a = Organism([1, 2, 3, 4, 5])
        b = Organism([6, 7, 8, 9, 10])
        a_orig = list(a.genome)
        b_orig = list(b.genome)
        single_point_crossover(a, b, rng)
        assert a.genome == a_orig
        assert b.genome == b_orig

    def test_deterministic(self):
        a = Organism([1, 1, 1, 1, 1])
        b = Organism([2, 2, 2, 2, 2])
        c1a, c2a = single_point_crossover(a, b, Mulberry32(42))
        c1b, c2b = single_point_crossover(a, b, Mulberry32(42))
        assert c1a.genome == c1b.genome
        assert c2a.genome == c2b.genome

    def test_different_length_parents(self, rng):
        a = Organism([1, 1, 1, 1, 1, 1])
        b = Organism([2, 2, 2])
        c1, c2 = single_point_crossover(a, b, rng)
        # Uses min length
        assert c1.size() >= 3


class TestTwoPointCrossover:
    def test_produces_correct_length(self, rng):
        a = Organism([1, 2, 3, 4, 5, 6])
        b = Organism([10, 20, 30, 40, 50, 60])
        c1, c2 = two_point_crossover(a, b, rng)
        assert c1.size() == 6
        assert c2.size() == 6

    def test_children_have_parent_genes(self, rng):
        a = Organism([1, 1, 1, 1, 1])
        b = Organism([2, 2, 2, 2, 2])
        c1, c2 = two_point_crossover(a, b, rng)
        for g in c1.genome:
            assert g in (1, 2)

    def test_does_not_modify_parents(self, rng):
        a = Organism([1, 2, 3, 4, 5])
        b = Organism([6, 7, 8, 9, 10])
        a_orig = list(a.genome)
        b_orig = list(b.genome)
        two_point_crossover(a, b, rng)
        assert a.genome == a_orig
        assert b.genome == b_orig


class TestUniformCrossover:
    def test_preserves_length(self, rng):
        a = Organism([1, 2, 3, 4])
        b = Organism([5, 6, 7, 8])
        c1, c2 = uniform_crossover(a, b, rng)
        assert c1.size() == 4
        assert c2.size() == 4

    def test_swap_prob_zero_copies_parents(self, rng):
        a = Organism([1, 2, 3, 4])
        b = Organism([5, 6, 7, 8])
        c1, c2 = uniform_crossover(a, b, rng, swap_prob=0.0)
        assert c1.genome == [1, 2, 3, 4]
        assert c2.genome == [5, 6, 7, 8]

    def test_swap_prob_one_swaps_all(self, rng):
        a = Organism([1, 2, 3, 4])
        b = Organism([5, 6, 7, 8])
        c1, c2 = uniform_crossover(a, b, rng, swap_prob=1.0)
        assert c1.genome == [5, 6, 7, 8]
        assert c2.genome == [1, 2, 3, 4]

    def test_does_not_modify_parents(self, rng):
        a = Organism([1, 2, 3, 4])
        b = Organism([5, 6, 7, 8])
        a_orig = list(a.genome)
        b_orig = list(b.genome)
        uniform_crossover(a, b, rng, swap_prob=0.5)
        assert a.genome == a_orig
        assert b.genome == b_orig

    def test_gene_conservation(self, rng):
        """Each gene position should contain a gene from one parent or the other."""
        a = Organism([1, 2, 3, 4, 5])
        b = Organism([6, 7, 8, 9, 10])
        c1, c2 = uniform_crossover(a, b, rng)
        for i in range(5):
            assert c1.genome[i] in (a.genome[i], b.genome[i])
            assert c2.genome[i] in (a.genome[i], b.genome[i])
