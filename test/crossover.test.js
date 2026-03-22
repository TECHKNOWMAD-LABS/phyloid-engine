'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { Organism } = require('../src/organism');
const { Mulberry32 } = require('../src/prng');
const { singlePointCrossover, twoPointCrossover, uniformCrossover } = require('../src/crossover');

describe('Crossover', () => {
  it('single-point produces two children', () => {
    const rng = new Mulberry32(42);
    const a = new Organism([1, 1, 1, 1, 1]);
    const b = new Organism([2, 2, 2, 2, 2]);
    const [c1, c2] = singlePointCrossover(a, b, rng);
    assert.equal(c1.size(), 5);
    assert.equal(c2.size(), 5);
  });

  it('single-point children contain genes from both parents', () => {
    const rng = new Mulberry32(42);
    const a = new Organism([0, 0, 0, 0, 0]);
    const b = new Organism([1, 1, 1, 1, 1]);
    const [c1] = singlePointCrossover(a, b, rng);
    const has0 = c1.genome.includes(0);
    const has1 = c1.genome.includes(1);
    assert.ok(has0 && has1, 'child should have genes from both parents');
  });

  it('two-point produces two children of correct length', () => {
    const rng = new Mulberry32(7);
    const a = new Organism([1, 2, 3, 4, 5, 6]);
    const b = new Organism([10, 20, 30, 40, 50, 60]);
    const [c1, c2] = twoPointCrossover(a, b, rng);
    assert.equal(c1.size(), 6);
    assert.equal(c2.size(), 6);
  });

  it('uniform crossover preserves genome length', () => {
    const rng = new Mulberry32(42);
    const a = new Organism([1, 2, 3, 4]);
    const b = new Organism([5, 6, 7, 8]);
    const [c1, c2] = uniformCrossover(a, b, rng);
    assert.equal(c1.size(), 4);
    assert.equal(c2.size(), 4);
  });

  it('uniform with swapProb=0 copies parents exactly', () => {
    const rng = new Mulberry32(42);
    const a = new Organism([1, 2, 3]);
    const b = new Organism([4, 5, 6]);
    const [c1, c2] = uniformCrossover(a, b, rng, 0);
    assert.deepEqual(c1.genome, [1, 2, 3]);
    assert.deepEqual(c2.genome, [4, 5, 6]);
  });

  it('crossover does not mutate parents', () => {
    const rng = new Mulberry32(42);
    const a = new Organism([1, 2, 3, 4]);
    const b = new Organism([5, 6, 7, 8]);
    const origA = [...a.genome];
    const origB = [...b.genome];
    singlePointCrossover(a, b, rng);
    assert.deepEqual(a.genome, origA);
    assert.deepEqual(b.genome, origB);
  });
});
