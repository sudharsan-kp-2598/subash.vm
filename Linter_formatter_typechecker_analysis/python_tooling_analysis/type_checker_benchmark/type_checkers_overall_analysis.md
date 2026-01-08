# Type Checker Benchmark — Analysis Document

## 1. Objective

This benchmark evaluates **static type checker capability and scalability** for Python under controlled and reproducible conditions.

The goal is **not** to declare a universal winner, but to expose **design trade-offs** across tools by measuring:

- Detection capability against known ground truth
- End-to-end performance on a real-world codebase
- Behavioral consistency across categories of typing errors

The benchmark explicitly avoids IDE features, runtime correctness, and developer ergonomics.

---

### 1.1 Non-Goals

This benchmark does **not** attempt to measure:

- Developer UX or editor latency
- IDE integration or live diagnostics
- Annotation burden or adoption cost
- False-positive rates by design
- Formal soundness guarantees

These exclusions are intentional and necessary to preserve scope clarity.

---

## 2. Benchmark Design Overview

Two complementary workloads were used.

### 2.1 Synthetic Ground-Truth Benchmark

- Purpose-built test suite
- Exactly **one intentional typing error per file**
- Total errors: **11**
  - Basic typing: 5
  - Advanced typing: 4
  - Control-flow typing: 2
- Expected errors defined explicitly in `expected/ground_truth.json`

This benchmark measures **reporting coverage only** (TP / FN), independent of error wording, codes, or severity.

Ground truth was manually validated against Python typing specifications and cross-checked across multiple analyzers to ensure intent clarity.

---

### 2.1.1 Error Taxonomy Definition

Each error category is defined by the **minimal type-system feature required to detect the error**, independent of syntax, control-flow structure, or runtime execution.

- **Basic typing errors** require only local type consistency (e.g., return types, argument matching).
- **Advanced typing errors** require higher-order typing features such as generics, protocols, variance, or structural typing.
- **Control-flow typing errors** require flow-sensitive reasoning or type narrowing across branches; reachability is included  **only insofar as it is implied by type annotations such as `NoReturn`** , not as general dead-code analysis. Categories are mutually exclusive by construction.

#### 2.1.2 Error Categories

Errors are grouped based on the **minimal type-system capability required to detect them**, independent of syntax, runtime execution, or stylistic concerns.
Categories are **mutually exclusive by construction**.

---

##### **Basic Typing Errors**

Errors detectable through **local, non–flow-sensitive type consistency checks**.

- Wrong return type
- Argument type mismatch
- Assignment type mismatch
- Missing return
- Optional misuse

---

##### **Advanced Typing Errors**

Errors requiring **higher-order typing features** such as generics, protocols, variance rules, or structural typing.

- Protocol mismatch
- Incorrect generic usage
- Variance misuse
- TypedDict key error

---

##### **Control-Flow Typing Errors**

Errors requiring **flow-sensitive reasoning or reachability analysis** across control paths.

- Incorrect type narrowing
- Unreachable branch (`NoReturn`-based reachability)

---

**Total errors:** 11

---

### 2.2 Real-World Scalability Benchmark

- Codebase: **CPython standard library**
- Measures:
  - End-to-end runtime
  - Determinism across repeated runs
  - Practical scalability under a large, heterogeneous codebase

The CPython standard library was chosen deliberately:

- It is large, import-heavy, and heterogeneous
- It contains incomplete and uneven typing
- It represents a **worst-case scalability workload**, not a typing-pure codebase

This choice stresses analyzers rather than rewarding annotation cleanliness.

### 2.3 Tools Evaluated

The benchmark evaluates the following Python static type checkers:

- **mypy** — reference, spec-driven static type checker
- **pyright** — editor-first, flow-sensitive type checker
- **pyre** — daemon-based, whole-program type checker
- **pyanalyze** — semantic and execution-aware analyzer
- **pytype** — inference-driven, soundness-first analyzer

All tools were evaluated using their default configurations unless otherwise stated.

---

## 3. Experimental Controls

To ensure fairness and reproducibility, the following controls were enforced.

### 3.1 Environment Control

- All tools executed in the same Conda environment
- Same Python minor version (3.12.x)
- Same hardware and OS
- No concurrent workloads during measurement
- For daemon-based tools, end-to-end wall-clock time includes required startup and teardown unless otherwise unavoidable by design.

Performance timings reflect **end-to-end wall-clock execution** under identical conditions.

---

### 3.2 Configuration Control (Critical)

All tools were run using their **default configurations**, without enabling optional strictness flags.

This was a deliberate choice:

- Default mode reflects typical real-world usage
- Strict modes differ significantly across tools
- Enabling tool-specific strictness would introduce asymmetric assumptions
- The benchmark evaluates **capability boundaries**, not maximum-error extraction

---

### 3.3 Scoring Control

- Only **true positives (TP)** and **false negatives (FN)** were counted
- Error wording, codes, severity levels, and suggestions were ignored
- Duplicate diagnostics were collapsed
- Performance and coverage were measured independently

---

### 3.4 Soundness vs Completeness Assumption

This benchmark intentionally evaluates **reporting completeness**, not formal soundness.

Tools that halt or limit analysis to preserve soundness may report fewer errors by design. Such behavior is considered a valid design trade-off and is not treated as a weakness.

---

## 4. Summary of Results

| Tool                | Version    | Avg Speed (s) | Basic (5) | Advanced (4) | Control Flow (2) | Total TP | Total FN |
| ------------------- | ---------- | ------------- | --------- | ------------ | ---------------- | -------- | -------- |
| **mypy**      | 1.19.1     | 0.165         | 5 / 5     | 4 / 4        | 1 / 2            | 10       | 1        |
| **pyre**      | 0.9.25     | 0.649         | 5 / 5     | 4 / 4        | 1 / 2            | 10       | 1        |
| **pyright**   | 1.1.407    | 72.821        | 5 / 5     | 4 / 4        | 1 / 2            | 10       | 1        |
| **pyanalyze** | 0.13.1     | 945.940       | 5 / 5     | 3 / 4        | 1 / 2            | 9        | 2        |
| **pytype**    | 2024.10.11 | 27.112        | 1 / 5     | 0 / 4        | 0 / 2            | 1        | 10       |

---

### 4.1 Inference from Results

### Coverage vs Speed Trade-off

The results reveal a clear separation between **coverage-oriented** and **inference-oriented** type checkers.

- **mypy** and **pyre** achieve high coverage with minimal runtime, favoring batch and CI usage.
- **pyright** matches coverage but incurs significantly higher runtime, reflecting an editor-first architecture.
- **pyanalyze** shows strong basic coverage but extreme runtime variance and reduced advanced coverage.
- **pytype** reports minimal coverage due to early termination after fundamental violations, reflecting a soundness-first design.

---

### Control-Flow and Reachability

All tools detect flow-sensitive type narrowing.

All tools fail to flag unreachable branches introduced by `NoReturn`.

This consistency indicates that unreachable-code detection is intentionally treated as a **linter concern**, not a core type-checking objective.

---

## 5. Category-Level Analysis

### 5.1 Basic Typing Errors

All tools except **pytype** detect all basic typing errors.

This confirms that basic static type checking is mature and standardized.

---

### 5.2 Advanced Typing Constructs

Formal type-system enforcement (generics, protocols, variance) distinguishes spec-driven type checkers from semantic analyzers.

---

### 5.3 Control-Flow Typing

Flow-sensitive narrowing is universally supported; reachability analysis is consistently excluded.

---

### 5.4 Failure Modes and Analysis Continuation

Tools differ in how they behave after encountering unsound or inconsistent states.

- Some tools continue analysis conservatively
- Others terminate early to preserve soundness

The **one-error-per-file** design prevents cascading failures and ensures that early termination does not suppress unrelated detections.

---

## 6. Tool-Specific Behavioral Interpretation

Each tool’s observed behavior aligns closely with its documented design goals.

Low coverage does not imply weakness; high coverage does not imply superior correctness.

---

## 7. Interpretation of Scores

The TP-based score answers a single question:

> *How many predefined typing errors are reported in one default run?*

It is descriptive, not evaluative.

---

## 8. Limitations

- Strict modes were not enabled
- Runtime typing behavior was not evaluated
- Memory usage was not instrumented due to inconsistent reporting semantics across tools
- Only one real-world codebase was used

These limitations are intentional and documented.

---


## Discussions

This section addresses common questions and potential points of confusion arising from the benchmark results.
The intent is to clarify **design intent**, **tool scope**, and **interpretation boundaries**, rather than to rank tools or prescribe usage.

---

### 1. pyanalyze: Design Intent and Adoption

pyanalyze was developed primarily to address internal needs at Dropbox, focusing on detecting **semantic and runtime-adjacent bugs** in large, dynamic, and partially typed Python codebases.

Unlike spec-driven type checkers, pyanalyze does not aim to fully implement the Python typing specification (PEP 484 and successors). Its emphasis is on reasoning about program behavior rather than enforcing formal typing rules.

As a result:

- It is not widely adopted as a general-purpose type checker
- It shows reduced coverage for advanced typing constructs
- Its performance characteristics reflect deep semantic analysis rather than typing-spec validation

Its lower coverage in this benchmark reflects **intentional design trade-offs**, not incomplete implementation.

---

### 2. pyre: Daemon-Based Incremental Analysis

pyre is explicitly designed for **large monorepos** and **incremental development workflows**.

Pyre runs as a persistent daemon that:

- Maintains a session-wide type environment
- Caches dependency graphs
- Re-analyzes only changed files and their dependents

While the initial run requires full analysis, subsequent checks amortize this cost.
In cold, one-shot benchmarks, this design advantage is not fully visible, but it is central to pyre’s relevance in large-scale production environments.

---

### 3. pytype: Early Termination and Soundness

pytype is an inference-driven, soundness-first analyzer.

It builds a **globally consistent inferred type model**. When an early type inconsistency invalidates this model, pytype intentionally limits or terminates further analysis to avoid propagating unsound assumptions.

This behavior results in:

- Very low false-positive rates
- Reduced total error reporting
- Early termination after fundamental violations

This is a deliberate design choice aligned with formal soundness principles.

---

### 4. Practical Relevance of pytype Today

Pytype originated in the mid-2010s, when most Python codebases were largely unannotated. Its goal was to detect real bugs in such environments without requiring full annotation coverage.

Today, pytype remains relevant in:

- Large legacy codebases
- Environments prioritizing soundness over coverage
- Internal tooling where inferred correctness is more important than typing-spec compliance

Its limited adoption reflects ecosystem evolution, not obsolescence.

---

### 5. Why pytype Is Not a Competitor to mypy or pyright

mypy and pyright are **spec-driven tools**.

They answer:

> “Does this code conform to the Python typing specification?”

pytype answers:

> “Can this code be proven type-safe under all executions?”

These are fundamentally different questions.
As a result, pytype is not positioned as a direct competitor to mypy or pyright.

---

### 6. Why Full Coverage Is Necessary for mypy and pyright

For spec-driven type checkers, near-complete reporting coverage is essential because they serve as:

- CI gatekeepers
- Specification enforcers
- Regression detectors

To maintain coverage, these tools:

- Continue analysis after errors
- Insert conservative fallback types (e.g., `Any`)
- Accept limited unsoundness in favor of completeness

This behavior is required for real-world development workflows.

---

### 7. Soundness vs Practicality: Is pytype “Better”?

From a **formal correctness** standpoint, pytype’s refusal to speculate is principled and defensible.

From a **workflow and ecosystem** standpoint, mypy and pyright are more practical:

- They provide continuous feedback
- They integrate cleanly with CI
- They scale to team-based development

The ecosystem largely prioritizes **developer productivity and coverage** over absolute soundness, which explains the dominance of mypy and pyright.

---

### 8. Relevance of mypy in a pyright-Dominated Editor World

Although pyright is deeply integrated into VS Code through Pylance, mypy remains relevant because it functions as:

- The de facto reference for typing behavior
- A stable, deterministic CI checker
- The standard tool for validating type stubs and library annotations

Editor dominance does not eliminate the need for a **spec-aligned, editor-agnostic CI tool**.

---

### 9. Type Stubs and Their Importance

A **type stub** (`.pyi` file) defines the type signatures of a module without providing runtime implementation.

Stubs are critical for:

- Legacy or unannotated code
- C extensions and native modules
- Stable API contracts with changing implementations

Correctness of stubs is essential, as incorrect stubs silently undermine type checking guarantees.

---

### 10. Why CI Type Checking Is Still Required

Passing type checks in an editor is **necessary but not sufficient**.

Editor analysis:

- Is incremental and contextual
- May skip files or paths
- Uses per-user configuration

CI analysis:

- Runs from a clean state
- Enforces shared configuration
- Guarantees project-wide consistency

CI type checking is therefore required to provide a **single authoritative correctness gate**.

---

## Summary

The benchmark results reflect **intentional, principled design trade-offs** across tools.

- High coverage does not imply superior correctness
- Low coverage does not imply weakness
- Tools differ because they optimize for different correctness definitions

These differences should be understood as **complementary philosophies**, not competitive failures.

## 9. Conclusion

This benchmark demonstrates that Python type checkers make **deliberate, principled trade-offs**.

The results should be read as a **comparative lens**, not a ranking.

Each tool performs exactly as its design philosophy predicts.
