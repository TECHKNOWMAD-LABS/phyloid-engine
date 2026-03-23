"""Comprehensive tests for ParadigmJudge and ParadigmPanel."""

import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.paradigm import ParadigmJudge, ParadigmPanel


class TestParadigmJudge:
    def test_evaluate(self):
        judge = ParadigmJudge("sum", lambda o: sum(o.genome))
        assert judge.evaluate(Organism([1, 2, 3])) == 6

    def test_name_and_weight(self):
        judge = ParadigmJudge("test", lambda o: 0, weight=2.5)
        assert judge.name == "test"
        assert judge.weight == 2.5

    def test_default_weight(self):
        judge = ParadigmJudge("test", lambda o: 0)
        assert judge.weight == 1.0

    def test_custom_evaluate_fn(self):
        judge = ParadigmJudge("max_gene", lambda o: max(o.genome))
        assert judge.evaluate(Organism([1, 5, 3])) == 5


class TestParadigmPanel:
    def test_add_judge(self, sum_judge):
        panel = ParadigmPanel()
        result = panel.add_judge(sum_judge)
        assert result is panel  # chainable
        assert len(panel.judges) == 1

    def test_remove_judge(self, sum_judge):
        panel = ParadigmPanel()
        panel.add_judge(sum_judge)
        panel.remove_judge("sum")
        assert len(panel.judges) == 0

    def test_remove_nonexistent_judge(self):
        panel = ParadigmPanel()
        panel.remove_judge("nonexistent")  # Should not raise
        assert len(panel.judges) == 0

    def test_get_judge(self, sum_judge):
        panel = ParadigmPanel()
        panel.add_judge(sum_judge)
        found = panel.get_judge("sum")
        assert found is sum_judge

    def test_get_judge_not_found(self):
        panel = ParadigmPanel()
        assert panel.get_judge("missing") is None

    def test_judges_property_is_copy(self, sum_judge):
        panel = ParadigmPanel()
        panel.add_judge(sum_judge)
        judges = panel.judges
        judges.clear()
        assert len(panel.judges) == 1  # Original unchanged

    def test_empty_panel_evaluate(self):
        panel = ParadigmPanel()
        result = panel.evaluate(Organism([1, 2, 3]))
        assert result == {"scores": {}, "aggregate": 0}

    def test_single_judge_evaluate(self, sum_judge):
        panel = ParadigmPanel()
        panel.add_judge(sum_judge)
        result = panel.evaluate(Organism([1, 2, 3]))
        assert result["scores"]["sum"] == 6
        assert result["aggregate"] == 6

    def test_weighted_aggregate(self, panel_with_judges):
        o = Organism([1, 2, 3])
        result = panel_with_judges.evaluate(o)
        # sum=6 (weight=1), max=3 (weight=2)
        # aggregate = (6*1 + 3*2) / (1+2) = 12/3 = 4
        assert result["aggregate"] == 4.0
        assert result["scores"]["sum"] == 6
        assert result["scores"]["max"] == 3

    def test_evaluate_population(self, sum_judge):
        panel = ParadigmPanel()
        panel.add_judge(sum_judge)
        pop = [Organism([1, 2]), Organism([3, 4]), Organism([5, 6])]
        panel.evaluate_population(pop)
        assert pop[0].fitness == 3
        assert pop[1].fitness == 7
        assert pop[2].fitness == 11

    def test_evaluate_population_sets_meta(self, sum_judge):
        panel = ParadigmPanel()
        panel.add_judge(sum_judge)
        pop = [Organism([1, 2])]
        panel.evaluate_population(pop)
        assert "paradigm_scores" in pop[0].meta
        assert pop[0].meta["paradigm_scores"]["sum"] == 3
