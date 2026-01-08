

# Overall Linter Analysis


## 0. What Are Linters and How They Differ from Type Checkers

### What Are Linters

- Linters are **static analysis tools** that examine source code **without executing it**
- They focus on:
  - Common programming mistakes
  - Code quality issues
  - Potential bugs
  - Maintainability problems
- Linters work primarily on:
  - Syntax
  - Abstract Syntax Tree (AST)
  - Simple semantic rules
- Linters are typically:
  - Fast (depending on depth)
  - Rule-based
  - Language-specific

---

### What Linters Are Used For

- Catch obvious bugs early:
  - Unused imports
  - Undefined variables
  - Bad comparisons
  - Dangerous patterns (e.g., mutable defaults)
- Improve code quality and maintainability
- Enforce consistency across a codebase
- Act as an **early warning system** before runtime errors
- Provide feedback during:
  - Development
  - Code review
  - Continuous Integration (CI)

---

### How Linters Differ from Type Checkers

- **Linters**

  - Analyze code structure and patterns
  - Focus on *how code is written*
  - Do not require type annotations
  - Can work on untyped or partially typed code
  - Detect stylistic, semantic, and structural issues
- **Type Checkers**

  - Analyze type correctness of code
  - Focus on *what values flow through the program*
  - Rely on type hints and type inference
  - Detect type mismatches and invalid operations
  - Enforce type safety, not code style or structure

---

### Key Differences at a Glance

| Aspect               | Linters                             | Type Checkers              |
| -------------------- | ----------------------------------- | -------------------------- |
| Primary focus        | Code quality & correctness patterns | Type correctness           |
| Requires type hints  | No                                  | Yes (or partial inference) |
| Detects style issues | Yes                                 | No                         |
| Detects type errors  | Limited or none                     | Yes                        |
| Typical use          | Bug prevention, maintainability     | Type safety, correctness   |

---

### Why Both Are Needed

- Linters and type checkers solve **different problems**
- Linters catch:
  - Mistakes that are syntactically valid but logically wrong
- Type checkers catch:
  - Errors caused by incorrect assumptions about data types
- Using both provides:
  - Broader static analysis coverage
  - Earlier detection of bugs
  - Higher code reliability

## 1. Introduction & Scope

This document presents the final analysis of Python linters evaluated under a
controlled benchmark. The goal is to understand **performance, detection
coverage, and design trade-offs**, not to crown a single “best” tool.

The benchmark focuses on:

- Realistic correctness issues
- Security vulnerabilities
- Execution performance on a large codebase

---

## 2. Benchmark Methodology

- **Ground truth issues:** 15 total
  - 8 Code Quality
  - 7 Security
- **Metrics used:**
  - True Positives (TP)
  - False Negatives (FN)
- **Explicit exclusions:**
  - Style / formatting warnings
  - False positives
  - Tool-specific scoring systems
- **Speed testing:**
  - Cold run + multiple warm runs
  - Average warm run used for comparison
- **Codebase:** CPython source tree

The benchmark prioritizes **semantic relevance and reproducibility**.



> **Note on False Positives:**
> False Positives were intentionally excluded from this benchmark to isolate
> *detection capability* rather than tool ergonomics or configuration quality.
> False Positive rates are highly sensitive to rule selection, project conventions,
> and subjective judgment, making them difficult to compare objectively across
> tools with different design philosophies. Including False Positives would
> conflate detection coverage with usability concerns and reduce reproducibility.
> False Positive analysis is better suited to a separate, ergonomics-focused study.
>


### 2.1 Issue Coverage

The benchmark evaluates linters against a fixed set of **15 planted issues**,
explicitly divided into code quality and security categories.

#### Code Quality (8)

- Unused imports
- Import cycles
- Undefined variables
- Variable shadowing
- Mutable default arguments
- Bad comparisons
- Dead code
- High cyclomatic complexity

#### Security (7)

- `eval` / `exec` usage
- Subprocess shell injection
- Unsafe deserialization
- Weak cryptography
- Hardcoded secrets
- Insecure temporary files
- Path traversal


> Import cycle detection inherently requires cross-file dependency graph
> construction and module resolution, which most performance-focused linters
> deliberately avoid.




#### Scope Limitations

This benchmark intentionally does **not** evaluate:

- Formatting behavior (e.g., Black, Ruff formatter)
- Type inference accuracy or type checking
- False-positive suppression ergonomics
- IDE integration or editor feedback quality
- Autofix capabilities or developer experience features

---

## 3. Tools Evaluated

- Ruff
- Pylint
- Flake8
- Pyflakes
- Bandit

Each tool was evaluated strictly within its documented scope.


### 3.1 Tool Versions Evaluated

The following tool versions were used during benchmarking. Results reflect the
behavior and performance characteristics of these specific releases and the
execution environment in which they were evaluated.

| Tool     | Version | Notes                                                      |
| -------- | ------- | ---------------------------------------------------------- |
| Ruff     | 0.14.10 | Rust-based, performance-focused linter                     |
| Pylint   | 4.0.4   | Deep semantic and structural analysis (uses astroid 4.0.3) |
| Flake8   | 7.3.0   | Orchestration layer over Pyflakes and Pycodestyle          |
| Pyflakes | 3.4.0   | Name-based correctness checker                             |
| Bandit   | 1.9.2   | Security-focused static analyzer                           |

**Execution environment:**

- Python 3.12.12 (Anaconda)
- Linux

---

## 4. Performance (Speed) Analysis

| Tool     | Avg Warm Runtime    |
| -------- | ------------------- |
| Ruff     | **0.372s**    |
| Flake8   | 9.825s              |
| Pyflakes | 13.919s             |
| Bandit   | 34.265s             |
| Pylint   | **2108.385s** |

### Observations

- Ruff operates at **sub-second latency**, suitable for real-time workflows.
- Flake8 and Pyflakes fall into the “seconds” category.
- Bandit is slower due to security rule evaluation.
- Pylint is **orders of magnitude slower**, making it unsuitable for frequent runs
  on large repositories.

---

## 5. Detection Coverage Analysis

### 5.1 Code Quality (8 issues)

| Tool     | TP          |
| -------- | ----------- |
| Ruff     | 3           |
| Flake8   | 3           |
| Pyflakes | 3           |
| Bandit   | 0           |
| Pylint   | **7** |

**Common detections (Ruff / Flake8 / Pyflakes):**

- Unused imports
- Undefined variables
- Bad comparisons (`is` vs `==`)

**Advanced detections (Pylint only):**

- Variable shadowing
- Mutable default arguments
- Dead code
- High cyclomatic complexity

---

### 5.2 Security (7 issues)

| Tool     | TP          |
| -------- | ----------- |
| Bandit   | **5** |
| Pylint   | 1           |
| Ruff     | 0           |
| Flake8   | 0           |
| Pyflakes | 0           |

Bandit detects classic Python security antipatterns.
Other linters do not attempt security analysis by design.



> **Note on Interpretation:**
> This benchmark measures the *presence* of detections (True Positives), not the
> quality, explanation depth, or fix guidance of individual diagnostics. A higher
> TP count does not imply better diagnostic quality, nor does a lower count imply
> a weaker tool.
>

---

## 6. Combined Detection Summary

| Tool     | TP / 15          |
| -------- | ---------------- |
| Ruff     | 3 / 15           |
| Flake8   | 3 / 15           |
| Pyflakes | 3 / 15           |
| Bandit   | 5 / 15           |
| Pylint   | **8 / 15** |

No tool achieves comprehensive coverage alone.

---

## 7. Discussion

### 7.1 Why Ruff Exists When Pylint Already Exists

Pylint cannot be made fast without abandoning deep semantic analysis.
Ruff exists to provide **deterministic, ultra-fast, low-noise checks**
suitable for modern development workflows.

---

### 7.2 Why Ruff Is Intentionally Limited

Ruff explicitly avoids:

- Cross-file analysis
- Deep control-flow reasoning
- Subjective code quality metrics
- Security analysis

These are not missing features.
They are **explicit non-goals** to preserve speed, determinism, and low noise.

---

### 7.3 What “Noise” Means in Linters

Noise refers to findings that:

- Do not lead to immediate corrective action
- Require suppression or configuration
- Increase cognitive load without proportional value

Pylint accepts higher noise to detect deep issues.
Ruff minimizes noise by enforcing only objective, local checks.

---

### 7.4 Ruff vs Flake8 vs Pyflakes

- **Pyflakes** defines the minimal correctness core (name-based errors).
- **Flake8** aggregates multiple lightweight tools under one interface.
- **Ruff** reimplements this rule space with a performance-first architecture.

Their detection overlap is expected; their operational goals differ.

---

### 7.5 Why Pylint Still Exists

Pylint detects deep semantic and structural issues that cannot be found
without expensive global analysis. These issues impact long-term correctness
and maintainability and justify Pylint’s performance cost.

---

### 7.6 Why No Single Linter Is Sufficient

- Fast linters catch frequent, local mistakes.
- Deep linters catch rare but costly semantic bugs.
- Security analyzers require specialized rule sets.

Each tool addresses a **different risk layer**.

---



### 7.7 Why Flake8 Is Not Widely Appreciated Today

- Multi-second execution time feels slow in modern workflows (on-save, pre-commit, CI)
- Does not provide unique analysis beyond what specialized tools already cover
- Significant overlap with:
  - Ruff (fast correctness checks)
  - Black (formatting)
  - Type checkers (mypy, pyright)
- Perceived as stable but outdated rather than essential for new projects
- Lacks a clear, distinct role in the modern Python tooling ecosystem

---

### 7.8 Flake8 Inbuilt Components and Working Structure

- Flake8 acts as an **orchestration layer**, not a deep analyzer
- Runs the following tools internally by default:
  - **Pyflakes**
    - Unused imports
    - Undefined variables
    - Bad comparisons
  - **Pycodestyle**
    - Blank lines
    - Line length
    - Indentation
- Flake8 itself:
  - Collects results from these tools
  - Assigns standardized error codes (e.g., `F401`, `E302`)
  - Produces a unified report
- Does not perform semantic analysis, security analysis, or cross-file reasoning on its own

---

### 7.9 How Ruff Replaced Flake8 and the Plugin Overhead Problem

- Ruff reimplements the most valuable Flake8 checks directly in a single binary
- Removes the need for:
  - External plugins
  - Plugin configuration and maintenance
  - Version compatibility management
- Flake8 plugin-based model introduces:
  - Increased runtime as plugins grow
  - Inconsistent rule quality
  - Higher configuration and cognitive overhead
- Ruff avoids plugin sprawl by:
  - Enforcing strict rule inclusion criteria
  - Prioritizing speed, determinism, and low-noise checks
- Result: simpler setup, faster execution, and predictable behavior

---


### 7.10 Ruff’s Relative Maturity and Ongoing Evolution

Ruff is a comparatively newer tool in the Python ecosystem, with initial
development beginning around 2022, whereas tools like Pylint, Flake8, and
Pyflakes have existed for over a decade. Despite its relative youth, Ruff has
seen rapid adoption and demonstrates architectural stability in its core design.
Its ongoing evolution primarily involves the addition of new low-noise,
file-local rules, performance optimizations, and improved autofix support,
rather than expansion into deep semantic or cross-file analysis. As a result,
while Ruff’s rule coverage may continue to grow, its fundamental scope and
design trade-offs are not expected to change significantly.

---





## 8. Threats to Validity

- **Performance measurements** were conducted on the `CPython/Lib` standard library directory; execution times may differ for smaller projects, application codebases, or non–stdlib layouts.
- **Detection coverage benchmarks** were evaluated on a custom, controlled benchmark designed to exercise specific code quality and security issues; results reflect coverage within this defined scope.
- Only **True Positives (TP)** and **False Negatives (FN)** were considered; False Positives were intentionally excluded to focus on detection capability rather than noise.
- Tools were evaluated within their default or documented scopes; alternative configurations or additional plugins may yield different results.
- Security findings reflect the selected vulnerability patterns and do not represent exhaustive security analysis.

## 9. Final Conclusions (Linters)

- Ruff provides unmatched speed and low-noise correctness checks.
- Pylint offers the deepest code-quality analysis at high computational cost.
- Bandit is the only effective security-focused tool in this benchmark.
- Flake8 and Pyflakes remain relevant for conservative, lightweight checks.

**Conclusion:**
A modern Python toolchain should treat linters as **complementary**, not
competitive. The benchmark demonstrates that coverage, speed, and depth
cannot be maximized simultaneously within a single linter.
