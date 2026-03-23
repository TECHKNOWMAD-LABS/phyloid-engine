"""Tests for input validation and error hardening."""

import sys
sys.path.insert(0, "python")

import pytest
from phyloid_engine.prng import Mulberry32
from phyloid_engine.organism import Organism
from phyloid_engine.selection import (
    tournament_selection,
    roulette_selection,
    rank_selection,
)
from phyloid_engine.crossover import single_point_crossover, two_point_crossover
from phyloid_engine.engine import EvolutionEngine


class TestPrngValidation:
    def test_string_seed_raises(self):
        with pytest.raises(TypeError, match="seed must be a number"):
            Mulberry32("bad")

    def test_none_seed_raises(self):
        with pytest.raises(TypeError, match="seed must be a number"):
            Mulberry32(None)

    def test_list_seed_raises(self):
        with pytest.raises(TypeError, match="seed must be a number"):
            Mulberry32([1, 2])

    def test_float_seed_accepted(self):
        rng = Mulberry32(42.7)
        assert 0 <= rng.next() < 1

    def test_next_int_invalid_range(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="must be greater than"):
            rng.next_int(10, 5)

    def test_next_int_equal_range(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="must be greater than"):
            rng.next_int(5, 5)


class TestOrganismValidation:
    def test_get_gene_out_of_range(self):
        o = Organism([1, 2, 3])
        with pytest.raises(IndexError, match="out of range"):
            o.get_gene(5)

    def test_get_gene_negative(self):
        o = Organism([1, 2, 3])
        with pytest.raises(IndexError, match="out of range"):
            o.get_gene(-1)

    def test_set_gene_out_of_range(self):
        o = Organism([1, 2, 3])
        with pytest.raises(IndexError, match="out of range"):
            o.set_gene(10, 5.0)

    def test_from_dict_not_dict(self):
        with pytest.raises(TypeError, match="expected dict"):
            Organism.from_dict("bad")

    def test_from_dict_missing_genome(self):
        with pytest.raises(ValueError, match="must contain"):
            Organism.from_dict({"fitness": 5})

    def test_from_dict_missing_fitness(self):
        with pytest.raises(ValueError, match="must contain"):
            Organism.from_dict({"genome": [1, 2]})

    def test_random_negative_length(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="non-negative"):
            Organism.random(-1, rng)

    def test_random_inverted_bounds(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="gene_max"):
            Organism.random(5, rng, gene_min=10, gene_max=1)


class TestSelectionValidation:
    def test_tournament_empty_population(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="must not be empty"):
            tournament_selection([], rng)

    def test_tournament_invalid_size(self):
        rng = Mulberry32(42)
        pop = [Organism([1], 10)]
        with pytest.raises(ValueError, match="must be >= 1"):
            tournament_selection(pop, rng, 0)

    def test_roulette_empty_population(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="must not be empty"):
            roulette_selection([], rng)

    def test_rank_empty_population(self):
        rng = Mulberry32(42)
        with pytest.raises(ValueError, match="must not be empty"):
            rank_selection([], rng)


class TestCrossoverValidation:
    def test_single_point_too_short(self):
        rng = Mulberry32(42)
        a = Organism([1])
        b = Organism([2])
        with pytest.raises(ValueError, match="at least 2 genes"):
            single_point_crossover(a, b, rng)

    def test_two_point_too_short(self):
        rng = Mulberry32(42)
        a = Organism([1])
        b = Organism([2])
        with pytest.raises(ValueError, match="at least 2 genes"):
            two_point_crossover(a, b, rng)


class TestEngineValidation:
    def test_population_too_small(self):
        with pytest.raises(ValueError, match="population_size must be >= 2"):
            EvolutionEngine({"population_size": 1})

    def test_genome_too_short(self):
        with pytest.raises(ValueError, match="genome_length must be >= 2"):
            EvolutionEngine({"genome_length": 1})

    def test_elite_count_too_large(self):
        with pytest.raises(ValueError, match="elite_count must be less"):
            EvolutionEngine({"population_size": 10, "elite_count": 10})
