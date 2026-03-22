'use strict';

class ParadigmJudge {
  constructor(name, evaluateFn, weight = 1.0) {
    this.name = name;
    this._evaluate = evaluateFn;
    this.weight = weight;
  }

  evaluate(organism) {
    return this._evaluate(organism);
  }
}

class ParadigmPanel {
  constructor() {
    this._judges = [];
  }

  addJudge(judge) {
    this._judges.push(judge);
    return this;
  }

  removeJudge(name) {
    this._judges = this._judges.filter((j) => j.name !== name);
    return this;
  }

  getJudge(name) {
    return this._judges.find((j) => j.name === name) ?? null;
  }

  get judges() {
    return [...this._judges];
  }

  evaluate(organism) {
    if (this._judges.length === 0) return 0;
    let totalWeight = 0;
    let totalScore = 0;
    const scores = {};
    for (const judge of this._judges) {
      const score = judge.evaluate(organism);
      scores[judge.name] = score;
      totalScore += score * judge.weight;
      totalWeight += judge.weight;
    }
    const aggregate = totalWeight > 0 ? totalScore / totalWeight : 0;
    return { scores, aggregate };
  }

  evaluatePopulation(population) {
    for (const org of population) {
      const result = this.evaluate(org);
      org.fitness = result.aggregate;
      org.meta.paradigmScores = result.scores;
    }
    return population;
  }
}

module.exports = { ParadigmJudge, ParadigmPanel };
