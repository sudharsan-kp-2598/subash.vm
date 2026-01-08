

# Ruff — Linter Benchmark Results

This document records Ruff’s performance against the fixed benchmark
of **15 known issues** (8 code quality + 7 security).

Evaluation considers **only**:

- True Positives (TP)
- False Negatives (FN)

False Positives are intentionally ignored for this phase.

---

## Summary

- **Total expected issues:** 15
- **True Positives (TP):** 3
- **False Negatives (FN):** 12

---

## Detected Issues (True Positives)

### Code Quality

1. **Unused imports**

   - Detected via `F401`
2. **Undefined variables**

   - Detected via `F821`
3. **Bad comparisons** (`is` vs `==`)

   - Detected via `F632`

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

## Notes

- Ruff focuses on **fast, local, syntactic correctness**
- It does **not** perform:
  - control-flow analysis
  - dependency graph analysis
  - security analysis
- Results are consistent with Ruff’s design goals

---

## Score (TP-based)

Score = 3 / 15

Ruff detects **20%** of the benchmarked issues.
