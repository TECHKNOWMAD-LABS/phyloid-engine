'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { Organism } = require('../src/organism');
const { Mulberry32 } = require('../src/prng');

describe('Organism', () => {
  it('constructs with genome and fitness', () => {
    const o = new Organism([1, 2, 3], 5);
    assert.deepEqual(o.genome, [1, 2, 3]);
    assert.equal(o.fitness, 5);
  });

  it('clone creates independent copy', () => {
    const o = new Organism([1, 2, 3], 10);
    o.meta.tag = 'original';
    const c = o.clone();
    c.genome[0] = 99;
    c.meta.tag = 'clone';
    assert.equal(o.genome[0], 1);
    assert.equal(o.meta.tag, 'original');
  });

  it('size returns genome length', () => {
    assert.equal(new Organism([0, 0, 0, 0]).size(), 4);
  });

  it('get/set gene', () => {
    const o = new Organism([10, 20, 30]);
    assert.equal(o.getGene(1), 20);
    o.setGene(1, 99);
    assert.equal(o.getGene(1), 99);
  });

  it('toJSON and fromJSON roundtrip', () => {
    const o = new Organism([1, 2], 7);
    o.age = 3;
    o.meta.x = true;
    const json = o.toJSON();
    const restored = Organism.fromJSON(json);
    assert.deepEqual(restored.genome, [1, 2]);
    assert.equal(restored.fitness, 7);
    assert.equal(restored.age, 3);
  });

  it('random generates organism with correct length', () => {
    const rng = new Mulberry32(42);
    const o = Organism.random(8, rng, 0, 10);
    assert.equal(o.size(), 8);
    for (const g of o.genome) {
      assert.ok(g >= 0 && g <= 10);
    }
  });

  it('default fitness is 0', () => {
    assert.equal(new Organism([1]).fitness, 0);
  });
});
