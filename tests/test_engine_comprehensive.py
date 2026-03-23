"""Comprehensive tests for EvolutionEngine."""

import sys
sys.path.insert(0, "python")

from phyloid_engine.engine import EvolutionEngine, DEFAULTS
from phyloid_engine.paradigm import ParadigmJudge
from phyloid_engine.organism import Organism
from phyloid_engine.selection import roulette_selection, rank_selection
from phyloid_engine.crossover import two_point_crossover, uniform_crossover
from phyloid_engine.mutation import bit_flip_mutation, swap_mutation


class TestEngineDefaults:
    def test_defaults_exist(self):
        assert DEFAULTS["population_size"] == 100
        assert DEFAULTS["genome_length"] == 10
        assert DEFAULTS["seed"] == 42
        assert DEFAULTS["max_generations"] == 100

    def test_default_config_applied(self):
        engine = EvolutionEngine()
        assert engine.config["population_size"] == 100
        assert engine.config["seed"] == 42


class TestEngineInitialize:
    def test_creates_population(self, small_engine):
        small_engine.initialize()
        assert len(small_engine.population) == 10
        assert all(o.size() == 4 for o in small_engine.population)

    def test_evaluates_fitness(self, small_engine):
        small_engine.initialize()
        assert all(o.fitness > 0 for o in small_engine.population)

    def test_sets_best_organism(self, small_engine):
        small_engine.initialize()
        assert small_engine.best_organism is not None

    def test_emits_initialized_event(self, small_engine):
        received = []
        small_engine.on("initialized", lambda d: received.append(d))
        small_engine.initialize()
        assert len(received) == 1
        assert "population" in received[0]

    def test_generation_starts_at_zero(self, small_engine):
        small_engine.initialize()
        assert small_engine.generation == 0


class TestEngineStep:
    def test_advances_generation(self, small_engine):
        small_engine.initialize()
        stats = small_engine.step()
        assert small_engine.generation == 1
        assert stats["generation"] == 1

    def test_maintains_population_size(self, small_engine):
        small_engine.initialize()
        small_engine.step()
        assert len(small_engine.population) == 10

    def test_stats_contain_expected_keys(self, small_engine):
        small_engine.initialize()
        stats = small_engine.step()
        assert "generation" in stats
        assert "best" in stats
        assert "worst" in stats
        assert "average" in stats
        assert "best_organism" in stats

    def test_emits_generation_event(self, small_engine):
        received = []
        small_engine.on("generation", lambda d: received.append(d))
        small_engine.initialize()
        small_engine.step()
        assert len(received) == 1
        assert received[0]["generation"] == 1


class TestEngineRun:
    def test_completes_all_generations(self, small_engine):
        result = small_engine.run()
        assert result["generations"] == 5

    def test_returns_best_organism(self, small_engine):
        result = small_engine.run()
        assert isinstance(result["best"], Organism)

    def test_auto_initializes(self):
        engine = EvolutionEngine({
            "population_size": 10,
            "genome_length": 4,
            "max_generations": 3,
            "seed": 42,
            "fitness_fn": lambda o: sum(o.genome),
        })
        result = engine.run()
        assert result["generations"] == 3

    def test_stops_at_target_fitness(self):
        engine = EvolutionEngine({
            "population_size": 20,
            "genome_length": 4,
            "max_generations": 1000,
            "seed": 42,
            "target_fitness": 0.01,  # Very low target, should hit quickly
            "fitness_fn": lambda o: sum(o.genome),
        })
        result = engine.run()
        assert result["generations"] < 1000

    def test_emits_started_and_completed(self):
        engine = EvolutionEngine({
            "population_size": 10,
            "genome_length": 4,
            "max_generations": 2,
            "seed": 42,
            "fitness_fn": lambda o: sum(o.genome),
        })
        events = []
        engine.on("started", lambda d: events.append("started"))
        engine.on("completed", lambda d: events.append("completed"))
        engine.run()
        assert "started" in events
        assert "completed" in events

    def test_stats_history_length(self, small_engine):
        result = small_engine.run()
        assert len(result["stats"]["generation_history"]) == 5


class TestEngineDeterminism:
    def test_same_seed_same_result(self):
        cfg = {
            "population_size": 10,
            "genome_length": 4,
            "max_generations": 5,
            "seed": 99,
            "fitness_fn": lambda o: sum(o.genome),
        }
        r1 = EvolutionEngine(cfg).run()
        r2 = EvolutionEngine(cfg).run()
        assert r1["best"].fitness == r2["best"].fitness
        assert r1["best"].genome == r2["best"].genome

    def test_different_seed_different_result(self):
        base = {
            "population_size": 10,
            "genome_length": 4,
            "max_generations": 10,
            "fitness_fn": lambda o: sum(o.genome),
        }
        r1 = EvolutionEngine({**base, "seed": 1}).run()
        r2 = EvolutionEngine({**base, "seed": 2}).run()
        # Very unlikely to be identical with different seeds
        assert r1["best"].genome != r2["best"].genome


class TestEngineCustomFunctions:
    def test_custom_selection(self):
        # roulette_selection doesn't take tournament_size, so wrap it
        def roulette_wrapper(pop, rng, _tournament_size=3):
            return roulette_selection(pop, rng)

        engine = EvolutionEngine({
            "population_size": 10,
            "genome_length": 4,
            "max_generations": 3,
            "seed": 42,
            "fitness_fn": lambda o: sum(o.genome),
            "select_fn": roulette_wrapper,
        })
        result = engine.run()
        assert result["generations"] == 3

    def test_custom_crossover(self):
        engine = EvolutionEngine({
            "population_size": 10,
            "genome_length": 6,
            "max_generations": 3,
            "seed": 42,
            "fitness_fn": lambda o: sum(o.genome),
            "crossover_fn": two_point_crossover,
        })
        result = engine.run()
        assert result["generations"] == 3


class TestEngineParadigm:
    def test_paradigm_panel_integration(self):
        engine = EvolutionEngine({
            "population_size": 10,
            "genome_length": 3,
            "max_generations": 3,
            "seed": 42,
        })
        engine.panel.add_judge(ParadigmJudge("sum", lambda o: sum(o.genome)))
        result = engine.run()
        assert result["best"].fitness > 0

    def test_multi_judge_panel(self):
        engine = EvolutionEngine({
            "population_size": 10,
            "genome_length": 3,
            "max_generations": 3,
            "seed": 42,
        })
        engine.panel.add_judge(ParadigmJudge("sum", lambda o: sum(o.genome), weight=1))
        engine.panel.add_judge(ParadigmJudge("max", lambda o: max(o.genome), weight=2))
        result = engine.run()
        assert result["best"].fitness > 0
        assert "paradigm_scores" in result["best"].meta
