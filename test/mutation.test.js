'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { Organism } = require('../src/organism');
const { Mulberry32 } = require('../src/prng');
const { bitFlipMutation, swapMutation, gaussianMutation } = require('../src/mutation');

describe('Mutation', () => {
  it('bitFlip flips genes', () => {
    const rng = new Mulberry32(42);
    const o = new Organism([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    const m = bitFlipMutation(o, rng, 1.0); // rate=1 flips all
    for (const g of m.genome) {
      assert.equal(g, 1);
    }
  });

  it('bitFlip with rate=0 changes nothing', () => {
    const rng = new Mulberry32(42);
    const o = new Organism([0, 1, 0, 1]);
    const m = bitFlipMutation(o, rng, 0);
    assert.deepEqual(m.genome, [0, 1, 0, 1]);
  });

  it('swap mutation does not change genome length', () => {
    const rng = new Mulberry32(42);
    const o = new Organism([1, 2, 3, 4, 5]);
    const m = swapMutation(o, rng, 0.5);
    assert.equal(m.size(), 5);
  });

  it('swap preserves gene set (all genes present)', () => {
    const rng = new Mulberry32(42);
    const genes = [10, 20, 30, 40, 50];
    const o = new Organism(genes);
    const m = swapMutation(o, rng, 1.0);
    assert.deepEqual([...m.genome].sort((a, b) => a - b), [10, 20, 30, 40, 50]);
  });

  it('gaussian produces bounded values', () => {
    const rng = new Mulberry32(42);
    const o = new Organism([0.5, 0.5, 0.5, 0.5, 0.5]);
    const m = gaussianMutation(o, rng, 1.0, 0.1, 0, 1);
    for (const g of m.genome) {
      assert.ok(g >= 0 && g <= 1);
    }
  });

  it('mutation does not modify original', () => {
    const rng = new Mulberry32(42);
    const o = new Organism([1, 2, 3]);
    const orig = [...o.genome];
    bitFlipMutation(o, rng, 1.0);
    assert.deepEqual(o.genome, orig);
  });
});
