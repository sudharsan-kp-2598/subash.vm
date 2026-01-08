

# YAPF Format Failure Analysis

## Summary

YAPF failed when run on the CPython Lib directory because it encountered Python 2–only syntax early during traversal. YAPF enforces Python 3 grammar strictly and uses a fail-fast execution model, meaning it stops immediately when it cannot parse a file. As a result, formatting aborted with exit status 1 and only a single error was reported, even though many additional files in the directory are incompatible with Python 3.

The failure observed is expected behavior and is not a misconfiguration or bug.

## Failed Files and Reasons

Lib/lib2to3/tests/data/different_encoding.py failed due to Python 2 syntax. The file contains a Python 2 style print statement without parentheses and uses legacy unicode literal syntax. This syntax is invalid in Python 3 and cannot be parsed into a Python 3 AST, which YAPF requires in order to operate.

This file is intentionally included in CPython as part of the lib2to3 test suite and is designed to test legacy syntax and encoding behavior, not to be formatted by modern formatters.

## Why Only One Error Is Reported

YAPF follows a fail-fast parsing strategy. Files are processed sequentially, and the first file that cannot be parsed using Python 3 grammar causes immediate termination. YAPF does not continue to subsequent files, does not aggregate multiple failures, and does not produce a summary of all incompatible files.

Because different_encoding.py appears early in the directory traversal order, YAPF exits before reaching other files that also contain Python 2 syntax or invalid encodings.

## Conclusion

YAPF’s behavior is correct and consistent with its design philosophy. The single reported error does not imply that only one file is incompatible; it indicates that YAPF never reached the remaining incompatible files. This fail-fast model makes YAPF unsuitable for large, mixed-version repositories such as CPython without preprocessing or explicit file exclusion.

When comparing formatter robustness and failure reporting, YAPF’s output is not directly comparable to tools like Black or ruff format, which traverse the entire directory and report all failures encountered.
