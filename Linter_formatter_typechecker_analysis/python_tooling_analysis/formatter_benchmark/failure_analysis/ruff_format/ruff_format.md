
# Ruff Format Failure Analysis (CPython Lib)

This document records the exact reasons `ruff format` failed when run against the full CPython 3.10.19 standard library (`Lib/` directory).

All failures are expected and stem from files that are intentionally invalid, Python-2–specific, or encoded using non-UTF-8 encodings for parser and tokenizer testing.

---

## Summary

Formatter: ruff format
Target: CPython 3.10.19 `Lib/`
Failure type: Parsing and encoding errors
Scope: Intentionally invalid or unsupported source files

---

## Failed Files and Reasons

1. **Lib/lib2to3/tests/data/bom.py**Failure reason: Python 2 syntaxThe file contains a Python 2 style `print` statement which is invalid under Python 3 grammar.
2. **Lib/lib2to3/tests/data/crlf.py**Failure reason: Python 2 syntaxUses a Python 2 `print` statement without parentheses.
3. **Lib/lib2to3/tests/data/different_encoding.py**Failure reason: Python 2 unicode literal and invalid encoding combinationThe file contains Python 2–specific unicode syntax not valid in Python 3.
4. **Lib/lib2to3/tests/data/false_encoding.py**Failure reason: Invalid encoding declarationThe file declares a fake encoding intended to break tokenization.
5. **Lib/lib2to3/tests/data/py2_test_grammar.py**Failure reason: Python 2–only grammarContains invalid Python 3 literals such as long integers.
6. **Lib/test/badsyntax_3131.py**Failure reason: Invalid tokenThe file contains an unexpected Unicode token (`€`) used to test parser error handling.
7. **Lib/test/badsyntax_pep3120.py**Failure reason: Invalid UTF-8 encodingThe file violates PEP 3120 encoding requirements.
8. **Lib/test/encoded_modules/module_iso_8859_1.py**Failure reason: Non-UTF-8 encoded sourceThe file is encoded using ISO-8859-1 and cannot be read as UTF-8.
9. **Lib/test/encoded_modules/module_koi8_r.py**Failure reason: Non-UTF-8 encoded sourceThe file is encoded using KOI8-R and is intentionally not UTF-8.
10. **Lib/test/test_source_encoding.py**
    Failure reason: Invalid source encoding
    The file intentionally violates source encoding rules.

---

## Conclusion

All reported failures correspond to files that are intentionally invalid, Python-2–specific, or encoded using non-UTF-8 encodings.

`ruff format` correctly refuses to parse or format these files.
These failures must be treated as expected exclusions in formatter benchmarking and do not indicate a defect in `ruff format`.
