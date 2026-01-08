# Type Checker Benchmark (Python)

This repository is a purpose-built benchmark suite for evaluating Python static type checkers in a controlled, minimal, and reproducible manner.

The benchmark answers one precise question:

Given a known set of intentional typing errors, how accurately do different type checkers detect them?

## Scope

This benchmark evaluates the following Python type checkers:

mypy
pyright (Pylance backend)
pytype
pyre
pyanalyze

Only static type analysis is evaluated. Runtime behavior, IDE features, and performance are out of scope.

## Core Principles

### One file → one type error

Each test file contains exactly one intentional typing error. This guarantees no cascading failures, no ambiguous diagnostics, and clear attribution of detections.

### Explicit ground truth

All expected typing errors are declared upfront in expected/ground_truth.json. This file is the single source of truth used to evaluate true positives and false negatives. Error wording, codes, and locations are ignored. Only capability is measured.

### Separation of concerns

basic  - contains fundamental typing mistakes.
advanced - contains protocols, generics, variance, and TypedDict errors.
control_flow - contains flow-sensitive typing and narrowing errors.
expected -  contains ground truth definitions.
results - contains per-tool analysis reports.

Test files contain no benchmark logic. Benchmark logic contains no test code.

## Error Categories

##### **Basic**
Wrong return type
Argument type mismatch
Assignment type mismatch
Missing return
Optional misuse

##### **Advanced**
Protocol mismatch
Incorrect generic usage
Variance misuse
TypedDict key error

##### **Control Flow**
Unreachable branch (NoReturn)
Incorrect type narrowing

Total errors: 11

## Evaluation Methodology

For each type checker, the tool is run on the benchmark directory, raw output is collected, and detections are compared against expected/ground_truth.json. Results are classified as true positives or false negatives.

The following are explicitly ignored: error wording differences, error codes, severity levels, duplicate diagnostics, performance, and runtime behavior. This benchmark measures coverage, not noise.

## What This Benchmark Is

A precision static type analysis benchmark.
A capability comparison across Python type checkers.
A reproducible research baseline.

## What This Benchmark Is NOT

A real-world codebase.
A performance benchmark.
An IDE comparison.
A runtime correctness test.

The code is intentionally incorrect by design.

## Versioning and Reproducibility

Test cases are stable. Tool versions must be recorded externally. Results are meaningful only when version information is preserved.

This repository benchmarks type checkers, not opinions.
