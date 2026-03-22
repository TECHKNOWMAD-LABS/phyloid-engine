import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32


def test_construct():
    o = Organism([1, 2, 3], 5)
    assert o.genome == [1, 2, 3]
    assert o.fitness == 5


def test_clone_independent():
    o = Organism([1, 2, 3], 10)
    c = o.clone()
    c.genome[0] = 99
    assert o.genome[0] == 1


def test_random():
    rng = Mulberry32(42)
    o = Organism.random(8, rng, 0, 10)
    assert o.size() == 8
    assert all(0 <= g <= 10 for g in o.genome)
