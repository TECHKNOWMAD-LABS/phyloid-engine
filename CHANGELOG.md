# Changelog

## v0.1.0 — 2026-03-23

First release after 8 Edgecraft autonomous iteration cycles.

### Cycle 1: Test Coverage
- Created `conftest.py` with shared fixtures and mock helpers
- Added comprehensive test suites for all 8 modules (prng, organism, events,
  selection, mutation, crossover, paradigm, engine)
- Expanded test count from 26 to 159 covering edge cases, boundary conditions,
  serialization roundtrips, and determinism verification

### Cycle 2: Error Hardening
- Added input validation across all modules:
  - PRNG: seed type validation, next_int range validation
  - Organism: bounds checking for get/set_gene, from_dict validation,
    random() length and gene bounds validation
  - Selection: empty population rejection, tournament size validation
  - Crossover: minimum genome length enforcement
  - Engine: config validation (population_size, genome_length, elite_count)
- 23 error-hardening tests verifying all validation paths

### Cycle 3: Performance
- Optimized `_update_best` to use `max()` and only clone on improvement
- Single-pass `_gen_stats` (min/max/sum in one loop)
- Cached config values and function references as locals in `step()`
- Verified 500x50 population completes under 5 seconds

### Cycle 4: Security
- Full security audit: 0 findings across Python and JavaScript source
- No hardcoded secrets, injection vectors, file I/O, or external dependencies
- Created SECURITY.md documenting audit results and recommendations

### Cycle 5: CI/CD
- GitHub Actions CI with Python 3.12 (ruff lint + pytest + coverage)
  and Node.js 22 test runner on push/PR to main
- Pre-commit config with ruff linter and formatter hooks

### Cycle 6: Property-Based Testing
- 18 Hypothesis property tests covering core invariants:
  - PRNG output range, determinism, next_int bounds, reset
  - Serialization roundtrip, clone independence
  - Mutation immutability, swap conservation, gaussian bounds
  - Crossover child length, gene conservation, parent immutability
  - Selection membership, elite ordering
  - Engine population size invariant, best-organism correctness

### Cycle 7: Examples & Docs
- Three working examples: basic evolution, multi-objective optimization,
  custom genetic operators
- Complete docstrings for all public classes and functions

### Cycle 8: Release Engineering
- Updated pyproject.toml with author metadata
- Created Makefile with test, lint, format, security, clean targets
- Created CHANGELOG.md, AGENTS.md, EVOLUTION.md
- Tagged v0.1.0
