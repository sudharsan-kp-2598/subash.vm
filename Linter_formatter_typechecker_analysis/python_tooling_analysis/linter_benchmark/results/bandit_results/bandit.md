# Bandit — Linter Benchmark Results

Bandit was intentionally executed on both `code_quality/` and `security/`
directories.Evaluation is performed against a fixed benchmark consisting of:

- **8 Code Quality issues**
- **7 Security issues**
- **15 Total issues**

Only **True Positives (TP)** and **False Negatives (FN)** are considered.
Multiple Bandit findings mapping to the same planted issue are collapsed
into a single TP.

---

## Code Quality Results

### Ground Truth

- Expected issues: **8**

### Bandit Findings

- Bandit reported **no findings** in `code_quality/`

### Evaluation

- **True Positives (TP):** 0
- **False Negatives (FN):** 8

Code Quality Score = 0 / 8

<pre class="overflow-visible! px-0!" data-start="936" data-end="1734"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"></div></pre>

Bandit does not perform code-quality or correctness analysis by design.

---

## Security Results

### Ground Truth

- Expected issues: **7**

### Detected Issues (True Positives)

1. **`eval` / `exec` usage**

   - `B307` — use of `eval`
2. **Insecure temporary files**

   - `B306` — use of `tempfile.mktemp()`
3. **Subprocess shell injection**

   - `B602` — `subprocess.call(..., shell=True)`
   - `B404` — import of `subprocess` (supporting signal)
4. **Unsafe deserialization**

   - `B301` — `pickle.loads()`
   - `B403` — import of `pickle`
5. **Weak cryptography**

   - `B324` — use of `hashlib.md5`

### Missed Issues (False Negatives)

6. **Hardcoded secrets**
7. **Path traversal**

### Evaluation

- **True Positives (TP):** 5
- **False Negatives (FN):** 2

Security Score = 5 / 7

## Combined Results (Code Quality + Security)

| Category           | TP          | Total        |
| ------------------ | ----------- | ------------ |
| Code Quality       | 0           | 8            |
| Security           | 5           | 7            |
| **Combined** | **5** | **15** |



Total Score = 5 / 15


## Notes

- Bandit findings were derived **only from the observed output**.
- Severity and confidence levels were recorded but **not used for scoring**.
- Multiple Bandit warnings for a single vulnerability were intentionally
  collapsed into one TP.
- No assumptions were made beyond explicit Bandit reports.
- Bandit is a **security-focused static analyzer**, not a general-purpose linter.
