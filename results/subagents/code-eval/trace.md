### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: glob
{"pattern": "workspace/**"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: glob
{"pattern": "*"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xf/ws02kc_12xlb90zbn8p75swh0000gp/T/agent_sandbox__fc_t0k5
plugins: langsmith-0.14.4, anyio-4.15.1
collected 0 items / 1 error

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/private/var/folders/xf/ws02kc_12xlb90zbn8p75swh0000gp/T/agent_sandbox__fc_t0k5/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.11/3.11.16/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
~/K4-DAY20-MULTIAGENTS-VoTruongAn-2A202602656/tasks/code-eval/workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.04s ===============================

Exit code: 2
[Command failed with exit

### Tool call: execute
{"command": "python3 -m pytest workspace"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xf/ws02kc_12xlb90zbn8p75swh0000gp/T/agent_sandbox__fc_t0k5
plugins: langsmith-0.14.4, anyio-4.15.1
collected 0 items / 1 error

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/private/var/folders/xf/ws02kc_12xlb90zbn8p75swh0000gp/T/agent_sandbox__fc_t0k5/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/homebrew/Cellar/python@3.11/3.11.16/Frameworks/Python.framework/Versions/3.11/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
~/K4-DAY20-MULTIAGENTS-VoTruongAn-2A202602656/tasks/code-eval/workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.04s ===============================

Exit code: 2
[Command failed with exit

### Tool call: execute
{"command": "PYTHONPATH=workspace pytest workspace/tests"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xf/ws02kc_12xlb90zbn8p75swh0000gp/T/agent_sandbox__fc_t0k5
plugins: langsmith-0.14.4, anyio-4.15.1
collected 3 items

workspace/tests/test_bookings.py FF.                                     [100%]

=================================== FAILURES ===================================
_______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

~/K4-DAY20-MULTIAGENTS-VoTruongAn-2A202602656/tasks/code-eval/workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
workspace/bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare 

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: task
{"description": "Read and inspect all python files in workspace/bookings/ and workspace/tests/test_bookings.py.\nCheck if there are any other files or configuration files or documentation in the repository or hidden files (e.g. .flake8, pyproject.toml, .pylintrc, etc.).\nAlso find out what \"Acme's review bot against the Acme Python team conventions\" refers to: search for any conventions, style guide, docstring standards, Acme guidelines, or review bot references anywhere in the sandbox.\n\nReport all contents, docstrings, current implementations, and any conventions found.", "subagent_type": "explorer"}

### Tool result
Based on an exploratory inspection of the sandbox and repository, here is the detailed report:

---

### 1. Repository & File Structure Inspection

A full search was performed across the sandbox root and the `workspace/` hierarchy (including hidden files):

* **Configuration files**: None found (`pyproject.toml`, `setup.cfg`, `setup.py`, `tox.ini`, `.flake8`, `.pylintrc`, `.ruff.toml`, etc. do not exist in the repository or sandbox).
* **Documentation files**:
  * `workspace/README.md`
  * `workspace/CHANGELOG.md`
* **Python source package (`workspace/bookings/`)**:
  * `__init__.py`
  * `timeutil.py`
  * `schedule.py`
  * `billing.py`
  * `calendar_export.py`
* **Tests (`workspace/tests/`)**:
  * `test_bookings.py`
* **Cache directories**:
  * `.pytest_cache/`, `workspace/.pytest_cache/`
  * `workspace/bookings/__pycache__/`, `workspace/tests/__pycache__/`

---

### 2. Regarding "Acme's review bot against the Acme Python team conventions"

A search across the sandbox files, environment variables, git history, and directory tree for `"Acme"`, `"review bot"`, `"conventions"`, or `"guidelines"` yielded **no external documentation, config files, or bot scripts** within the sandbox repository.

However, an inspection of the code implementations, docstrings, and existing test failures reveals the exact domain rules and standard Python anti-patterns/conventions that an automated review bot / linter checks against:

1. **Docstring vs. Implementation Mismatches / Bugs**:
   * Functio

### Tool call: execute
{"command": "git status && git log -n 5"}

### Tool result
[stderr] fatal: not a git repository (or any of the parent directories): .git

Exit code: 128
[Command failed with exit code 128]

### Tool call: execute
{"command": "flake8 workspace"}

### Tool result
[stderr] /bin/sh: flake8: command not found

Exit code: 127
[Command failed with exit code 127]

### Tool call: execute
{"command": "ruff check workspace"}

### Tool result
[stderr] /bin/sh: ruff: command not found

Exit code: 127
[Command failed with exit code 127]

### Tool call: execute
{"command": "python3 -m pip list"}

### Tool result
Package                Version   Editable project location
---------------------- --------- -----------------------------------------------------------
annotated-types        0.8.0
anthropic              1.11.0
anyio                  4.15.1
bracex                 3.0.1
certifi                2026.7.22
cffi                   2.1.1
charset-normalizer     3.5.2
cryptography           50.0.2
deepagents             0.7.21
distro                 1.9.0
docstring_parser       0.18.0
filetype               1.2.0
google-auth            2.60.0
google-genai           2.28.0
h11                    0.16.0
httpcore               1.0.9
httpcore2              2.13.1
httpx                  0.28.1
httpx2                 2.13.1
idna                   3.20
iniconfig              2.3.0
jiter                  0.17.0
jsonpatch              1.33
jsonpointer            3.1.1
lab-deepagents         0.1.0     ~/K4-DAY20-MULTIAGENTS-VoTruongAn-2A202602656
langchain              1.4.3
langchain-anthropic    1.7.5
langchain-core         1.6.6
langchain-deepseek     1.1.1
langchain-google-genai 4.4.0
langchain-openai       1.6.7
langchain-protocol     0.0.19
langgraph              1.2.13
langgraph-checkpoint   4.2.0
langgraph-prebuilt     1.1.0
langgraph-sdk          0.4.5
langsmith              0.14.4
openai                 3.24.0
orjson                 3.12.0
ormsgpack              1.12.2
packaging              26.3
pip                    26.2.1
pluggy                 1.6.0
pyasn1                 0.6.4
py

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: task
{"description": "Implement the fixes for `workspace/bookings/timeutil.py`, `workspace/bookings/schedule.py`, and `workspace/bookings/billing.py`.\nCheck `workspace/bookings/calendar_export.py` as well to make sure everything meets its docstring and Acme / PEP 8 conventions.\n\nRequirements:\n1. `workspace/bookings/timeutil.py`:\n   `parse_duration(text)` docstring:\n   ```\n   Convert a duration string to whole minutes (int).\n\n   Supported formats:\n     \"1h30m\" -> 90\n     \"2h\"    -> 120\n     \"45m\"   -> 45\n     \"1:30\"  -> 90\n     \"45\"    -> 45    # a bare number means minutes\n   Surrounding whitespace is ignored.\n   ```\n   If the string does not match any valid format, raise ValueError(f\"bad duration: {text!r}\").\n   Be careful with regex / parsing:\n   - Strip leading/trailing whitespace.\n   - Format 1: `(\\d+)h(\\d+)m` -> hours * 60 + minutes\n   - Format 2: `(\\d+)h` -> hours * 60\n   - Format 3: `(\\d+)m` -> minutes\n   - Format 4: `(\\d+):(\\d+)` -> hours * 60 + minutes (e.g. \"1:30\" -> 90)\n   - Format 5: `(\\d+)` -> minutes (bare number)\n   Make sure invalid strings like \"\", \"abc\", \"1h30\", \"1m30h\", \"-5\", etc. raise ValueError.\n\n2. `workspace/bookings/schedule.py`:\n   `add_slot(slot, slots=None)`\n   Docstring:\n   ```\n   Return a NEW list containing the given slots plus `slot`.\n\n   Separate calls must not share state: calling add_slot(\"a\") and then\n   add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n   ```\n   Fix the mutabl

### Tool result
All fixes have been implemented and verified:

1. **`workspace/bookings/timeutil.py`**:
   - Strips leading and trailing whitespace.
   - Matches against all supported formats in order:
     - `(\d+)h(\d+)m` (e.g., `"1h30m"` -> 90)
     - `(\d+)h` (e.g., `"2h"` -> 120)
     - `(\d+)m` (e.g., `"45m"` -> 45)
     - `(\d+):(\d+)` (e.g., `"1:30"` -> 90)
     - `(\d+)` (e.g., `"45"` -> 45)
   - Raises `ValueError(f"bad duration: {text!r}")` for invalid strings.

2. **`workspace/bookings/schedule.py`**:
   - Replaced mutable default argument `slots=[]` with `slots=None`.
   - Returns a new list `[slot]` when `slots is None` or `list(slots) + [slot]` otherwise, preventing state sharing and avoiding mutation of input lists.
   - Handles empty input `total_minutes([]) == 0`.

3. **`workspace/bookings/billing.py`**:
   - Validates that `minutes >= 0` (raising `ValueError("minutes must be >= 0")` on negative values).
   - Validates that `block > 0`.
   - Uses `math.ceil(minutes / block)` to round partial blocks up to whole integers.

4. **`workspace/bookings/calendar_export.py`**:
   - Verified docstring and implementation conforming to PEP 8 standards.

5. **Testing**:
   - Ran `cd workspace && python3 -m pytest tests -q` (all tests passed).
   - Validated additional edge cases for duration formats, invalid inputs, list isolation, and billing calculation rules.

### Tool call: task
{"subagent_type": "reviewer", "description": "Perform a thorough, independent review and test of the changes made to the `bookings` package in `workspace/`.\n\nCheck:\n1. Did we modify any files in `workspace/tests/`? (Run git diff or inspect workspace/tests to ensure test files were NOT modified).\n2. Run `cd workspace && python3 -m pytest tests -v` to ensure visible tests pass.\n3. Write and run a standalone script (without modifying workspace/tests/) that comprehensively verifies every function against its docstring:\n   - `timeutil.parse_duration`:\n     - Test \"1h30m\" -> 90\n     - Test \"2h\" -> 120\n     - Test \"45m\" -> 45\n     - Test \"1:30\" -> 90\n     - Test \"45\" -> 45\n     - Whitespace handling: \"  1h30m  \", \"\\t2h\\n\"\n     - Invalid inputs: \"\", \"abc\", \"1h30\", \"-10\", \"1:30:00\", None, etc. -> raises ValueError\n   - `schedule.total_minutes`:\n     - Test with multiple formats: `[\"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\"]`\n     - Test with empty list: `[]` -> 0\n   - `schedule.add_slot`:\n     - Test separate calls do not share state:\n       `s1 = add_slot(\"a\")` -> [\"a\"]\n       `s2 = add_slot(\"b\")` -> [\"b\"]\n     - Test passing an existing list creates a NEW list and doesn't mutate original:\n       `orig = [\"x\"]`\n       `res = add_slot(\"y\", orig)` -> [\"x\", \"y\"]\n       `assert orig == [\"x\"]`\n       `assert res is not orig`\n   - `billing.billable_blocks`:\n     - 0 minutes -> 0\n     - 1 minute -> 1 (block=15)\n     

### Tool result


### Tool call: execute
{"command": "cd workspace && python3 -m pytest tests -v"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0 -- ~/K4-DAY20-MULTIAGENTS-VoTruongAn-2A202602656/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /private/var/folders/xf/ws02kc_12xlb90zbn8p75swh0000gp/T/agent_sandbox__fc_t0k5/workspace
plugins: langsmith-0.14.4, anyio-4.15.1
collecting ... collected 3 items

tests/test_bookings.py::test_total_minutes_mixed_formats PASSED          [ 33%]
tests/test_bookings.py::test_billable_blocks_rounds_up PASSED            [ 66%]
tests/test_bookings.py::test_add_slot_single_call PASSED                 [100%]

============================== 3 passed in 0.00s ===============================

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-38 of 38 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    stripped = text.strip()

    m = re.fullmatch(r"(\d+)h(\d+)m", stripped)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))

    m = re.fullmatch(r"(\d+)h", stripped)
    if m:
        return int(m.group(1)) * 60

    m = re.fullmatch(r"(\d+)m", stripped)
    if m:
        return int(m.group(1))

    m = re.fullmatch(r"(\d+):(\d+)", stripped)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))

    m = re.fullmatch(r"(\d+)", stripped)
    if m:
        return int(m.group(1))

    raise ValueError(f"bad duration: {text!r}")

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-20 of 20 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=None):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    if slots is None:
        result = [slot]
    else:
        result = list(slots) + [slot]
    return result

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-16 of 16 @@
"""Billing rules."""
import math


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError("minutes must be >= 0")
    if block <= 0:
        raise ValueError("block must be > 0")
    return math.ceil(minutes / block)

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: execute
{"command": "python3 -c '\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n# Test parse_duration\nassert parse_duration(\"1h30m\") == 90\nassert parse_duration(\"2h\") == 120\nassert parse_duration(\"45m\") == 45\nassert parse_duration(\"1:30\") == 90\nassert parse_duration(\"45\") == 45\nassert parse_duration(\"  1h30m  \") == 90\nassert parse_duration(\"  2h  \") == 120\nassert parse_duration(\"  45m  \") == 45\nassert parse_duration(\"  1:30  \") == 90\nassert parse_duration(\"  45  \") == 45\n\nfor bad in [\"\", \"   \", \"abc\", \"1h30\", \"1m30h\", \"-5\", \"1:30:00\"]:\n    try:\n        parse_duration(bad)\n        assert False, f\"Should have failed for {bad}\"\n    except ValueError:\n        pass\n\n# Test total_minutes\nassert total_minutes([]) == 0\nassert total_minutes([\"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\"]) == 90 + 120 + 45 + 90 + 45\n\n# Test add_slot\ns1 = add_slot(\"a\")\ns2 = add_slot(\"b\")\nassert s1 == [\"a\"]\nassert s2 == [\"b\"]\norig = [\"x\"]\ns3 = add_slot(\"y\", orig)\nassert orig == [\"x\"]\nassert s3 == [\"x\", \"y\"]\n\n# Test billable_blocks\nassert billable_blocks(0) == 0\nassert billable_blocks(1) == 1\nassert billable_blocks(15) == 1\nassert billable_blocks(16) == 2\nassert billable_blocks(20) == 2\nassert billable_blocks(45) == 3\nassert billable_blocks(10, block=60) == 1\nassert billab

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<string>", line 2, in <module>
[stderr] ModuleNotFoundError: No module named 'bookings'

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "PYTHONPATH=workspace python3 -c '\nfrom bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\n# Test parse_duration\nassert parse_duration(\"1h30m\") == 90\nassert parse_duration(\"2h\") == 120\nassert parse_duration(\"45m\") == 45\nassert parse_duration(\"1:30\") == 90\nassert parse_duration(\"45\") == 45\nassert parse_duration(\"  1h30m  \") == 90\nassert parse_duration(\"  2h  \") == 120\nassert parse_duration(\"  45m  \") == 45\nassert parse_duration(\"  1:30  \") == 90\nassert parse_duration(\"  45  \") == 45\n\nfor bad in [\"\", \"   \", \"abc\", \"1h30\", \"1m30h\", \"-5\", \"1:30:00\"]:\n    try:\n        parse_duration(bad)\n        assert False, f\"Should have failed for {bad}\"\n    except ValueError:\n        pass\n\n# Test total_minutes\nassert total_minutes([]) == 0\nassert total_minutes([\"1h30m\", \"2h\", \"45m\", \"1:30\", \"45\"]) == 90 + 120 + 45 + 90 + 45\n\n# Test add_slot\ns1 = add_slot(\"a\")\ns2 = add_slot(\"b\")\nassert s1 == [\"a\"]\nassert s2 == [\"b\"]\norig = [\"x\"]\ns3 = add_slot(\"y\", orig)\nassert orig == [\"x\"]\nassert s3 == [\"x\", \"y\"]\n\n# Test billable_blocks\nassert billable_blocks(0) == 0\nassert billable_blocks(1) == 1\nassert billable_blocks(15) == 1\nassert billable_blocks(16) == 2\nassert billable_blocks(20) == 2\nassert billable_blocks(45) == 3\nassert billable_blocks(10, block=60

### Tool result
All assertion checks passed successfully!

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q"}

### Tool result
...                                                                      [100%]
3 passed in 0.00s

[Command succeeded with exit code 0]

### Assistant
### Summary of Changes

The following files in `workspace/bookings/` were updated to meet their docstring specifications and Python conventions:

1. **`workspace/bookings/timeutil.py`**:
   - Updated `parse_duration(text)` to handle all formats specified in its docstring (`"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, and bare numbers like `"45"`), while ignoring leading and trailing whitespace and raising `ValueError` on malformed inputs.

2. **`workspace/bookings/billing.py`**:
   - Replaced `round()` with `math.ceil()` in `billable_blocks(minutes, block=15)` so that partial blocks are rounded up as required.
   - Added validation to ensure `minutes >= 0` (raising `ValueError` when negative) and `block > 0`.

3. **`workspace/bookings/schedule.py`**:
   - Replaced mutable default argument `slots=[]` with `slots=None` in `add_slot(slot, slots=None)`.
   - Ensured a new list is returned without mutating input arguments or sharing state across separate function calls.

The files in `tests/` were left unchanged, and the entire test suite now passes.

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q"}