import sys

sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32
from phyloid_engine.mutation import bit_flip_mutation, swap_mutation, gaussian_mutation


def test_bit_flip_all():
    rng = Mulberry32(42)
    o = Organism([0, 0, 0, 0, 0])
    m = bit_flip_mutation(o, rng, rate=1.0)
    assert all(g == 1 for g in m.genome)


def test_swap_preserves_genes():
    rng = Mulberry32(42)
    o = Organism([10, 20, 30, 40, 50])
    m = swap_mutation(o, rng, rate=1.0)
    assert sorted(m.genome) == [10, 20, 30, 40, 50]


def test_gaussian_bounded():
    rng = Mulberry32(42)
    o = Organism([0.5, 0.5, 0.5, 0.5, 0.5])
    m = gaussian_mutation(o, rng, rate=1.0, sigma=0.1, min_val=0, max_val=1)
    assert all(0 <= g <= 1 for g in m.genome)
