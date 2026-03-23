#!/usr/bin/env python3
"""Basic evolution example — maximize the sum of genome values.

Demonstrates:
- Creating an EvolutionEngine with a fitness function
- Running evolution for a fixed number of generations
- Accessing the best organism and stats
"""

import sys
sys.path.insert(0, "python")

from phyloid_engine import EvolutionEngine

# Configure a simple evolution run
engine = EvolutionEngine({
    "population_size": 50,
    "genome_length": 10,
    "gene_min": 0,
    "gene_max": 1,
    "max_generations": 100,
    "mutation_rate": 0.05,
    "mutation_sigma": 0.1,
    "seed": 42,
    "fitness_fn": lambda o: sum(o.genome),  # Maximize sum
})

# Subscribe to events
engine.on("generation", lambda data: (
    print(f"  Gen {data['generation']:3d}: best={data['stats']['best']:.4f}  avg={data['stats']['average']:.4f}")
    if data["generation"] % 10 == 0 else None
))

print("Starting evolution — maximizing sum of 10 genes in [0, 1]")
print("=" * 55)

result = engine.run()

print("=" * 55)
print(f"Completed in {result['generations']} generations")
print(f"Best fitness: {result['best'].fitness:.4f}")
print(f"Best genome:  [{', '.join(f'{g:.3f}' for g in result['best'].genome)}]")
print(f"Theoretical max: 10.0")
