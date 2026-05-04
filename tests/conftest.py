"""Shared fixtures and mock helpers for phyloid-engine test suite."""

import sys

sys.path.insert(0, "python")

import pytest
from phyloid_engine.prng import Mulberry32
from phyloid_engine.organism import Organism
from phyloid_engine.events import EventEmitter
from phyloid_engine.paradigm import ParadigmJudge, ParadigmPanel
from phyloid_engine.engine import EvolutionEngine


@pytest.fixture
def rng():
    """Deterministic PRNG seeded at 42."""
    return Mulberry32(42)


@pytest.fixture
def rng_alt():
    """Deterministic PRNG seeded at 99."""
    return Mulberry32(99)


@pytest.fixture
def sample_organism():
    """Organism with genome [0.1, 0.5, 0.9, 0.3, 0.7]."""
    return Organism([0.1, 0.5, 0.9, 0.3, 0.7], fitness=2.5)


@pytest.fixture
def binary_organism():
    """Organism with binary genome [0, 1, 0, 1, 1]."""
    return Organism([0, 1, 0, 1, 1])


@pytest.fixture
def sample_population():
    """Population of 5 organisms with varying fitness."""
    return [
        Organism([0.1], 10),
        Organism([0.2], 50),
        Organism([0.3], 30),
        Organism([0.4], 80),
        Organism([0.5], 20),
    ]


@pytest.fixture
def emitter():
    """Fresh EventEmitter instance."""
    return EventEmitter()


@pytest.fixture
def sum_judge():
    """ParadigmJudge that scores by genome sum."""
    return ParadigmJudge("sum", lambda o: sum(o.genome))


@pytest.fixture
def panel_with_judges():
    """ParadigmPanel with two weighted judges."""
    panel = ParadigmPanel()
    panel.add_judge(ParadigmJudge("sum", lambda o: sum(o.genome), weight=1.0))
    panel.add_judge(ParadigmJudge("max", lambda o: max(o.genome), weight=2.0))
    return panel


@pytest.fixture
def small_engine():
    """Small EvolutionEngine for quick tests."""
    return EvolutionEngine(
        {
            "population_size": 10,
            "genome_length": 4,
            "max_generations": 5,
            "seed": 42,
            "fitness_fn": lambda o: sum(o.genome),
        }
    )


def make_organisms(n, genome_len=5, fitness_fn=None):
    """Helper to create n organisms with optional fitness function."""
    rng = Mulberry32(42)
    orgs = []
    for _ in range(n):
        org = Organism.random(genome_len, rng)
        if fitness_fn:
            org.fitness = fitness_fn(org)
        orgs.append(org)
    return orgs
