"""Property-based tests using Hypothesis for core invariants."""

import sys
sys.path.insert(0, "python")

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from phyloid_engine.prng import Mulberry32
from phyloid_engine.organism import Organism
from phyloid_engine.selection import tournament_selection, roulette_selection, elite_selection
from phyloid_engine.mutation import bit_flip_mutation, swap_mutation, gaussian_mutation
from phyloid_engine.crossover import single_point_crossover, two_point_crossover, uniform_crossover
from phyloid_engine.paradigm import ParadigmJudge, ParadigmPanel
from phyloid_engine.engine import EvolutionEngine


# -- Strategies --

seeds = st.integers(min_value=0, max_value=0xFFFFFFFF)
genome_values = st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False)
genomes = st.lists(genome_values, min_size=2, max_size=50)
rates = st.floats(min_value=0.0, max_value=1.0)


class TestPrngProperties:
    @given(seed=seeds)
    @settings(max_examples=50)
    def test_output_always_in_unit_range(self, seed):
        rng = Mulberry32(seed)
        for _ in range(100):
            v = rng.next()
            assert 0.0 <= v < 1.0

    @given(seed=seeds)
    @settings(max_examples=50)
    def test_deterministic_for_any_seed(self, seed):
        a = Mulberry32(seed)
        b = Mulberry32(seed)
        for _ in range(50):
            assert a.next() == b.next()

    @given(seed=seeds, lo=st.integers(min_value=-1000, max_value=999))
    @settings(max_examples=50)
    def test_next_int_always_in_bounds(self, seed, lo):
        hi = lo + 1 + (seed % 100)
        rng = Mulberry32(seed)
        for _ in range(20):
            v = rng.next_int(lo, hi)
            assert lo <= v < hi

    @given(seed=seeds)
    @settings(max_examples=30)
    def test_reset_reproduces_sequence(self, seed):
        rng = Mulberry32(seed)
        first = [rng.next() for _ in range(20)]
        rng.reset()
        second = [rng.next() for _ in range(20)]
        assert first == second


class TestOrganismProperties:
    @given(genome=genomes, fitness=genome_values)
    @settings(max_examples=50)
    def test_serialization_roundtrip(self, genome, fitness):
        o = Organism(genome, fitness)
        o.age = 5
        o.meta = {"key": "value"}
        d = o.to_dict()
        restored = Organism.from_dict(d)
        assert restored.genome == o.genome
        assert restored.fitness == o.fitness
        assert restored.age == o.age
        assert restored.meta == o.meta

    @given(genome=genomes, fitness=genome_values)
    @settings(max_examples=50)
    def test_clone_preserves_all_fields(self, genome, fitness):
        o = Organism(genome, fitness)
        o.age = 3
        c = o.clone()
        assert c.genome == o.genome
        assert c.fitness == o.fitness
        assert c.age == o.age
        # Clone is independent
        c.genome[0] = -999
        assert o.genome[0] != -999

    @given(seed=seeds, length=st.integers(min_value=0, max_value=100))
    @settings(max_examples=30)
    def test_random_always_correct_length(self, seed, length):
        rng = Mulberry32(seed)
        o = Organism.random(length, rng, 0, 1)
        assert o.size() == length


class TestMutationProperties:
    @given(genome=genomes, seed=seeds)
    @settings(max_examples=50)
    def test_bit_flip_preserves_size(self, genome, seed):
        rng = Mulberry32(seed)
        o = Organism(genome)
        m = bit_flip_mutation(o, rng, rate=0.5)
        assert m.size() == o.size()

    @given(genome=genomes, seed=seeds)
    @settings(max_examples=50)
    def test_swap_preserves_multiset(self, genome, seed):
        rng = Mulberry32(seed)
        o = Organism(genome)
        m = swap_mutation(o, rng, rate=1.0)
        assert sorted(m.genome) == sorted(o.genome)

    @given(genome=genomes, seed=seeds)
    @settings(max_examples=50)
    def test_gaussian_respects_bounds(self, genome, seed):
        rng = Mulberry32(seed)
        o = Organism(genome)
        m = gaussian_mutation(o, rng, rate=1.0, sigma=1.0, min_val=-200, max_val=200)
        assert all(-200 <= g <= 200 for g in m.genome)

    @given(genome=genomes, seed=seeds)
    @settings(max_examples=50)
    def test_mutation_never_modifies_original(self, genome, seed):
        rng = Mulberry32(seed)
        o = Organism(list(genome))
        original = list(genome)
        bit_flip_mutation(o, rng, rate=0.5)
        assert o.genome == original
        swap_mutation(o, Mulberry32(seed), rate=0.5)
        assert o.genome == original
        gaussian_mutation(o, Mulberry32(seed), rate=0.5, sigma=0.1)
        assert o.genome == original


class TestCrossoverProperties:
    @given(seed=seeds, n=st.integers(min_value=2, max_value=30))
    @settings(max_examples=50)
    def test_single_point_children_correct_length(self, seed, n):
        rng = Mulberry32(seed)
        a = Organism([float(i) for i in range(n)])
        b = Organism([float(i + 100) for i in range(n)])
        c1, c2 = single_point_crossover(a, b, rng)
        assert c1.size() == n
        assert c2.size() == n

    @given(seed=seeds, n=st.integers(min_value=2, max_value=30))
    @settings(max_examples=50)
    def test_uniform_gene_conservation(self, seed, n):
        rng = Mulberry32(seed)
        a = Organism([float(i) for i in range(n)])
        b = Organism([float(i + 100) for i in range(n)])
        c1, c2 = uniform_crossover(a, b, rng)
        for i in range(n):
            assert c1.genome[i] in (a.genome[i], b.genome[i])
            assert c2.genome[i] in (a.genome[i], b.genome[i])

    @given(seed=seeds, n=st.integers(min_value=2, max_value=30))
    @settings(max_examples=50)
    def test_crossover_never_modifies_parents(self, seed, n):
        rng = Mulberry32(seed)
        a = Organism([float(i) for i in range(n)])
        b = Organism([float(i + 100) for i in range(n)])
        a_orig = list(a.genome)
        b_orig = list(b.genome)
        single_point_crossover(a, b, rng)
        assert a.genome == a_orig
        assert b.genome == b_orig


class TestSelectionProperties:
    @given(seed=seeds)
    @settings(max_examples=30)
    def test_tournament_always_returns_member(self, seed):
        rng = Mulberry32(seed)
        pop = [Organism([float(i)], fitness=float(i)) for i in range(10)]
        for _ in range(20):
            sel = tournament_selection(pop, rng, 3)
            assert sel in pop

    @given(seed=seeds)
    @settings(max_examples=30)
    def test_elite_returns_sorted_descending(self, seed):
        rng = Mulberry32(seed)
        pop = [Organism([float(i)], fitness=rng.next() * 100) for i in range(20)]
        elites = elite_selection(pop, 5)
        fitnesses = [e.fitness for e in elites]
        assert fitnesses == sorted(fitnesses, reverse=True)


class TestEngineProperties:
    @given(seed=seeds)
    @settings(max_examples=10, deadline=10000)
    def test_population_size_invariant(self, seed):
        engine = EvolutionEngine({
            "population_size": 20,
            "genome_length": 5,
            "max_generations": 5,
            "seed": seed,
            "fitness_fn": lambda o: sum(o.genome),
        })
        engine.run()
        assert len(engine.population) == 20

    @given(seed=seeds)
    @settings(max_examples=10, deadline=10000)
    def test_best_organism_is_best(self, seed):
        engine = EvolutionEngine({
            "population_size": 20,
            "genome_length": 5,
            "max_generations": 10,
            "seed": seed,
            "fitness_fn": lambda o: sum(o.genome),
        })
        result = engine.run()
        # Best organism should be >= any current population member
        best = result["best"]
        for org in engine.population:
            assert best.fitness >= org.fitness
