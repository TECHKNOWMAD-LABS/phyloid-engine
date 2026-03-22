import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32
from phyloid_engine.crossover import (
    single_point_crossover,
    two_point_crossover,
    uniform_crossover,
)


def test_single_point():
    rng = Mulberry32(42)
    a = Organism([1, 1, 1, 1, 1])
    b = Organism([2, 2, 2, 2, 2])
    c1, c2 = single_point_crossover(a, b, rng)
    assert c1.size() == 5
    assert c2.size() == 5


def test_two_point():
    rng = Mulberry32(7)
    a = Organism([1, 2, 3, 4, 5, 6])
    b = Organism([10, 20, 30, 40, 50, 60])
    c1, c2 = two_point_crossover(a, b, rng)
    assert c1.size() == 6
    assert c2.size() == 6


def test_uniform_preserves_length():
    rng = Mulberry32(42)
    a = Organism([1, 2, 3, 4])
    b = Organism([5, 6, 7, 8])
    c1, c2 = uniform_crossover(a, b, rng)
    assert c1.size() == 4
    assert c2.size() == 4
