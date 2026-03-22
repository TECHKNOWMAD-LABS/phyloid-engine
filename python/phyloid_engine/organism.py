from __future__ import annotations

from typing import Any

from .prng import Mulberry32


class Organism:
    def __init__(self, genome: list[float] | None = None, fitness: float = 0) -> None:
        self.genome: list[float] = list(genome) if genome else []
        self.fitness = fitness
        self.age = 0
        self.meta: dict[str, Any] = {}

    def clone(self) -> Organism:
        copy = Organism(list(self.genome), self.fitness)
        copy.age = self.age
        copy.meta = dict(self.meta)
        return copy

    def size(self) -> int:
        return len(self.genome)

    def get_gene(self, index: int) -> float:
        return self.genome[index]

    def set_gene(self, index: int, value: float) -> None:
        self.genome[index] = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "genome": self.genome,
            "fitness": self.fitness,
            "age": self.age,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Organism:
        o = cls(obj["genome"], obj["fitness"])
        o.age = obj.get("age", 0)
        o.meta = obj.get("meta", {})
        return o

    @classmethod
    def random(
        cls,
        length: int,
        rng: Mulberry32,
        gene_min: float = 0,
        gene_max: float = 1,
    ) -> Organism:
        genome = [gene_min + rng.next() * (gene_max - gene_min) for _ in range(length)]
        return cls(genome)
