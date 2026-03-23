from __future__ import annotations

from typing import Any

from .prng import Mulberry32


class Organism:
    """Container for a genome, fitness score, age, and metadata."""

    def __init__(self, genome: list[float] | None = None, fitness: float = 0) -> None:
        """Create an organism with the given genome and fitness."""
        self.genome: list[float] = list(genome) if genome else []
        self.fitness = fitness
        self.age = 0
        self.meta: dict[str, Any] = {}

    def clone(self) -> Organism:
        """Return an independent deep copy of this organism."""
        copy = Organism(list(self.genome), self.fitness)
        copy.age = self.age
        copy.meta = dict(self.meta)
        return copy

    def size(self) -> int:
        return len(self.genome)

    def get_gene(self, index: int) -> float:
        if not 0 <= index < len(self.genome):
            raise IndexError(f"gene index {index} out of range [0, {len(self.genome)})")
        return self.genome[index]

    def set_gene(self, index: int, value: float) -> None:
        if not 0 <= index < len(self.genome):
            raise IndexError(f"gene index {index} out of range [0, {len(self.genome)})")
        self.genome[index] = value

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict for JSON storage."""
        return {
            "genome": self.genome,
            "fitness": self.fitness,
            "age": self.age,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Organism:
        """Deserialize from a dict (inverse of to_dict)."""
        if not isinstance(obj, dict):
            raise TypeError(f"expected dict, got {type(obj).__name__}")
        if "genome" not in obj or "fitness" not in obj:
            raise ValueError("dict must contain 'genome' and 'fitness' keys")
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
        """Create a random organism with genes uniformly distributed in [gene_min, gene_max]."""
        if length < 0:
            raise ValueError(f"length must be non-negative, got {length}")
        if gene_max < gene_min:
            raise ValueError(f"gene_max ({gene_max}) must be >= gene_min ({gene_min})")
        genome = [gene_min + rng.next() * (gene_max - gene_min) for _ in range(length)]
        return cls(genome)
