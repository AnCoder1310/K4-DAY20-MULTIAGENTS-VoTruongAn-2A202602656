---
name: python-code-maintenance
description: Use when fixing bugs, refactoring, or preparing code changes for review in a Python package.
---
# Python Code Maintenance Checklist

1. Add explicit type annotations to all parameters and return types for every public function (any function whose name does not begin with an underscore `_`) across the package.
2. Create `tests/test_regressions.py` with at least one passing test function per bug fixed (minimum 3 test functions total).
3. Run the test suite to ensure all tests in `tests/test_regressions.py` pass without errors.
4. Update `CHANGELOG.md` under the heading `## Unreleased` by recording each fix as a bullet point in the format `- fix(<function name>): <short description>` (minimum 3 bullets).