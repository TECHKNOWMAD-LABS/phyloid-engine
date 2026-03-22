# phyloid-engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776ab.svg)](https://www.python.org/downloads/release/python-3120/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

PEP-003 genetic algorithm framework with dual implementations in Python 3.12 and Node.js 22. Supports organism selection, crossover, mutation, and paradigm-based fitness evaluation.

## Features

- **Dual runtime**: identical API surface in Python 3.12 (snake_case) and Node.js 22
- **Selection strategies**: tournament, roulette wheel, rank-based, and elitist selection
- **Crossover operators**: single-point, two-point, and uniform crossover
- **Mutation operators**: bit-flip, swap, and gaussian mutation
- **Paradigm judges**: composable `ParadigmJudge` and `ParadigmPanel` for multi-objective fitness evaluation
- **Seeded PRNG**: Mulberry32 generator for fully reproducible evolution runs

## Quick Start

### Python

```python
from phyloid_engine import EvolutionEngine, Organism, ParadigmJudge

def fitness(genome: list[float]) -> float:
    return -sum((x - 0.5) ** 2 for x in genome)

judge = ParadigmJudge(fitness)
engine = EvolutionEngine(
    population_size=100,
    genome_length=10,
    judge=judge,
    mutation_rate=0.01,
    seed=42,
)

result = engine.run(generations=200)
print(result.best.fitness)
```

### Node.js

```js
import { EvolutionEngine, ParadigmJudge } from 'phyloid-engine';

const judge = new ParadigmJudge(genome =>
  -genome.reduce((s, x) => s + (x - 0.5) ** 2, 0)
);

const engine = new EvolutionEngine({
  populationSize: 100,
  genomeLength: 10,
  judge,
  mutationRate: 0.01,
  seed: 42,
});

const result = await engine.run({ generations: 200 });
console.log(result.best.fitness);
```

## Installation

**Python**

```bash
pip install phyloid-engine
```

**Node.js**

```bash
npm install phyloid-engine
```

## Architecture

```
phyloid-engine
├── EvolutionEngine      # orchestrates the GA loop
│   ├── Selection        # tournament | roulette | rank | elite
│   ├── Crossover        # single-point | two-point | uniform
│   ├── Mutation         # bit-flip | swap | gaussian
│   └── PRNG             # Mulberry32 seeded random
├── Organism             # genome + cached fitness score
└── Paradigm
    ├── ParadigmJudge    # single-objective fitness function wrapper
    └── ParadigmPanel    # weighted aggregate of multiple judges
```

Each generation follows the canonical GA cycle:

1. **Evaluate** — score all organisms via the paradigm
2. **Select** — choose parents by the configured strategy
3. **Crossover** — recombine parent genomes
4. **Mutate** — apply stochastic perturbations
5. **Replace** — form the next generation
6. **Emit** — fire lifecycle events for observability

Events (`generation`, `convergence`, `stagnation`) are emitted at each stage and can be subscribed to for logging, early stopping, or checkpointing.

## Testing

```bash
# Python
pytest

# Node.js
npm test
```

Both suites run 8 test modules covering every public API. No external test dependencies beyond `pytest`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch conventions, coding standards, and the pull-request checklist.

## License

[MIT](LICENSE)

---

Built by [TechKnowMad Labs](https://techknowmad.ai)
