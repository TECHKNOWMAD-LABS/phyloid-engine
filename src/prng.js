'use strict';

/**
 * Mulberry32 seeded PRNG — deterministic, identical output in JS and Python.
 */
class Mulberry32 {
  constructor(seed) {
    this._initial = seed >>> 0;
    this._state = this._initial;
  }

  next() {
    let t = (this._state += 0x6d2b79f5) | 0;
    t = Math.imul(t ^ (t >>> 15), 1 | t);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  }

  nextInt(min, max) {
    return min + Math.floor(this.next() * (max - min));
  }

  reset() {
    this._state = this._initial;
  }

  get seed() {
    return this._initial;
  }
}

module.exports = { Mulberry32 };
