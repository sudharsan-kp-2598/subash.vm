# Linter Benchmark

This repository is a **purpose-built benchmark suite** for evaluating Python linters in a
**controlled, minimal, and reproducible** manner.

The benchmark answers one question precisely:

> Given a known set of issues, how accurately, consistently, and efficiently does a linter detect them?

---

## Core Principles

### 1. One file → one issue

Each test file contains **exactly one intentional issue**.

This guarantees:

- No rule interaction ambiguity
- Clear attribution of detections
- Clean false-positive / false-negative analysis

---

### 2. Explicit ground truth

All expected findings are declared upfront in:

expected/ground_truth.json

This file is the **single source of truth** used to evaluate:

- True positives
- False positives
- False negatives

No heuristic matching. No guessing.

---

### 3. Separation of concerns

| Component         | Responsibility                     |
| ----------------- | ---------------------------------- |
| `code_quality/` | Code quality violations            |
| `security/`     | Security vulnerabilities           |
| `expected/`     | Ground truth definitions           |
| `runner/`       | Execution and result normalization |

Test cases never contain benchmark logic.
Runner logic never encodes expectations.

---


## Directory Structure

```text
linter-benchmark/
│
├── code_quality/
├── security/
├── expected/
├── runner/
└── README.md
```


---

## Issue Coverage

### Code Quality (8)

- Unused imports
- Import cycles
- Undefined variables
- Variable shadowing
- Mutable default arguments
- Bad comparisons
- Dead code
- High cyclomatic complexity

### Security (7)

- `eval` / `exec` usage
- Subprocess shell injection
- Unsafe deserialization
- Weak cryptography
- Hardcoded secrets
- Insecure temporary files
- Path traversal

**Total issues: 15**
----------------

## What This Benchmark Is

- A precision static-analysis benchmark
- A research-oriented evaluation suite
- A reproducible baseline for linter comparison

---

## What This Benchmark Is NOT

- A real-world codebase
- A formatter benchmark
- A style-guide test
- A dynamic analysis suite

The code is intentionally *bad* — by design.

---

## Versioning Philosophy

- Test cases remain stable
- Linters and configs are frozen externally
- Results are meaningful only when versions are recorded

This ensures reproducibility and auditability.

---

**This repository benchmarks linters — not opinions.**
