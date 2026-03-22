'use strict';

function tournamentSelection(population, rng, tournamentSize = 3) {
  let best = null;
  for (let i = 0; i < tournamentSize; i++) {
    const idx = rng.nextInt(0, population.length);
    const candidate = population[idx];
    if (best === null || candidate.fitness > best.fitness) {
      best = candidate;
    }
  }
  return best;
}

function rouletteSelection(population, rng) {
  const minFitness = Math.min(...population.map((o) => o.fitness));
  const offset = minFitness < 0 ? -minFitness : 0;
  const totalFitness = population.reduce((s, o) => s + o.fitness + offset, 0);
  if (totalFitness === 0) {
    return population[rng.nextInt(0, population.length)];
  }
  let spin = rng.next() * totalFitness;
  for (const org of population) {
    spin -= org.fitness + offset;
    if (spin <= 0) return org;
  }
  return population[population.length - 1];
}

function rankSelection(population, rng) {
  const sorted = [...population].sort((a, b) => a.fitness - b.fitness);
  const n = sorted.length;
  const totalRank = (n * (n + 1)) / 2;
  let spin = rng.next() * totalRank;
  for (let i = 0; i < n; i++) {
    spin -= i + 1;
    if (spin <= 0) return sorted[i];
  }
  return sorted[n - 1];
}

function eliteSelection(population, count) {
  const sorted = [...population].sort((a, b) => b.fitness - a.fitness);
  return sorted.slice(0, count);
}

const STRATEGIES = {
  tournament: tournamentSelection,
  roulette: rouletteSelection,
  rank: rankSelection,
};

module.exports = {
  tournamentSelection,
  rouletteSelection,
  rankSelection,
  eliteSelection,
  STRATEGIES,
};
