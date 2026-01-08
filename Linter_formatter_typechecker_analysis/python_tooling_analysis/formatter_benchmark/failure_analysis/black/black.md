

# Black Formatter Failure Analysis (CPython Lib)

This document records the exact reasons Black failed when run against the full CPython 3.10.19 standard library (`Lib/` directory).

All failures are expected and correct behavior. The affected files are intentionally invalid or Python-2-specific test fixtures included in CPython to validate parser, tokenizer, and encoding error handling.

Black supports only valid Python 3 grammar and encoding rules.

---

## Summary

Formatter: Black
Target: CPython 3.10.19 `Lib/`
Total files scanned: ~1730
Files failed to format: 8

Failure category: Unsupported or intentionally invalid source files

---

## Failed Files and Reasons

1. **Lib/lib2to3/tests/data/bom.py**Failure reason: Python 2 syntaxThe file contains a Python 2 print statement (`print "BOM BOOM!"`) which is not valid Python 3 syntax.
2. **Lib/lib2to3/tests/data/crlf.py**Failure reason: Python 2 syntaxThe file uses a Python 2 style print statement (`print "hi"`).
3. **Lib/lib2to3/tests/data/different_encoding.py**Failure reason: Invalid encoding combined with Python 2 unicode literalThe file uses a Python 2 unicode literal (`u'...'`) together with encoding constructs that violate Python 3 parsing rules.
4. **Lib/lib2to3/tests/data/false_encoding.py**Failure reason: Invalid encoding declarationThe file declares a fake encoding (`#coding=0`) which is intentionally invalid.
5. **Lib/lib2to3/tests/data/py2_test_grammar.py**Failure reason: Python 2-only grammarThe file contains Python 2 grammar such as long integer literals (`0L`).
6. **Lib/test/bad_coding.py**Failure reason: Invalid encoding nameThe file declares an unknown encoding (`# coding: uft-8`), which is intentionally incorrect.
7. **Lib/test/bad_coding2.py**Failure reason: Deliberately corrupted encodingThe file is designed to trigger tokenizer encoding errors.
8. **Lib/test/badsyntax_pep3120.py**
   Failure reason: Invalid or missing encoding declaration
   The file intentionally violates PEP 3120 encoding requirements.

---

## Conclusion

All eight failures are intentional CPython test fixtures and are not valid Python 3 source files.

Black correctly refuses to format these files.
Black successfully formats all valid Python 3 files in the CPython standard library.

These failures must be treated as expected exclusions in formatter benchmarking and do not indicate a robustness or correctness issue in Black.
