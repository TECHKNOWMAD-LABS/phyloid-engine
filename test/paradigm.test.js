'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { Organism } = require('../src/organism');
const { ParadigmJudge, ParadigmPanel } = require('../src/paradigm');

describe('ParadigmJudge', () => {
  it('evaluates an organism', () => {
    const judge = new ParadigmJudge('sum', (o) => o.genome.reduce((a, b) => a + b, 0));
    assert.equal(judge.evaluate(new Organism([1, 2, 3])), 6);
  });

  it('has name and weight', () => {
    const judge = new ParadigmJudge('test', () => 0, 2.5);
    assert.equal(judge.name, 'test');
    assert.equal(judge.weight, 2.5);
  });
});

describe('ParadigmPanel', () => {
  it('registers and retrieves judges', () => {
    const panel = new ParadigmPanel();
    const j = new ParadigmJudge('a', () => 1);
    panel.addJudge(j);
    assert.equal(panel.getJudge('a'), j);
    assert.equal(panel.judges.length, 1);
  });

  it('removes judge by name', () => {
    const panel = new ParadigmPanel();
    panel.addJudge(new ParadigmJudge('a', () => 1));
    panel.addJudge(new ParadigmJudge('b', () => 2));
    panel.removeJudge('a');
    assert.equal(panel.judges.length, 1);
    assert.equal(panel.getJudge('a'), null);
  });

  it('evaluates with weighted aggregate', () => {
    const panel = new ParadigmPanel();
    panel.addJudge(new ParadigmJudge('a', () => 10, 1));
    panel.addJudge(new ParadigmJudge('b', () => 20, 3));
    const result = panel.evaluate(new Organism([1]));
    // (10*1 + 20*3) / (1+3) = 70/4 = 17.5
    assert.equal(result.aggregate, 17.5);
    assert.equal(result.scores.a, 10);
    assert.equal(result.scores.b, 20);
  });

  it('empty panel returns 0', () => {
    const panel = new ParadigmPanel();
    const result = panel.evaluate(new Organism([1]));
    assert.equal(result, 0);
  });

  it('evaluatePopulation sets fitness on all organisms', () => {
    const panel = new ParadigmPanel();
    panel.addJudge(new ParadigmJudge('sum', (o) => o.genome.reduce((a, b) => a + b, 0)));
    const pop = [new Organism([1, 2]), new Organism([3, 4])];
    panel.evaluatePopulation(pop);
    assert.equal(pop[0].fitness, 3);
    assert.equal(pop[1].fitness, 7);
  });
});
