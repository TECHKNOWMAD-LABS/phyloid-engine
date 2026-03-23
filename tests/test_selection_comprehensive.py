"""Comprehensive tests for selection strategies."""

import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32
from phyloid_engine.selection import (
    tournament_selection,
    roulette_selection,
    rank_selection,
    elite_selection,
)


class TestTournamentSelection:
    def test_returns_from_population(self, rng, sample_population):
        sel = tournament_selection(sample_population, rng, 3)
        assert sel in sample_population

    def test_full_tournament_returns_best(self, rng, sample_population):
        sel = tournament_selection(sample_population, rng, len(sample_population))
        assert sel.fitness == 80

    def test_tournament_size_1(self, rng, sample_population):
        sel = tournament_selection(sample_population, rng, 1)
        assert sel in sample_population

    def test_deterministic(self, sample_population):
        r1 = tournament_selection(sample_population, Mulberry32(42), 3)
        r2 = tournament_selection(sample_population, Mulberry32(42), 3)
        assert r1.fitness == r2.fitness

    def test_prefers_fitter(self, sample_population):
        rng = Mulberry32(42)
        counts = {}
        for _ in range(500):
            sel = tournament_selection(sample_population, rng, 3)
            counts[sel.fitness] = counts.get(sel.fitness, 0) + 1
        # Fittest (80) should be selected most often
        assert counts.get(80, 0) > counts.get(10, 0)


class TestRouletteSelection:
    def test_returns_from_population(self, rng, sample_population):
        sel = roulette_selection(sample_population, rng)
        assert sel in sample_population

    def test_handles_negative_fitness(self, rng):
        pop = [Organism([1], -5), Organism([2], -10), Organism([3], 5)]
        sel = roulette_selection(pop, rng)
        assert sel in pop

    def test_handles_zero_fitness(self, rng):
        pop = [Organism([1], 0), Organism([2], 0), Organism([3], 0)]
        sel = roulette_selection(pop, rng)
        assert sel in pop

    def test_single_organism(self, rng):
        pop = [Organism([1], 10)]
        sel = roulette_selection(pop, rng)
        assert sel is pop[0]


class TestRankSelection:
    def test_returns_from_population(self, rng, sample_population):
        sel = rank_selection(sample_population, rng)
        assert sel in sample_population

    def test_prefers_higher_ranked(self, sample_population):
        rng = Mulberry32(42)
        counts = {}
        for _ in range(500):
            sel = rank_selection(sample_population, rng)
            counts[sel.fitness] = counts.get(sel.fitness, 0) + 1
        assert counts.get(80, 0) > counts.get(10, 0)


class TestEliteSelection:
    def test_returns_top_n(self, sample_population):
        elites = elite_selection(sample_population, 2)
        assert len(elites) == 2
        assert elites[0].fitness == 80
        assert elites[1].fitness == 50

    def test_count_exceeds_population(self, sample_population):
        elites = elite_selection(sample_population, 100)
        assert len(elites) == len(sample_population)

    def test_single_elite(self, sample_population):
        elites = elite_selection(sample_population, 1)
        assert len(elites) == 1
        assert elites[0].fitness == 80

    def test_zero_elites(self, sample_population):
        elites = elite_selection(sample_population, 0)
        assert elites == []

    def test_preserves_order(self):
        pop = [Organism([i], i * 10) for i in range(10)]
        elites = elite_selection(pop, 5)
        fitnesses = [e.fitness for e in elites]
        assert fitnesses == sorted(fitnesses, reverse=True)
