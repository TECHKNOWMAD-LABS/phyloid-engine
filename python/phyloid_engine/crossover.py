from __future__ import annotations

from .organism import Organism
from .prng import Mulberry32


def single_point_crossover(
    parent_a: Organism, parent_b: Organism, rng: Mulberry32
) -> tuple[Organism, Organism]:
    """Split genomes at a random point and swap tails. Returns two children."""
    length = min(parent_a.size(), parent_b.size())
    if length < 2:
        raise ValueError(
            f"parents must have at least 2 genes for crossover, got {length}"
        )
    point = rng.next_int(1, length)
    child_a = Organism(parent_a.genome[:point] + parent_b.genome[point:])
    child_b = Organism(parent_b.genome[:point] + parent_a.genome[point:])
    return child_a, child_b


def two_point_crossover(
    parent_a: Organism, parent_b: Organism, rng: Mulberry32
) -> tuple[Organism, Organism]:
    """Swap the middle segment between two random points. Returns two children."""
    length = min(parent_a.size(), parent_b.size())
    if length < 2:
        raise ValueError(
            f"parents must have at least 2 genes for crossover, got {length}"
        )
    p1 = rng.next_int(1, length)
    p2 = rng.next_int(1, length)
    if p1 > p2:
        p1, p2 = p2, p1
    if p1 == p2:
        p2 = min(p2 + 1, length)
    child_a = Organism(
        parent_a.genome[:p1] + parent_b.genome[p1:p2] + parent_a.genome[p2:]
    )
    child_b = Organism(
        parent_b.genome[:p1] + parent_a.genome[p1:p2] + parent_b.genome[p2:]
    )
    return child_a, child_b


def uniform_crossover(
    parent_a: Organism, parent_b: Organism, rng: Mulberry32, swap_prob: float = 0.5
) -> tuple[Organism, Organism]:
    """Swap each gene independently with the given probability. Returns two children."""
    length = min(parent_a.size(), parent_b.size())
    genome_a: list[float] = []
    genome_b: list[float] = []
    for i in range(length):
        if rng.next() < swap_prob:
            genome_a.append(parent_b.genome[i])
            genome_b.append(parent_a.genome[i])
        else:
            genome_a.append(parent_a.genome[i])
            genome_b.append(parent_b.genome[i])
    return Organism(genome_a), Organism(genome_b)
