'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { EventEmitter } = require('../src/events');

describe('EventEmitter', () => {
  it('emits and receives events', () => {
    const ee = new EventEmitter();
    let received = null;
    ee.on('test', (data) => { received = data; });
    ee.emit('test', 42);
    assert.equal(received, 42);
  });

  it('supports multiple listeners', () => {
    const ee = new EventEmitter();
    const calls = [];
    ee.on('x', () => calls.push('a'));
    ee.on('x', () => calls.push('b'));
    ee.emit('x');
    assert.deepEqual(calls, ['a', 'b']);
  });

  it('off removes a specific listener', () => {
    const ee = new EventEmitter();
    let count = 0;
    const fn = () => { count++; };
    ee.on('x', fn);
    ee.emit('x');
    ee.off('x', fn);
    ee.emit('x');
    assert.equal(count, 1);
  });

  it('once fires only once', () => {
    const ee = new EventEmitter();
    let count = 0;
    ee.once('x', () => { count++; });
    ee.emit('x');
    ee.emit('x');
    assert.equal(count, 1);
  });

  it('wildcard listener receives all events', () => {
    const ee = new EventEmitter();
    const events = [];
    ee.on('*', (name, data) => events.push({ name, data }));
    ee.emit('a', 1);
    ee.emit('b', 2);
    assert.equal(events.length, 2);
    assert.equal(events[0].name, 'a');
    assert.equal(events[1].name, 'b');
  });

  it('listenerCount returns correct count', () => {
    const ee = new EventEmitter();
    assert.equal(ee.listenerCount('x'), 0);
    ee.on('x', () => {});
    ee.on('x', () => {});
    assert.equal(ee.listenerCount('x'), 2);
  });

  it('off without fn removes all listeners for event', () => {
    const ee = new EventEmitter();
    ee.on('x', () => {});
    ee.on('x', () => {});
    ee.off('x');
    assert.equal(ee.listenerCount('x'), 0);
  });
});
