# mypy — Type Checker Benchmark Results

## Summary

- **Total expected issues:** 11
- **True Positives (TP):** 10
- **False Negatives (FN):** 1

---

## Detected Issues (True Positives)

### Basic

- Wrong return type
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

- Incorrect type narrowing

---

## Missed Issues (False Negatives)

### Control Flow

- Unreachable branch (`NoReturn`-based reachability)

---

## Notes

- mypy shows **strong coverage** for basic and advanced typing errors.
- It correctly handles protocols, generics, variance, and TypedDicts.
- Control-flow reachability analysis is **conservative**, which explains the missed unreachable-branch case.
- Informational notes and suggestions emitted by mypy were recorded but **not used** for scoring.

---

## Score (TP-based)

Score = 10 / 11
