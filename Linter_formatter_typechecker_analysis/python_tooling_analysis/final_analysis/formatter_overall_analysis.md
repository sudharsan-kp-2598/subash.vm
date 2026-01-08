# Formatter Benchmark — Analysis Document

## 1. Objective

This benchmark evaluates **Python code formatter performance, robustness, and safety guarantees**
under controlled and reproducible conditions.

The goal is **not** to assess formatting style or readability, but to measure
*objective operational properties* of Python formatters by analyzing:

- End-to-end formatting speed on a large real-world codebase
- Idempotence under repeated application
- Failure behavior when encountering invalid or unsupported source files

The benchmark intentionally avoids stylistic judgment and focuses solely on
measurable, reproducible behavior.

---

### 1.1 Non-Goals

This benchmark does **not** attempt to measure:

- Formatting aesthetics or style quality
- Readability or human preference
- Semantic correctness of reformatted code
- Cross-platform determinism
- IDE or editor integration

These exclusions are deliberate to preserve objectivity.

---

## 2. Benchmark Design Overview

Two complementary benchmarks were used.

---

### 2.1 Speed Benchmark

**Target codebase**

- CPython 3.10.19 standard library (`Lib/`)

**Measured metrics**

- Cold-run wall-clock time
- Warm-run wall-clock time (3 repeated runs)
- Number of files processed before failure (if any)

All runs were executed from a clean filesystem state.
No files were pre-filtered or excluded.

---

### 2.2 Idempotence Benchmark

A dedicated idempotence verification script was used.

**Method**

1. Apply formatter to an input file
2. Apply the same formatter again to the formatted output
3. Compare results byte-for-byte

Any difference between runs is classified as **non-idempotence**.

---

## 3. Benchmark Design Rationale

### 3.1 Choice of Codebase

The CPython standard library was selected because it:

- Is large (~1700 Python files)
- Is heterogeneous in style and age
- Contains:
  - Python 3 code
  - Python 2–only grammar
  - Invalid encoding declarations
  - Deliberately malformed source files for parser testing

This makes it a **worst-case stress workload**, not a clean formatting target.

---

### 3.2 Failure Handling Policy

Formatter failures were **not treated as benchmark failures by default**.

Instead:

- Each failure was analyzed individually
- Root causes were documented at file level
- Failures caused by intentionally invalid CPython test fixtures were classified as **expected**

This avoids penalizing correct refusal to process invalid input.

---

## 4. Tools Evaluated

| Tool        | Category             | Implementation               |
| ----------- | -------------------- | ---------------------------- |
| Black       | General formatter    | AST-based (Python, compiled) |
| ruff format | General formatter    | AST-based (Rust)             |
| isort       | Import formatter     | Token-based                  |
| YAPF        | General formatter    | AST-based                    |
| autopep8    | Rule-based formatter | Regex / token-based          |

All tools were evaluated using **default configurations**.


###### Python Code Execution Pipeline

```text
source code
   ↓ tokenize
tokens
   ↓ parse
AST
   ↓ compile
bytecode
   ↓ execute
Python VM
```


---

## 5. Experimental Controls

### 5.1 Environment Control

- Conda environment: `LFT`
- Python version: **CPython 3.12.12**
- Identical hardware and OS
- No concurrent workloads

---

### 5.2 Tool Versions

| Tool     | Version |
| -------- | ------- |
| Black    | 25.12.0 |
| ruff     | 0.14.10 |
| isort    | 7.0.0   |
| YAPF     | 0.43.0  |
| autopep8 | 2.3.2   |

---

## 6. Summary of Results

### 6.1 Speed Benchmark Results

| Formatter   | Cold Run | Warm Run Avg | Files Processed | Status |
| ----------- | -------- | ------------ | --------------- | ------ |
| Black       | 90.7s    | ~103.0s      | 1621            | FAILED |
| ruff format | 0.32s    | ~0.32s       | 1622            | FAILED |
| isort       | 2.69s    | 2.66s        | 1310            | OK     |
| YAPF        | 32.9s    | ~31.4s       | 186             | FAILED |
| autopep8    | 1389.7s  | ~1421.5s     | 1447            | OK     |

Failures are analyzed in Section 8.

---

### 6.2 Idempotence Results

| Formatter   | Idempotent |
| ----------- | ---------- |
| Black       | YES        |
| ruff format | YES        |
| isort       | YES        |
| YAPF        | YES        |
| autopep8    | YES        |

All tools produced identical output on repeated runs.

---

## 7. Performance Analysis

### 7.1 Observed Performance Characteristics

- `ruff format` demonstrates **orders-of-magnitude speed advantage**
- Black exhibits consistent but high runtime cost
- autopep8 shows extreme runtime due to rule-based design
- YAPF’s fail-fast behavior prevents full traversal
- isort performs fast but operates on a limited problem scope

Performance differences align with implementation strategies.

---

## 8. Error Handling and Failure Analysis

This section documents **exact failure causes** at file level.

---

### 8.1 Black Failure Analysis

**Failure point**

- Processed 1621 files before termination

**Failed files (8 total)**

| File                                             | Reason                              |
| ------------------------------------------------ | ----------------------------------- |
| `Lib/lib2to3/tests/data/bom.py`                | Python 2 print statement            |
| `Lib/lib2to3/tests/data/crlf.py`               | Python 2 syntax                     |
| `Lib/lib2to3/tests/data/different_encoding.py` | Python 2 unicode + invalid encoding |
| `Lib/lib2to3/tests/data/false_encoding.py`     | Fake encoding declaration           |
| `Lib/lib2to3/tests/data/py2_test_grammar.py`   | Python 2 grammar (`0L`)           |
| `Lib/test/bad_coding.py`                       | Invalid encoding name               |
| `Lib/test/bad_coding2.py`                      | Deliberately corrupted encoding     |
| `Lib/test/badsyntax_pep3120.py`                | Encoding violation                  |

**Interpretation**
Black correctly refuses to format invalid Python 3 source files.

---

### 8.2 ruff format Failure Analysis

**Failure point**

- Processed 1622 files before termination

**Failed files (10 total)**

| File                                              | Reason                |
| ------------------------------------------------- | --------------------- |
| `Lib/lib2to3/tests/data/bom.py`                 | Python 2 syntax       |
| `Lib/lib2to3/tests/data/crlf.py`                | Python 2 syntax       |
| `Lib/lib2to3/tests/data/different_encoding.py`  | Python 2 unicode      |
| `Lib/lib2to3/tests/data/false_encoding.py`      | Invalid encoding      |
| `Lib/lib2to3/tests/data/py2_test_grammar.py`    | Python 2 grammar      |
| `Lib/test/badsyntax_3131.py`                    | Invalid Unicode token |
| `Lib/test/badsyntax_pep3120.py`                 | Encoding violation    |
| `Lib/test/encoded_modules/module_iso_8859_1.py` | Non-UTF-8 encoding    |
| `Lib/test/encoded_modules/module_koi8_r.py`     | Non-UTF-8 encoding    |
| `Lib/test/test_source_encoding.py`              | Invalid encoding      |

**Interpretation**
ruff format correctly enforces valid Python 3 syntax and UTF-8 input.


###### Formatter Execution Pipeline with Failure Points

```text
source file
   ↓ read file bytes
text decoding (UTF-8 expected)
   ├─ FAILS IF:
   │   • Non-UTF-8 encoded
   │   • Invalid or conflicting encoding declaration
   │   → formatter cannot tokenize
   ↓
tokenize
   ├─ FAILS IF:
   │   • Invalid Unicode tokens
   │   • Malformed byte sequences
   │   → no valid token stream
   ↓
parse
   ├─ FAILS IF:
   │   • Python 2 syntax
   │   • Invalid grammar
   │   → AST cannot be constructed
   ↓
AST
   ↓ format / rewrite
formatted source
```


---

### 8.3 YAPF Failure Analysis

**Failure point**

- Terminated after processing 186 files

**First failing file**

- `Lib/lib2to3/tests/data/different_encoding.py`

**Failure reason**

- Python 2 grammar and legacy unicode literal

**Behavioral explanation**
YAPF follows a **fail-fast parsing model** and aborts on first unsupported file.

**Interpretation**
Early termination reflects design choice, not limited incompatibility.

---

### 8.4 Failure Classification Summary

| Failure Category                    | Count    |
| ----------------------------------- | -------- |
| Python 2–only grammar              | Multiple |
| Invalid encoding declarations       | Multiple |
| Deliberately malformed parser tests | Multiple |

No formatter failed on valid UTF-8 Python 3 source files.

---

## 9. Limitations

- Only one real-world codebase was evaluated
- Cross-platform determinism not measured
- Memory usage not analyzed
- Formatting quality intentionally excluded

These limitations are documented and accepted.

---

# Discussions

This section discusses the key observations and design trade-offs revealed by the formatter benchmark.
The intent is to clarify **why certain tools succeeded or declined**, and how **technical design, operational behavior, and ecosystem factors** influence formatter adoption in practice.

---

## 1. Why did autopep8 become impractical for modern Python codebases despite producing correct formatting output?

autopep8 applies formatting through a large set of incremental, rule-based fixes derived from PEP 8. While this approach produces syntactically correct and standards-compliant output, it does not scale well to large codebases. The benchmark results demonstrate extreme runtime costs on real-world repositories, making autopep8 unsuitable for CI pipelines and large projects. Its decline is therefore driven by **performance limitations**, not formatting correctness.

---

## 2. Why does YAPF terminate early on large, heterogeneous repositories, and how does its fail-fast architecture differ from batch-oriented formatters?

YAPF assumes uniformly valid Python input and treats formatting as a pure AST-to-AST transformation. When AST construction fails—due to Python 2 syntax, invalid encodings, or deliberately malformed files—YAPF aborts immediately. This fail-fast design is appropriate for controlled environments but does not scale to heterogeneous repositories such as CPython, which intentionally contain invalid files. In contrast, batch-oriented formatters are designed to traverse entire trees and tolerate partial incompatibility.

---

## 3. Why do Black and ruff format prioritize full-tree traversal and error accumulation rather than stopping at the first incompatible file?

Black and ruff format are designed for **operational robustness**. Their primary goal is to complete a full formatting pass wherever possible, even in imperfect repositories. By accumulating and reporting multiple failures rather than terminating early, these tools remain usable in CI pipelines and large monorepos. This design choice favors practicality and workflow continuity over strict input assumptions.

---

## 4. Why does idempotence matter for formatters, and how does it prevent long-term diff churn in version control systems?

Idempotence ensures that once code is formatted, subsequent formatter runs produce no further changes. This property is essential for CI enforcement and pre-commit workflows, as it guarantees that formatting introduces a **one-time diff** rather than ongoing churn. The benchmark confirms that all evaluated formatters satisfy this requirement, making them safe for repeated execution without destabilizing version control history.

---

## 5. Why is Black still the de-facto community standard despite the availability of faster alternatives like ruff format?

Black’s dominance is rooted in ecosystem adoption rather than raw technical superiority. Over time, Black has become a social convention: contributors recognize its output, tooling assumes its presence, and repositories encode it into CI and contribution guidelines. Switching formatters in established projects introduces large diffs and increased review scrutiny, creating friction that outweighs performance benefits in many cases.

---

## 6. Can ruff format realistically replace Black, and what technical versus social constraints govern such a transition?

Technically, ruff format already satisfies the core requirements of a modern formatter, including determinism, idempotence, and high performance. However, widespread replacement of Black depends on non-technical factors: compatibility expectations, diff stability, reviewer trust, and ecosystem inertia. As a result, ruff format is more likely to see **gradual adoption**, particularly in new projects or performance-sensitive environments, rather than immediate ecosystem-wide replacement.

---

## Closing Note

The formatter benchmark shows that formatter adoption is shaped as much by **operational robustness and social convention** as by technical capability. Performance, failure behavior, and idempotence determine viability, while ecosystem trust determines longevity.

## 10. Conclusion

This benchmark demonstrates that Python formatters make **clear, intentional trade-offs**
between performance, robustness, and failure behavior.

- Speed varies by orders of magnitude based on implementation
- All evaluated formatters satisfy idempotence requirements
- Failures on CPython test fixtures reflect correct behavior, not defects

The results should be interpreted as a **comparative operational analysis**, not a stylistic ranking.
