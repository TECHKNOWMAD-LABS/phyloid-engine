'use strict';

const { Organism } = require('./organism');

function singlePointCrossover(parentA, parentB, rng) {
  const len = Math.min(parentA.size(), parentB.size());
  const point = rng.nextInt(1, len);
  const childGenomeA = [
    ...parentA.genome.slice(0, point),
    ...parentB.genome.slice(point),
  ];
  const childGenomeB = [
    ...parentB.genome.slice(0, point),
    ...parentA.genome.slice(point),
  ];
  return [new Organism(childGenomeA), new Organism(childGenomeB)];
}

function twoPointCrossover(parentA, parentB, rng) {
  const len = Math.min(parentA.size(), parentB.size());
  let p1 = rng.nextInt(1, len);
  let p2 = rng.nextInt(1, len);
  if (p1 > p2) [p1, p2] = [p2, p1];
  if (p1 === p2) p2 = Math.min(p2 + 1, len);
  const childGenomeA = [
    ...parentA.genome.slice(0, p1),
    ...parentB.genome.slice(p1, p2),
    ...parentA.genome.slice(p2),
  ];
  const childGenomeB = [
    ...parentB.genome.slice(0, p1),
    ...parentA.genome.slice(p1, p2),
    ...parentB.genome.slice(p2),
  ];
  return [new Organism(childGenomeA), new Organism(childGenomeB)];
}

function uniformCrossover(parentA, parentB, rng, swapProb = 0.5) {
  const len = Math.min(parentA.size(), parentB.size());
  const genomeA = [];
  const genomeB = [];
  for (let i = 0; i < len; i++) {
    if (rng.next() < swapProb) {
      genomeA.push(parentB.genome[i]);
      genomeB.push(parentA.genome[i]);
    } else {
      genomeA.push(parentA.genome[i]);
      genomeB.push(parentB.genome[i]);
    }
  }
  return [new Organism(genomeA), new Organism(genomeB)];
}

const STRATEGIES = {
  singlePoint: singlePointCrossover,
  twoPoint: twoPointCrossover,
  uniform: uniformCrossover,
};

module.exports = {
  singlePointCrossover,
  twoPointCrossover,
  uniformCrossover,
  STRATEGIES,
};
