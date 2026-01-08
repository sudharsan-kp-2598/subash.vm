

# pyanalyze — Type Checker Benchmark Results

## Summary

- **Total expected issues:** 11
- **True Positives (TP):** 9
- **False Negatives (FN):** 2

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
- TypedDict key error

### Control Flow

- Incorrect type narrowing

---

## Missed Issues (False Negatives)

### Advanced

- Variance error

### Control Flow

- Unreachable branch

---

## Notes

- pyanalyze **executes modules during analysis**, unlike mypy or pyright.
- Several detections surfaced as `import_failed` due to runtime `TypeError`s.
- These import-time failures were **counted as valid detections** because they directly expose the intended typing violations.
- pyanalyze shows strong correctness checks but is sensitive to top-level executable code.
- Control-flow reachability and variance handling are weaker compared to mypy and pyright.

---

## Score (TP-based)

Score = 9 / 11
