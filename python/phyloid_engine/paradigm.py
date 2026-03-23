from __future__ import annotations

from typing import Any, Callable

from .organism import Organism


class ParadigmJudge:
    """Single-objective fitness function with a name and weight."""

    def __init__(
        self, name: str, evaluate_fn: Callable[[Organism], float], weight: float = 1.0
    ) -> None:
        self.name = name
        self._evaluate = evaluate_fn
        self.weight = weight

    def evaluate(self, organism: Organism) -> float:
        return self._evaluate(organism)


class ParadigmPanel:
    """Multi-objective fitness aggregator using weighted judges."""

    def __init__(self) -> None:
        self._judges: list[ParadigmJudge] = []

    def add_judge(self, judge: ParadigmJudge) -> ParadigmPanel:
        self._judges.append(judge)
        return self

    def remove_judge(self, name: str) -> ParadigmPanel:
        self._judges = [j for j in self._judges if j.name != name]
        return self

    def get_judge(self, name: str) -> ParadigmJudge | None:
        for j in self._judges:
            if j.name == name:
                return j
        return None

    @property
    def judges(self) -> list[ParadigmJudge]:
        return list(self._judges)

    def evaluate(self, organism: Organism) -> dict[str, Any]:
        if not self._judges:
            return {"scores": {}, "aggregate": 0}
        total_weight = 0.0
        total_score = 0.0
        scores: dict[str, float] = {}
        for judge in self._judges:
            score = judge.evaluate(organism)
            scores[judge.name] = score
            total_score += score * judge.weight
            total_weight += judge.weight
        aggregate = total_score / total_weight if total_weight > 0 else 0
        return {"scores": scores, "aggregate": aggregate}

    def evaluate_population(self, population: list[Organism]) -> list[Organism]:
        for org in population:
            result = self.evaluate(org)
            org.fitness = result["aggregate"]
            org.meta["paradigm_scores"] = result["scores"]
        return population
