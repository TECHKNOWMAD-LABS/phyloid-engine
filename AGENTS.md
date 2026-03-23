# AGENTS.md — Autonomous Development Protocol

## Edgecraft Protocol

This repository was developed using the **Edgecraft Protocol**, an autonomous
iterative development methodology that applies 8 structured improvement cycles
to a codebase. Each cycle targets a specific quality dimension.

### Layer Model (L0-L7)

| Layer | Name | Purpose |
|-------|------|---------|
| L0 | attention | Initial focus and context gathering |
| L1 | detection | Identify gaps, missing coverage, or weaknesses |
| L2 | noise | Security scanning and noise filtering |
| L3 | sub-noise | Edge cases, subtle bugs, and boundary conditions |
| L4 | conjecture | Performance hypotheses and optimization targets |
| L5 | action | Implementation of fixes, features, and improvements |
| L6 | grounding | Verification with measurements and test results |
| L7 | flywheel | Patterns that transfer to other repositories |

### Cycle Sequence

1. **Test Coverage** — Identify untested modules, create shared fixtures, write comprehensive tests
2. **Error Hardening** — Break the code with adversarial inputs, add validation and error handling
3. **Performance** — Profile bottlenecks, optimize hot paths, measure before/after
4. **Security** — Scan for secrets, injection vectors, dependency risks
5. **CI/CD** — Automated testing and linting on every push/PR
6. **Property-Based Testing** — Hypothesis-driven invariant testing
7. **Examples & Docs** — Working examples and complete docstring coverage
8. **Release Engineering** — Metadata, changelog, tooling, tagging

### Commit Convention

Every commit message starts with an Edgecraft layer prefix:

```
L1/detection: identify untested modules at 0% coverage
L5/action: add test suite for [module] — N tests
L6/grounding: N tests passing, coverage improved to N%
L3/sub-noise: [input] causes [error] in [module]
L2/noise: security scan — N findings, M false positives
L4/conjecture: parallelizing N calls will yield Nx speedup
L7/flywheel: pattern applicable to [other repos]
```

### Agent Configuration

- **Model**: Claude Opus 4.6
- **Execution**: Fully autonomous — no human interaction during cycles
- **Git identity**: TechKnowMad Labs <admin@techknowmad.ai>
- **Push strategy**: Push after each cycle completion
- **Error handling**: Log failures, continue to next step

### Quality Gates

- All tests must pass before committing
- Every commit must have a meaningful diff
- No empty commits, no whitespace-only commits
- Test failures are fixed before proceeding
