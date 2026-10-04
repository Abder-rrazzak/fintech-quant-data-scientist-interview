"""Make ``from solution import ...`` resolve to the exercise next to the test.

Each exercise directory has its own ``solution.py``. The module cache is cleared
before each file is collected so later exercises do not reuse an earlier solution.
"""

from __future__ import annotations

import sys
from pathlib import Path


def pytest_collect_file(file_path: Path, parent):  # noqa: ARG001
    if file_path.name != "test_solution.py":
        return None
    sys.modules.pop("solution", None)
    folder = str(file_path.parent)
    if folder in sys.path:
        sys.path.remove(folder)
    sys.path.insert(0, folder)
    return None
