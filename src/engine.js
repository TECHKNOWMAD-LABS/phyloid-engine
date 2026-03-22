'use strict';

const { Mulberry32 } = require('./prng');
const { Organism } = require('./organism');
const { tournamentSelection, eliteSelection } = require('./selection');
const { singlePointCrossover } = require('./crossover');
const { gaussianMutation } = require('./mutation');
const { ParadigmPanel } = require('./paradigm');
const { EventEmitter } = require('./events');

const DEFAULTS = {
  populationSize: 100,
  genomeLength: 10,
  geneMin: 0,
  geneMax: 1,
  eliteCount: 2,
  mutationRate: 0.05,
  mutationSigma: 0.1,
  crossoverRate: 0.8,
  tournamentSize: 3,
  maxGenerations: 100,
  targetFitness: Infinity,
  seed: 42,
};

class EvolutionEngine extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...DEFAULTS, ...config };
    this.rng = new Mulberry32(this.config.seed);
    this.panel = new ParadigmPanel();
    this.population = [];
    this.generation = 0;
    this.bestOrganism = null;
    this.stats = { generationHistory: [] };

    this._selectFn = config.selectFn || tournamentSelection;
    this._crossoverFn = config.crossoverFn || singlePointCrossover;
    this._mutateFn = config.mutateFn || gaussianMutation;
    this._fitnessFn = config.fitnessFn || null;
  }

  initialize() {
    this.population = [];
    for (let i = 0; i < this.config.populationSize; i++) {
      this.population.push(
        Organism.random(
          this.config.genomeLength,
          this.rng,
          this.config.geneMin,
          this.config.geneMax
        )
      );
    }
    this.generation = 0;
    this._evaluateAll();
    this.emit('initialized', { population: this.population });
    return this;
  }

  _evaluateAll() {
    if (this._fitnessFn) {
      for (const org of this.population) {
        org.fitness = this._fitnessFn(org);
      }
    }
    if (this.panel.judges.length > 0) {
      this.panel.evaluatePopulation(this.population);
    }
    this._updateBest();
  }

  _updateBest() {
    for (const org of this.population) {
      if (!this.bestOrganism || org.fitness > this.bestOrganism.fitness) {
        this.bestOrganism = org.clone();
      }
    }
  }

  step() {
    const { eliteCount, crossoverRate, mutationRate, mutationSigma, tournamentSize } = this.config;
    const nextPop = [];

    // Elitism
    const elites = eliteSelection(this.population, eliteCount);
    for (const e of elites) {
      const c = e.clone();
      c.age = e.age + 1;
      nextPop.push(c);
    }

    // Fill rest
    while (nextPop.length < this.config.populationSize) {
      const parentA = this._selectFn(this.population, this.rng, tournamentSize);
      const parentB = this._selectFn(this.population, this.rng, tournamentSize);

      let children;
      if (this.rng.next() < crossoverRate) {
        children = this._crossoverFn(parentA, parentB, this.rng);
      } else {
        children = [parentA.clone(), parentB.clone()];
      }

      for (let child of children) {
        child = this._mutateFn(child, this.rng, mutationRate, mutationSigma,
          this.config.geneMin, this.config.geneMax);
        if (nextPop.length < this.config.populationSize) {
          nextPop.push(child);
        }
      }
    }

    this.population = nextPop;
    this.generation++;
    this._evaluateAll();

    const genStats = this._genStats();
    this.stats.generationHistory.push(genStats);
    this.emit('generation', { generation: this.generation, stats: genStats });

    return genStats;
  }

  _genStats() {
    const fitnesses = this.population.map((o) => o.fitness);
    const sum = fitnesses.reduce((a, b) => a + b, 0);
    return {
      generation: this.generation,
      best: Math.max(...fitnesses),
      worst: Math.min(...fitnesses),
      average: sum / fitnesses.length,
      bestOrganism: this.bestOrganism?.clone() ?? null,
    };
  }

  run() {
    if (this.population.length === 0) this.initialize();

    this.emit('started', { config: this.config });

    while (this.generation < this.config.maxGenerations) {
      const stats = this.step();
      if (stats.best >= this.config.targetFitness) {
        this.emit('targetReached', stats);
        break;
      }
    }

    const result = {
      generations: this.generation,
      best: this.bestOrganism?.clone() ?? null,
      stats: this.stats,
    };
    this.emit('completed', result);
    return result;
  }
}

module.exports = { EvolutionEngine, DEFAULTS };
