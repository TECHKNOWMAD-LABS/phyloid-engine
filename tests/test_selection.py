import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32
from phyloid_engine.selection import (
    tournament_selection,
    roulette_selection,
    rank_selection,
    elite_selection,
)


def _make_pop():
    return [
        Organism([1], 10),
        Organism([2], 50),
        Organism([3], 30),
        Organism([4], 80),
        Organism([5], 20),
    ]


def test_tournament():
    rng = Mulberry32(42)
    pop = _make_pop()
    sel = tournament_selection(pop, rng, 3)
    assert sel in pop


def test_roulette():
    rng = Mulberry32(42)
    pop = _make_pop()
    sel = roulette_selection(pop, rng)
    assert sel in pop


def test_elite():
    pop = _make_pop()
    elites = elite_selection(pop, 2)
    assert len(elites) == 2
    assert elites[0].fitness == 80
    assert elites[1].fitness == 50
