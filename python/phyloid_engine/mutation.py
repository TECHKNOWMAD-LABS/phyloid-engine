from __future__ import annotations

import math

from .organism import Organism
from .prng import Mulberry32


def bit_flip_mutation(
    organism: Organism, rng: Mulberry32, rate: float = 0.01
) -> Organism:
    """Flip each gene (1-x) with the given probability. Returns a new organism."""
    child = organism.clone()
    for i in range(child.size()):
        if rng.next() < rate:
            child.set_gene(i, 1 - child.get_gene(i))
    return child


def swap_mutation(organism: Organism, rng: Mulberry32, rate: float = 0.01) -> Organism:
    """Swap pairs of genes with the given probability. Returns a new organism."""
    child = organism.clone()
    for i in range(child.size()):
        if rng.next() < rate:
            j = rng.next_int(0, child.size())
            tmp = child.get_gene(i)
            child.set_gene(i, child.get_gene(j))
            child.set_gene(j, tmp)
    return child


def gaussian_mutation(
    organism: Organism,
    rng: Mulberry32,
    rate: float = 0.01,
    sigma: float = 0.1,
    min_val: float = float("-inf"),
    max_val: float = float("inf"),
) -> Organism:
    """Add Gaussian noise to genes, clamped to [min_val, max_val]. Returns a new organism."""
    child = organism.clone()
    for i in range(child.size()):
        if rng.next() < rate:
            u1 = rng.next() or 1e-10
            u2 = rng.next()
            z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            value = child.get_gene(i) + z * sigma
            value = max(min_val, min(max_val, value))
            child.set_gene(i, value)
    return child
