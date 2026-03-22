from __future__ import annotations

from .organism import Organism
from .prng import Mulberry32


def tournament_selection(
    population: list[Organism], rng: Mulberry32, tournament_size: int = 3
) -> Organism:
    best: Organism | None = None
    for _ in range(tournament_size):
        idx = rng.next_int(0, len(population))
        candidate = population[idx]
        if best is None or candidate.fitness > best.fitness:
            best = candidate
    assert best is not None
    return best


def roulette_selection(population: list[Organism], rng: Mulberry32) -> Organism:
    min_fitness = min(o.fitness for o in population)
    offset = -min_fitness if min_fitness < 0 else 0
    total_fitness = sum(o.fitness + offset for o in population)
    if total_fitness == 0:
        return population[rng.next_int(0, len(population))]
    spin = rng.next() * total_fitness
    for org in population:
        spin -= org.fitness + offset
        if spin <= 0:
            return org
    return population[-1]


def rank_selection(population: list[Organism], rng: Mulberry32) -> Organism:
    sorted_pop = sorted(population, key=lambda o: o.fitness)
    n = len(sorted_pop)
    total_rank = n * (n + 1) // 2
    spin = rng.next() * total_rank
    for i, org in enumerate(sorted_pop):
        spin -= i + 1
        if spin <= 0:
            return org
    return sorted_pop[-1]


def elite_selection(population: list[Organism], count: int) -> list[Organism]:
    sorted_pop = sorted(population, key=lambda o: o.fitness, reverse=True)
    return sorted_pop[:count]
