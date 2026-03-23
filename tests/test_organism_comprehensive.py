"""Comprehensive tests for Organism class."""

import sys
sys.path.insert(0, "python")

from phyloid_engine.organism import Organism
from phyloid_engine.prng import Mulberry32


class TestOrganismConstruction:
    def test_default_empty(self):
        o = Organism()
        assert o.genome == []
        assert o.fitness == 0
        assert o.age == 0
        assert o.meta == {}

    def test_with_genome_and_fitness(self):
        o = Organism([1.0, 2.0, 3.0], 42.0)
        assert o.genome == [1.0, 2.0, 3.0]
        assert o.fitness == 42.0

    def test_genome_is_copied(self):
        original = [1.0, 2.0, 3.0]
        o = Organism(original)
        original[0] = 999
        assert o.genome[0] == 1.0

    def test_none_genome_becomes_empty(self):
        o = Organism(None)
        assert o.genome == []


class TestOrganismClone:
    def test_clone_is_independent(self, sample_organism):
        clone = sample_organism.clone()
        clone.genome[0] = 999
        clone.fitness = 999
        clone.age = 999
        clone.meta["key"] = "val"
        assert sample_organism.genome[0] == 0.1
        assert sample_organism.fitness == 2.5
        assert sample_organism.age == 0
        assert "key" not in sample_organism.meta

    def test_clone_preserves_all_fields(self, sample_organism):
        sample_organism.age = 5
        sample_organism.meta["tag"] = "test"
        clone = sample_organism.clone()
        assert clone.genome == sample_organism.genome
        assert clone.fitness == sample_organism.fitness
        assert clone.age == 5
        assert clone.meta == {"tag": "test"}


class TestOrganismGenes:
    def test_size(self, sample_organism):
        assert sample_organism.size() == 5

    def test_size_empty(self):
        assert Organism().size() == 0

    def test_get_gene(self, sample_organism):
        assert sample_organism.get_gene(0) == 0.1
        assert sample_organism.get_gene(4) == 0.7

    def test_set_gene(self, sample_organism):
        sample_organism.set_gene(2, 0.0)
        assert sample_organism.get_gene(2) == 0.0


class TestOrganismSerialization:
    def test_to_dict(self, sample_organism):
        sample_organism.age = 3
        sample_organism.meta["x"] = 1
        d = sample_organism.to_dict()
        assert d["genome"] == [0.1, 0.5, 0.9, 0.3, 0.7]
        assert d["fitness"] == 2.5
        assert d["age"] == 3
        assert d["meta"] == {"x": 1}

    def test_from_dict_roundtrip(self, sample_organism):
        sample_organism.age = 7
        sample_organism.meta["tag"] = "hello"
        d = sample_organism.to_dict()
        restored = Organism.from_dict(d)
        assert restored.genome == sample_organism.genome
        assert restored.fitness == sample_organism.fitness
        assert restored.age == 7
        assert restored.meta == {"tag": "hello"}

    def test_from_dict_missing_optional_fields(self):
        d = {"genome": [1, 2], "fitness": 5}
        o = Organism.from_dict(d)
        assert o.age == 0
        assert o.meta == {}


class TestOrganismRandom:
    def test_random_creates_correct_length(self, rng):
        o = Organism.random(10, rng)
        assert o.size() == 10

    def test_random_respects_bounds(self, rng):
        o = Organism.random(100, rng, gene_min=-5, gene_max=5)
        assert all(-5 <= g <= 5 for g in o.genome)

    def test_random_default_bounds(self, rng):
        o = Organism.random(100, rng)
        assert all(0 <= g <= 1 for g in o.genome)

    def test_random_deterministic(self):
        o1 = Organism.random(10, Mulberry32(42))
        o2 = Organism.random(10, Mulberry32(42))
        assert o1.genome == o2.genome

    def test_random_zero_length(self, rng):
        o = Organism.random(0, rng)
        assert o.size() == 0
        assert o.genome == []
