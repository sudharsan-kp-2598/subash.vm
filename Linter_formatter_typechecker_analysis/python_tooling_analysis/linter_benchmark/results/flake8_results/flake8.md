

# Flake8 — Linter Benchmark Results

This document records Flake8’s performance against a fixed benchmark
of **15 known issues** (8 code quality + 7 security).

Only **True Positives (TP)** and **False Negatives (FN)** are considered.
Formatting and style warnings (e.g., E302) are ignored.

---

## Summary

- **Total expected issues:** 15
- **True Positives (TP):** 3
- **False Negatives (FN):** 12

---

## Detected Issues (True Positives)

### Code Quality

1. Unused imports (`F401`)
2. Undefined variables (`F821`)
3. Bad comparisons (`F632`)

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

- Flake8 emitted several **formatting and style warnings**, which were
  **recorded but explicitly ignored** for benchmarking purposes.
- Ignored warnings include:

  - `E302`: expected 2 blank lines, found 1
    - Reported in multiple files across both `code_quality/` and `security/`
    - Purely a **PEP 8 formatting rule**
    - No semantic or security relevance
- Files where formatting warnings were observed (non-exhaustive):

  - `code_quality/import_cycles/import_cycle_a.py`
  - `code_quality/import_cycles/import_cycle_b.py`
  - `code_quality/shadowing.py`
  - `code_quality/unused_imports.py`
  - `security/insecure_temp_files.py`
  - `security/path_traversal.py`
  - `security/subprocess_shell_injection.py`
  - `security/unsafe_deserialization.py`
  - `security/weak_cryptography.py`
- These warnings were:

  - **Not counted as True Positives**
  - **Not counted as False Positives**
  - **Not counted as False Negatives**
- Reason for exclusion:

  - The benchmark evaluates **semantic correctness and security issues**
  - Formatting/style findings do not correspond to any planted ground-truth issue
- This behavior is intentional and consistent across all tools.
