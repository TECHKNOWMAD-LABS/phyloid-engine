'use strict';

const { Organism } = require('./organism');

function bitFlipMutation(organism, rng, rate = 0.01) {
  const child = organism.clone();
  for (let i = 0; i < child.size(); i++) {
    if (rng.next() < rate) {
      child.setGene(i, 1 - child.getGene(i));
    }
  }
  return child;
}

function swapMutation(organism, rng, rate = 0.01) {
  const child = organism.clone();
  for (let i = 0; i < child.size(); i++) {
    if (rng.next() < rate) {
      const j = rng.nextInt(0, child.size());
      const tmp = child.getGene(i);
      child.setGene(i, child.getGene(j));
      child.setGene(j, tmp);
    }
  }
  return child;
}

function gaussianMutation(organism, rng, rate = 0.01, sigma = 0.1, min = -Infinity, max = Infinity) {
  const child = organism.clone();
  for (let i = 0; i < child.size(); i++) {
    if (rng.next() < rate) {
      // Box-Muller transform for Gaussian
      const u1 = rng.next() || 1e-10;
      const u2 = rng.next();
      const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
      let value = child.getGene(i) + z * sigma;
      value = Math.max(min, Math.min(max, value));
      child.setGene(i, value);
    }
  }
  return child;
}

const STRATEGIES = {
  bitFlip: bitFlipMutation,
  swap: swapMutation,
  gaussian: gaussianMutation,
};

module.exports = {
  bitFlipMutation,
  swapMutation,
  gaussianMutation,
  STRATEGIES,
};
