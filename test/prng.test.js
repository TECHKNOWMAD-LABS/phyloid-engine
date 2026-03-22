'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { Mulberry32 } = require('../src/prng');

describe('Mulberry32 PRNG', () => {
  it('produces deterministic output for same seed', () => {
    const a = new Mulberry32(42);
    const b = new Mulberry32(42);
    for (let i = 0; i < 20; i++) {
      assert.equal(a.next(), b.next());
    }
  });

  it('produces values in [0, 1)', () => {
    const rng = new Mulberry32(123);
    for (let i = 0; i < 1000; i++) {
      const v = rng.next();
      assert.ok(v >= 0 && v < 1, `out of range: ${v}`);
    }
  });

  it('different seeds produce different sequences', () => {
    const a = new Mulberry32(1);
    const b = new Mulberry32(2);
    const seqA = Array.from({ length: 5 }, () => a.next());
    const seqB = Array.from({ length: 5 }, () => b.next());
    assert.notDeepEqual(seqA, seqB);
  });

  it('reset restores initial state', () => {
    const rng = new Mulberry32(99);
    const first = [rng.next(), rng.next(), rng.next()];
    rng.reset();
    const second = [rng.next(), rng.next(), rng.next()];
    assert.deepEqual(first, second);
  });

  it('nextInt produces integers in [min, max)', () => {
    const rng = new Mulberry32(7);
    for (let i = 0; i < 200; i++) {
      const v = rng.nextInt(3, 10);
      assert.ok(v >= 3 && v < 10 && Number.isInteger(v));
    }
  });

  it('exposes seed property', () => {
    const rng = new Mulberry32(55);
    assert.equal(rng.seed, 55);
  });
});
