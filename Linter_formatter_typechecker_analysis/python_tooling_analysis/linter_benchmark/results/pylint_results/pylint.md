

# Pylint — Linter Benchmark Results

This document records Pylint’s performance against a fixed benchmark
of **15 known issues** (8 code quality + 7 security).

Only **True Positives (TP)** and **False Negatives (FN)** are considered.
Style, documentation, and naming warnings are ignored.

---

## Summary

- **Total expected issues:** 15
- **True Positives (TP):** 8
- **False Negatives (FN):** 7

---

## Detected Issues (True Positives)

### Code Quality

1. Unused imports (`unused-import`)
2. Undefined variables (`undefined-variable`)
3. Dead code (`unreachable`)
4. Mutable default arguments (`dangerous-default-value`)
5. Variable shadowing (`redefined-outer-name`)
6. Bad comparisons (`literal-comparison`)
7. High cyclomatic complexity (`too-many-return-statements`)

### Security

8. `eval` / `exec` usage (`eval-used`)

---

## Missed Issues (False Negatives)

### Code Quality

9. Import cycles

### Security

10. Subprocess shell injection
11. Unsafe deserialization
12. Weak cryptography
13. Hardcoded secrets
14. Insecure temporary files
15. Path traversal

---

## Score (TP-based)

Score = 8 / 15


## Notes

- Pylint has **broad static analysis coverage**
- It detects many structural code-quality issues
- Security coverage is **very limited**
- Pylint numeric score (e.g., 0.34/10) is recorded separately and **not used** in benchmarking
