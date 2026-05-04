#!/usr/bin/env python3
"""Custom genetic operators example.

Demonstrates:
- Using different selection, crossover, and mutation strategies
- Swapping operators via engine config
- Event-driven progress tracking with target fitness
"""

import sys

sys.path.insert(0, "python")

from phyloid_engine import (
    EvolutionEngine,
    roulette_selection,
    two_point_crossover,
    swap_mutation,
    Organism,
)


# Wrap roulette to accept tournament_size arg (engine always passes it)
def roulette_wrapper(pop, rng, _ts=3):
    return roulette_selection(pop, rng)


# Wrap swap_mutation to accept sigma/min/max args (engine always passes them)
def swap_wrapper(org, rng, rate=0.01, _sigma=0.1, _min=0, _max=1):
    return swap_mutation(org, rng, rate)


# Evolve toward a target pattern: [1, 0, 1, 0, 1, 0]
TARGET = [1, 0, 1, 0, 1, 0]


def pattern_fitness(o: Organism) -> float:
    """Score = number of genes matching the target pattern."""
    return sum(1 for a, b in zip(o.genome, TARGET) if abs(a - b) < 0.3)


engine = EvolutionEngine(
    {
        "population_size": 40,
        "genome_length": 6,
        "gene_min": 0,
        "gene_max": 1,
        "max_generations": 200,
        "target_fitness": 6,  # All 6 genes match
        "mutation_rate": 0.15,
        "seed": 123,
        "fitness_fn": pattern_fitness,
        "select_fn": roulette_wrapper,
        "crossover_fn": two_point_crossover,
        "mutate_fn": swap_wrapper,
    }
)

# Track progress
engine.on(
    "target_reached",
    lambda s: print(f"\n  Target reached at generation {s['generation']}!"),
)

print(f"Evolving toward target pattern: {TARGET}")
print("Operators: roulette selection, two-point crossover, swap mutation")
print("=" * 55)

result = engine.run()

best = result["best"]
print(f"\nResult after {result['generations']} generations:")
print(f"  Best fitness: {best.fitness}")
print(f"  Best genome:  [{', '.join(f'{g:.2f}' for g in best.genome)}]")
print(f"  Target:       [{', '.join(str(t) for t in TARGET)}]")
