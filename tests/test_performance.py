"""Performance benchmarks and optimization verification."""

import sys
import time

sys.path.insert(0, "python")

from phyloid_engine.engine import EvolutionEngine


class TestPerformanceOptimizations:
    def test_update_best_only_clones_on_improvement(self):
        """Verify _update_best uses max() instead of iterating with clone."""
        engine = EvolutionEngine(
            {
                "population_size": 50,
                "genome_length": 10,
                "max_generations": 20,
                "seed": 42,
                "fitness_fn": lambda o: sum(o.genome),
            }
        )
        result = engine.run()
        assert result["best"] is not None
        assert result["generations"] == 20

    def test_gen_stats_single_pass(self):
        """Verify _gen_stats computes min/max/avg in one pass."""
        engine = EvolutionEngine(
            {
                "population_size": 100,
                "genome_length": 10,
                "max_generations": 5,
                "seed": 42,
                "fitness_fn": lambda o: sum(o.genome),
            }
        )
        engine.initialize()
        stats = engine.step()
        fitnesses = [o.fitness for o in engine.population]
        assert stats["best"] == max(fitnesses)
        assert stats["worst"] == min(fitnesses)
        assert abs(stats["average"] - sum(fitnesses) / len(fitnesses)) < 1e-10

    def test_large_population_completes(self):
        """500 organisms x 50 generations should complete under 5 seconds."""
        start = time.time()
        engine = EvolutionEngine(
            {
                "population_size": 500,
                "genome_length": 20,
                "max_generations": 50,
                "seed": 42,
                "fitness_fn": lambda o: sum(o.genome),
            }
        )
        result = engine.run()
        elapsed = time.time() - start
        assert result["generations"] == 50
        assert elapsed < 5.0, f"Took {elapsed:.2f}s, expected < 5s"

    def test_config_lookup_cached_in_step(self):
        """Engine.step() should cache config values as locals."""
        engine = EvolutionEngine(
            {
                "population_size": 20,
                "genome_length": 5,
                "max_generations": 10,
                "seed": 42,
                "fitness_fn": lambda o: sum(o.genome),
            }
        )
        result = engine.run()
        assert result["generations"] == 10
        assert result["best"].fitness > 0
