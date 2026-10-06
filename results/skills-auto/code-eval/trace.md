### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: read_file
{"limit": 1000, "file_path": "skills/python-code-maintenance/SKILL.md"}

### Tool result
@@ lines 1-10 of 10 @@
---
name: python-code-maintenance
description: Use when fixing bugs, refactoring, or preparing code changes for review in a Python package.
---
# Python Code Maintenance Checklist

1. Add explicit type annotations to all parameters and return types for every public function (any function whose name does not begin with an underscore `_`) across the package.
2. Create `tests/test_regressions.py` with at least one passing test function per bug fixed (minimum 3 test functions total).
3. Run the test suite to ensure all tests in `tests/test_regressions.py` pass without errors.
4. Update `CHANGELOG.md` under the heading `## Unreleased` by recording each fix as a bullet point in the format `- fix(<function name>): <short description>` (minimum 3 bullets).

### Tool call: glob
{"pattern": "workspace/**/*"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: glob
{"pattern": "workspace/**/*"}