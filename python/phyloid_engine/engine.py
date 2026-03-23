from __future__ import annotations

from typing import Any, Callable

from .prng import Mulberry32
from .organism import Organism
from .selection import tournament_selection, elite_selection
from .crossover import single_point_crossover
from .mutation import gaussian_mutation
from .paradigm import ParadigmPanel
from .events import EventEmitter

DEFAULTS: dict[str, Any] = {
    "population_size": 100,
    "genome_length": 10,
    "gene_min": 0,
    "gene_max": 1,
    "elite_count": 2,
    "mutation_rate": 0.05,
    "mutation_sigma": 0.1,
    "crossover_rate": 0.8,
    "tournament_size": 3,
    "max_generations": 100,
    "target_fitness": float("inf"),
    "seed": 42,
}


class EvolutionEngine(EventEmitter):
    """Main evolution orchestrator with configurable operators and event hooks."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__()
        self.config = {**DEFAULTS, **(config or {})}
        if self.config["population_size"] < 2:
            raise ValueError("population_size must be >= 2")
        if self.config["genome_length"] < 2:
            raise ValueError("genome_length must be >= 2 for crossover")
        if self.config["elite_count"] >= self.config["population_size"]:
            raise ValueError("elite_count must be less than population_size")
        self.rng = Mulberry32(self.config["seed"])
        self.panel = ParadigmPanel()
        self.population: list[Organism] = []
        self.generation = 0
        self.best_organism: Organism | None = None
        self.stats: dict[str, Any] = {"generation_history": []}

        self._select_fn: Callable[..., Organism] = (
            config.get("select_fn", tournament_selection) if config else tournament_selection
        )
        self._crossover_fn = (
            config.get("crossover_fn", single_point_crossover) if config else single_point_crossover
        )
        self._mutate_fn = (
            config.get("mutate_fn", gaussian_mutation) if config else gaussian_mutation
        )
        self._fitness_fn: Callable[[Organism], float] | None = (
            config.get("fitness_fn") if config else None
        )

    def initialize(self) -> EvolutionEngine:
        """Create the initial random population and evaluate fitness."""
        self.population = []
        for _ in range(self.config["population_size"]):
            self.population.append(
                Organism.random(
                    self.config["genome_length"],
                    self.rng,
                    self.config["gene_min"],
                    self.config["gene_max"],
                )
            )
        self.generation = 0
        self._evaluate_all()
        self.emit("initialized", {"population": self.population})
        return self

    def _evaluate_all(self) -> None:
        if self._fitness_fn:
            for org in self.population:
                org.fitness = self._fitness_fn(org)
        if self.panel.judges:
            self.panel.evaluate_population(self.population)
        self._update_best()

    def _update_best(self) -> None:
        current_best = max(self.population, key=lambda o: o.fitness)
        if self.best_organism is None or current_best.fitness > self.best_organism.fitness:
            self.best_organism = current_best.clone()

    def step(self) -> dict[str, Any]:
        """Run one generation of selection, crossover, mutation, and evaluation."""
        cfg = self.config
        elite_count = cfg["elite_count"]
        crossover_rate = cfg["crossover_rate"]
        mutation_rate = cfg["mutation_rate"]
        mutation_sigma = cfg["mutation_sigma"]
        tournament_size = cfg["tournament_size"]
        pop_size = cfg["population_size"]
        gene_min = cfg["gene_min"]
        gene_max = cfg["gene_max"]
        select = self._select_fn
        crossover = self._crossover_fn
        mutate = self._mutate_fn
        rng = self.rng
        population = self.population

        # Pre-allocate with elites
        next_pop: list[Organism] = []
        elites = elite_selection(population, elite_count)
        for e in elites:
            c = e.clone()
            c.age = e.age + 1
            next_pop.append(c)

        # Fill remaining via selection + crossover + mutation
        while len(next_pop) < pop_size:
            parent_a = select(population, rng, tournament_size)
            parent_b = select(population, rng, tournament_size)

            if rng.next() < crossover_rate:
                children = crossover(parent_a, parent_b, rng)
            else:
                children = (parent_a.clone(), parent_b.clone())

            for child in children:
                child = mutate(child, rng, mutation_rate, mutation_sigma, gene_min, gene_max)
                if len(next_pop) < pop_size:
                    next_pop.append(child)

        self.population = next_pop
        self.generation += 1
        self._evaluate_all()

        gen_stats = self._gen_stats()
        self.stats["generation_history"].append(gen_stats)
        self.emit("generation", {"generation": self.generation, "stats": gen_stats})
        return gen_stats

    def _gen_stats(self) -> dict[str, Any]:
        fitnesses = [o.fitness for o in self.population]
        best_f = fitnesses[0]
        worst_f = fitnesses[0]
        total = 0.0
        for f in fitnesses:
            if f > best_f:
                best_f = f
            if f < worst_f:
                worst_f = f
            total += f
        return {
            "generation": self.generation,
            "best": best_f,
            "worst": worst_f,
            "average": total / len(fitnesses),
            "best_organism": self.best_organism.clone() if self.best_organism else None,
        }

    def run(self) -> dict[str, Any]:
        """Run evolution until max_generations or target_fitness is reached."""
        if not self.population:
            self.initialize()

        self.emit("started", {"config": self.config})

        while self.generation < self.config["max_generations"]:
            stats = self.step()
            if stats["best"] >= self.config["target_fitness"]:
                self.emit("target_reached", stats)
                break

        result = {
            "generations": self.generation,
            "best": self.best_organism.clone() if self.best_organism else None,
            "stats": self.stats,
        }
        self.emit("completed", result)
        return result
