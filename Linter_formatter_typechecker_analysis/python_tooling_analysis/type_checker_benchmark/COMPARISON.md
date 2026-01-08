

# Type Checker Comparative Analysis

This document summarizes the comparative evaluation of Python type checkers across correctness, speed, architecture, determinism, and memory usage.

Two complementary codebases were used:

1. A **controlled synthetic test bench** with known ground truth
2. A **real-world standard library workload** (CPython)

The goal is to expose **design trade-offs**, not to declare a single universal winner.

---

## Codebases Used

### 1. Synthetic Test Bench

Directory:

cpython-src/Python-3.10.19/Lib


Characteristics:

- Large, production-grade codebase
- No ground truth
- Realistic dependency graph
- Heterogeneous coding styles

Used to measure:

- End-to-end runtime
- Scalability
- Memory pressure
- Determinism under load

This workload reflects **practical CI and developer usage**, complementing the synthetic benchmark.

---

## Evaluation Dimensions

The following dimensions were considered:

- **Coverage (TP / FN)** — synthetic benchmark only
- **Speed** — CPython standard library
- **Architecture** — daemon vs non-daemon
- **Incrementality** — reuse of analysis state
- **Determinism** — stability across repeated runs
- **Memory Usage** — relative footprint during analysis

---

## Comparative Table

| Tool                       | Architecture                     | Primary Optimization Target   | Coverage (TP / 11) | Avg Speed (CPython Lib) | Incremental / Live | Determinism    | Memory Usage        | Best Fit                      |
| -------------------------- | -------------------------------- | ----------------------------- | ------------------ | ----------------------- | ------------------ | -------------- | ------------------- | ----------------------------- |
| **mypy**             | Non-daemon (batch)               | CI, predictable static checks | **10 / 11**  | **0.165s**        | No                 | **High** | **Low**       | CI pipelines, large repos     |
| **pyre**             | Daemon-based                     | Whole-program strict typing   | **10 / 11**  | 0.649s                  | Yes                | Medium–High   | Medium–High        | Monorepos, strict typing orgs |
| **pyright (CLI)**    | Non-daemon (editor-first design) | IDE diagnostics               | **10 / 11**  | 72.8s                   | No                 | High           | Medium              | Secondary batch usage         |
| **Pylance (editor)** | Daemon (LSP)                     | Live typing feedback          | **10 / 11*** | ~instant                | Yes                | Medium         | Medium–High        | Editor workflows              |
| **pytype**           | Non-daemon (inference-first)     | Type inference research       | **1 / 11**   | 27.1s                   | No                 | **High** | Medium              | Inference exploration         |
| **pyanalyze**        | Non-daemon (exec + static)       | Semantic correctness          | **9 / 11**   | 945.9s                  | No                 | **Low**  | **Very High** | Research / deep audits        |

\* Pylance coverage inferred from the pyright engine; editor mode was not benchmarked separately.

---

## Architectural Interpretation

### Non-daemon tools

- Start fresh on every run
- Highly deterministic
- Low memory overhead
- Favor reproducibility and CI stability

Examples: mypy, pytype, pyanalyze

---

### Daemon-based tools

- Maintain long-lived background state
- Enable incremental and interactive analysis
- Trade memory for responsiveness
- Favor large codebases and editor workflows

Examples: pyre, Pylance

---

## Key Observations

- **mypy** provides the best balance of speed, determinism, and correctness for CI usage on both synthetic and real-world codebases.
- **pyre** matches mypy’s detection capability while benefiting from daemon-based whole-program analysis, at the cost of higher configuration and memory usage.
- **pyright / Pylance** prioritize developer experience and flow-sensitive analysis, explaining strong editor performance but poor CLI scalability.
- **pytype** is not designed for exhaustive error reporting in a single run; early termination reflects a deliberate soundness trade-off.
- **pyanalyze** offers deep semantic analysis but exhibits extreme runtime variance and memory consumption, limiting its practicality for large codebases.

---

## Final Verdict

No single type checker dominates all evaluation axes.

The synthetic test bench establishes **capability boundaries**, while the CPython standard library benchmark establishes **scalability and practicality**. Together, they confirm that each tool’s behavior aligns with its documented design goals and architectural choices.

This benchmark therefore serves as a **comparative lens**, not a ranking system.
