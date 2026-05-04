import sys

sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.paradigm import ParadigmJudge, ParadigmPanel


def test_judge_evaluates():
    judge = ParadigmJudge("sum", lambda o: sum(o.genome))
    assert judge.evaluate(Organism([1, 2, 3])) == 6


def test_panel_weighted_aggregate():
    panel = ParadigmPanel()
    panel.add_judge(ParadigmJudge("a", lambda _: 10, weight=1))
    panel.add_judge(ParadigmJudge("b", lambda _: 20, weight=3))
    result = panel.evaluate(Organism([1]))
    assert result["aggregate"] == 17.5


def test_panel_evaluate_population():
    panel = ParadigmPanel()
    panel.add_judge(ParadigmJudge("sum", lambda o: sum(o.genome)))
    pop = [Organism([1, 2]), Organism([3, 4])]
    panel.evaluate_population(pop)
    assert pop[0].fitness == 3
    assert pop[1].fitness == 7
