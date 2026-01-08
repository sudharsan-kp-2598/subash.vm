# Python Tooling Analysis

## Purpose

This project evaluates **Python linters, formatters, and type checkers** to determine
the **best overall tools** based on correctness, performance, usability, and ecosystem
adoption.

The goal is to make a **reproducible, auditable, and evidence-based decision**, not a
preference-based one.

---

## Scope

### Included

- **Linters**: ruff, pylint, flake8, bandit, pyflakes
- **Formatters**: black, ruff format, isort, yapf, autopep8
- **Type Checkers**: pyright, mypy, pytype, pyre, pyanalyze

### Excluded

- IDE-only inspections
- Experimental or unmaintained tools
- Language-server-only features

---

## Methodology

- Tool versions are **explicitly frozen**
- Configurations are **explicitly defined and committed**
- All tools are run on:
  - The **same codebase**
  - The **same hardware**
  - The **same Python version**
- Performance tests include:
  - Cold runs
  - Warm runs
- Rankings are derived from **documented experiments**, not opinions

---

## Evaluation Dimensions

Each tool is evaluated on the following dimensions:

1. **Correctness / Quality**

   - Issues detected
   - Missed issues
   - False positives
2. **Performance**

   - Runtime
   - Scalability with code size
3. **Usability**

   - Configuration complexity
   - Error clarity
   - Developer experience
4. **Ecosystem & Adoption**

   - Community usage
   - Maintenance activity
   - CI / tooling compatibility

---
