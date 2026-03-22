'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { EvolutionEngine } = require('../src/engine');
const { ParadigmJudge } = require('../src/paradigm');
const { Organism } = require('../src/organism');

describe('EvolutionEngine', () => {
  it('initializes a population', () => {
    const engine = new EvolutionEngine({ populationSize: 20, genomeLength: 5, seed: 1 });
    engine.initialize();
    assert.equal(engine.population.length, 20);
    assert.equal(engine.population[0].size(), 5);
  });

  it('step advances one generation', () => {
    const engine = new EvolutionEngine({
      populationSize: 10, genomeLength: 4, seed: 42,
      fitnessFn: (o) => o.genome.reduce((a, b) => a + b, 0),
    });
    engine.initialize();
    const stats = engine.step();
    assert.equal(stats.generation, 1);
    assert.equal(engine.generation, 1);
  });

  it('run completes all generations', () => {
    const engine = new EvolutionEngine({
      populationSize: 10, genomeLength: 4, maxGenerations: 5, seed: 42,
      fitnessFn: (o) => o.genome.reduce((a, b) => a + b, 0),
    });
    const result = engine.run();
    assert.equal(result.generations, 5);
    assert.ok(result.best instanceof Organism);
  });

  it('emits generation events', () => {
    const engine = new EvolutionEngine({
      populationSize: 10, genomeLength: 4, maxGenerations: 3, seed: 42,
      fitnessFn: (o) => o.genome.reduce((a, b) => a + b, 0),
    });
    const gens = [];
    engine.on('generation', (data) => gens.push(data.generation));
    engine.run();
    assert.deepEqual(gens, [1, 2, 3]);
  });

  it('stops at target fitness', () => {
    const engine = new EvolutionEngine({
      populationSize: 20, genomeLength: 5, maxGenerations: 1000,
      targetFitness: 3, seed: 42, geneMin: 0, geneMax: 1,
      fitnessFn: (o) => o.genome.reduce((a, b) => a + b, 0),
    });
    let targetReached = false;
    engine.on('targetReached', () => { targetReached = true; });
    const result = engine.run();
    assert.ok(result.generations < 1000);
    assert.ok(targetReached);
  });

  it('paradigm panel integrates with engine', () => {
    const engine = new EvolutionEngine({
      populationSize: 10, genomeLength: 3, maxGenerations: 2, seed: 42,
    });
    engine.panel.addJudge(
      new ParadigmJudge('sum', (o) => o.genome.reduce((a, b) => a + b, 0))
    );
    const result = engine.run();
    assert.ok(result.best.fitness > 0);
  });

  it('deterministic with same seed', () => {
    const cfg = {
      populationSize: 10, genomeLength: 4, maxGenerations: 5, seed: 99,
      fitnessFn: (o) => o.genome.reduce((a, b) => a + b, 0),
    };
    const r1 = new EvolutionEngine(cfg).run();
    const r2 = new EvolutionEngine(cfg).run();
    assert.equal(r1.best.fitness, r2.best.fitness);
    assert.deepEqual(r1.best.genome, r2.best.genome);
  });

  it('stats track generation history', () => {
    const engine = new EvolutionEngine({
      populationSize: 10, genomeLength: 4, maxGenerations: 3, seed: 42,
      fitnessFn: (o) => o.genome.reduce((a, b) => a + b, 0),
    });
    engine.run();
    assert.equal(engine.stats.generationHistory.length, 3);
    assert.ok('best' in engine.stats.generationHistory[0]);
    assert.ok('average' in engine.stats.generationHistory[0]);
  });

  it('emits started and completed events', () => {
    const engine = new EvolutionEngine({
      populationSize: 10, genomeLength: 4, maxGenerations: 1, seed: 42,
      fitnessFn: () => 1,
    });
    let started = false;
    let completed = false;
    engine.on('started', () => { started = true; });
    engine.on('completed', () => { completed = true; });
    engine.run();
    assert.ok(started);
    assert.ok(completed);
  });
});
