import sys
sys.path.insert(0, "python")

from phyloid_engine.engine import EvolutionEngine
from phyloid_engine.paradigm import ParadigmJudge
from phyloid_engine.organism import Organism


def test_initialize():
    engine = EvolutionEngine({"population_size": 20, "genome_length": 5, "seed": 1})
    engine.initialize()
    assert len(engine.population) == 20
    assert engine.population[0].size() == 5


def test_step():
    engine = EvolutionEngine({
        "population_size": 10,
        "genome_length": 4,
        "seed": 42,
        "fitness_fn": lambda o: sum(o.genome),
    })
    engine.initialize()
    stats = engine.step()
    assert stats["generation"] == 1


def test_run_completes():
    engine = EvolutionEngine({
        "population_size": 10,
        "genome_length": 4,
        "max_generations": 5,
        "seed": 42,
        "fitness_fn": lambda o: sum(o.genome),
    })
    result = engine.run()
    assert result["generations"] == 5
    assert isinstance(result["best"], Organism)


def test_deterministic():
    cfg = {
        "population_size": 10,
        "genome_length": 4,
        "max_generations": 5,
        "seed": 99,
        "fitness_fn": lambda o: sum(o.genome),
    }
    r1 = EvolutionEngine(cfg).run()
    r2 = EvolutionEngine(cfg).run()
    assert r1["best"].fitness == r2["best"].fitness
    assert r1["best"].genome == r2["best"].genome


def test_paradigm_integration():
    engine = EvolutionEngine({
        "population_size": 10,
        "genome_length": 3,
        "max_generations": 2,
        "seed": 42,
    })
    engine.panel.add_judge(ParadigmJudge("sum", lambda o: sum(o.genome)))
    result = engine.run()
    assert result["best"].fitness > 0


def test_events_fired():
    engine = EvolutionEngine({
        "population_size": 10,
        "genome_length": 4,
        "max_generations": 3,
        "seed": 42,
        "fitness_fn": lambda o: sum(o.genome),
    })
    gens = []
    engine.on("generation", lambda data: gens.append(data["generation"]))
    engine.run()
    assert gens == [1, 2, 3]
