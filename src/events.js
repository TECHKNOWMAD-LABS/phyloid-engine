'use strict';

class EventEmitter {
  constructor() {
    this._listeners = new Map();
    this._once = new Set();
  }

  on(event, fn) {
    if (!this._listeners.has(event)) {
      this._listeners.set(event, []);
    }
    this._listeners.get(event).push(fn);
    return this;
  }

  once(event, fn) {
    this._once.add(fn);
    return this.on(event, fn);
  }

  off(event, fn) {
    if (!this._listeners.has(event)) return this;
    if (fn) {
      const fns = this._listeners.get(event).filter((f) => f !== fn);
      this._listeners.set(event, fns);
    } else {
      this._listeners.delete(event);
    }
    return this;
  }

  emit(event, ...args) {
    const fns = this._listeners.get(event) || [];
    const wildcard = this._listeners.get('*') || [];
    for (const fn of [...fns]) {
      fn(...args);
      if (this._once.has(fn)) {
        this.off(event, fn);
        this._once.delete(fn);
      }
    }
    for (const fn of [...wildcard]) {
      fn(event, ...args);
      if (this._once.has(fn)) {
        this.off('*', fn);
        this._once.delete(fn);
      }
    }
    return this;
  }

  listenerCount(event) {
    return (this._listeners.get(event) || []).length;
  }
}

module.exports = { EventEmitter };
