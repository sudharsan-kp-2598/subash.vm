
# pyright — Type Checker Benchmark Results

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

- pyright performs **flow-sensitive, strict static type analysis**.
- It provides precise diagnostics for generics, variance, protocols, and TypedDicts.
- Suggestions (e.g., recommending `Sequence` for covariance) were recorded but not used for scoring.
- pyright does not report unreachable code caused by `NoReturn` under default settings.
- No warnings or informational diagnostics were counted toward results.

---

## Score (TP-based)

Score = 10 / 11
