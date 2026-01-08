
# Pyre — Type Checker Benchmark Results

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

- Pyre is a **configuration-driven, daemon-based** static type checker.
- It performs **whole-program analysis** using declared types and does not rely on runtime execution.
- Pyre shows **excellent coverage** for basic and advanced typing constructs, including generics, variance rules, protocols, and TypedDict validation.
- Progress logs, worker setup messages, and environment diagnostics were recorded but **ignored for scoring**.
- Pyre does not flag unreachable code resulting from `NoReturn`, indicating limited reachability analysis.
- Diagnostics are strict and precise but intentionally scoped to type soundness rather than control-flow warnings.

---

## Score (TP-based)

**Score = 10 / 11**
