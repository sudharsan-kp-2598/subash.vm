

# Pyflakes — Linter Benchmark Results

This document records Pyflakes’ performance against a fixed benchmark
of **15 known issues** (8 code quality + 7 security).

Only **True Positives (TP)** and **False Negatives (FN)** are considered.

---

## Summary

- **Total expected issues:** 15
- **True Positives (TP):** 3
- **False Negatives (FN):** 12

---

## Detected Issues (True Positives)

### Code Quality

1. Unused imports
2. Undefined variables
3. Bad comparisons (`is` vs `==`)

---

## Missed Issues (False Negatives)

### Code Quality

4. Import cycles
5. Variable shadowing
6. Mutable default arguments
7. Dead code
8. High cyclomatic complexity

### Security

9. `eval` / `exec` usage
10. Subprocess shell injection
11. Unsafe deserialization
12. Weak cryptography
13. Hardcoded secrets
14. Insecure temporary files
15. Path traversal

---

## Score (TP-based)

Score = 3 / 15

## Notes

- Pyflakes focuses on **simple, fast name-based static checks**
- No control-flow, complexity, or security analysis
- Very low noise, but limited coverage
