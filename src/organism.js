'use strict';

class Organism {
  constructor(genome, fitness = 0) {
    this.genome = Array.isArray(genome) ? [...genome] : [];
    this.fitness = fitness;
    this.age = 0;
    this.meta = {};
  }

  clone() {
    const copy = new Organism([...this.genome], this.fitness);
    copy.age = this.age;
    copy.meta = { ...this.meta };
    return copy;
  }

  size() {
    return this.genome.length;
  }

  getGene(index) {
    return this.genome[index];
  }

  setGene(index, value) {
    this.genome[index] = value;
  }

  toJSON() {
    return {
      genome: this.genome,
      fitness: this.fitness,
      age: this.age,
      meta: this.meta,
    };
  }

  static fromJSON(obj) {
    const o = new Organism(obj.genome, obj.fitness);
    o.age = obj.age ?? 0;
    o.meta = obj.meta ?? {};
    return o;
  }

  static random(length, rng, geneMin = 0, geneMax = 1) {
    const genome = [];
    for (let i = 0; i < length; i++) {
      genome.push(geneMin + rng.next() * (geneMax - geneMin));
    }
    return new Organism(genome);
  }
}

module.exports = { Organism };
