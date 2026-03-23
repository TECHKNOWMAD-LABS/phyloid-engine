#!/usr/bin/env python3
"""Multi-objective optimization using ParadigmPanel.

Demonstrates:
- Creating multiple ParadigmJudge instances with different weights
- Using ParadigmPanel for weighted multi-objective fitness
- Inspecting per-judge scores in organism metadata
"""

import sys
sys.path.insert(0, "python")

from phyloid_engine import EvolutionEngine, ParadigmJudge

# Create engine without a direct fitness_fn — panel judges provide fitness
engine = EvolutionEngine({
    "population_size": 80,
    "genome_length": 8,
    "gene_min": 0,
    "gene_max": 1,
    "max_generations": 50,
    "seed": 7,
})

# Objective 1: maximize sum (weight=1)
engine.panel.add_judge(ParadigmJudge(
    "sum",
    lambda o: sum(o.genome),
    weight=1.0,
))

# Objective 2: minimize variance — penalize spread (weight=2)
def low_variance(o):
    avg = sum(o.genome) / len(o.genome)
    variance = sum((g - avg) ** 2 for g in o.genome) / len(o.genome)
    return 1.0 / (1.0 + variance)  # Higher is better

engine.panel.add_judge(ParadigmJudge("uniformity", low_variance, weight=2.0))

print("Multi-objective evolution: maximize sum + minimize variance")
print(f"Judges: sum (weight=1.0), uniformity (weight=2.0)")
print("=" * 60)

result = engine.run()

best = result["best"]
scores = best.meta.get("paradigm_scores", {})
print(f"\nBest organism after {result['generations']} generations:")
print(f"  Aggregate fitness: {best.fitness:.4f}")
print(f"  Sum score:         {scores.get('sum', 'N/A'):.4f}")
print(f"  Uniformity score:  {scores.get('uniformity', 'N/A'):.4f}")
print(f"  Genome: [{', '.join(f'{g:.3f}' for g in best.genome)}]")
