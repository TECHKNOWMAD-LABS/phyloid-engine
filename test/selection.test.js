'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { Organism } = require('../src/organism');
const { Mulberry32 } = require('../src/prng');
const { tournamentSelection, rouletteSelection, rankSelection, eliteSelection } = require('../src/selection');

function makePop() {
  return [
    new Organism([1], 10),
    new Organism([2], 50),
    new Organism([3], 30),
    new Organism([4], 80),
    new Organism([5], 20),
  ];
}

describe('Selection', () => {
  it('tournament returns an organism from the population', () => {
    const rng = new Mulberry32(42);
    const pop = makePop();
    const selected = tournamentSelection(pop, rng, 3);
    assert.ok(pop.includes(selected));
  });

  it('tournament with size=pop.length always returns fittest', () => {
    const rng = new Mulberry32(1);
    const pop = makePop();
    const selected = tournamentSelection(pop, rng, pop.length);
    assert.equal(selected.fitness, 80);
  });

  it('roulette returns an organism from the population', () => {
    const rng = new Mulberry32(42);
    const pop = makePop();
    const selected = rouletteSelection(pop, rng);
    assert.ok(pop.includes(selected));
  });

  it('roulette handles negative fitness', () => {
    const rng = new Mulberry32(42);
    const pop = [new Organism([1], -5), new Organism([2], -10), new Organism([3], 3)];
    const selected = rouletteSelection(pop, rng);
    assert.ok(pop.includes(selected));
  });

  it('rank returns an organism from the population', () => {
    const rng = new Mulberry32(42);
    const pop = makePop();
    const selected = rankSelection(pop, rng);
    assert.ok(pop.includes(selected));
  });

  it('elite returns top N organisms', () => {
    const pop = makePop();
    const elites = eliteSelection(pop, 2);
    assert.equal(elites.length, 2);
    assert.equal(elites[0].fitness, 80);
    assert.equal(elites[1].fitness, 50);
  });

  it('elite with count > pop returns all', () => {
    const pop = makePop();
    const elites = eliteSelection(pop, 100);
    assert.equal(elites.length, 5);
  });
});
