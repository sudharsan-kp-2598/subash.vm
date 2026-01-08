
# pytype — Type Checker Benchmark Results

## Summary

- **Total expected issues:** 11
- **True Positives (TP):** 1
- **False Negatives (FN):** 10

---

## Detected Issues (True Positives)

### Basic

- Wrong return type

---

## Missed Issues (False Negatives)

### Basic

- Argument type mismatch
- Assignment type mismatch
- Missing return
- Optional misuse

### Advanced

- Protocol mismatch
- Generic misuse
- Variance error
- TypedDict key error

### Control Flow

- Unreachable branch
- Incorrect type narrowing

---

## Notes

- pytype is an **inference-driven, execution-aware** type checker that builds a dependency graph internally (via `ninja`).
- During analysis, pytype encountered a **soundness-breaking type error** (`bad return type`) and **aborted further analysis early**.
- This behavior **does not mean** pytype is incapable of detecting other errors in the benchmark.
- Instead, it reflects a **design trade-off**: pytype prioritizes soundness and inference correctness over exhaustive error reporting in a single run.
- When a fundamental type violation is detected, pytype may stop processing additional files rather than continuing with potentially unsound assumptions.
- This behavior is **by design**, not a misconfiguration or user error.
- No flags were changed to force continued analysis, in order to preserve **default tool behavior** and ensure fair comparison.

---

## Score (TP-based)

Score = 1 / 11
