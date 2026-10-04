"""Reference Python interview exercises. Importing this module executes every test."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class PythonProblem:
    level: str
    topic: str
    slug: str
    title: str
    prompt: str
    function_name: str
    signature: str
    solution_body: str
    tests: str
    extra_imports: str = ""


def _check(problem: PythonProblem) -> None:
    module = "\n".join(
        [
            "from __future__ import annotations",
            problem.extra_imports,
            "",
            f"def {problem.function_name}({problem.signature}):",
            f'    """{problem.title}."""',
            textwrap.indent(textwrap.dedent(problem.solution_body).strip("\n"), "    "),
            "",
            textwrap.dedent(problem.tests).replace(
                f"from solution import {problem.function_name}\n", ""
            ),
        ]
    )
    namespace: dict = {"pytest": pytest}
    exec(compile(module, problem.slug, "exec"), namespace)  # noqa: S102
    ran = False
    for name, value in namespace.items():
        if name.startswith("test_") and callable(value):
            value()
            ran = True
    if not ran:
        raise RuntimeError(f"{problem.slug} has no test")


def all_python_problems() -> list[PythonProblem]:
    from lab_specs.python_raw import RAW as raw_a
    from lab_specs.python_raw_b import RAW as raw_b
    from lab_specs.python_raw_c import RAW as raw_c

    RAW = list(raw_a) + list(raw_b) + list(raw_c)

    problems: list[PythonProblem] = []
    for row in RAW:
        extra = row[9] if len(row) > 9 else ""
        problem = PythonProblem(
            level=row[0],
            topic=row[1],
            slug=row[2],
            title=row[3],
            prompt=row[4],
            function_name=row[5],
            signature=row[6],
            solution_body=row[7],
            tests=row[8],
            extra_imports=extra,
        )
        _check(problem)
        problems.append(problem)
    slugs = [problem.slug for problem in problems]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError("Duplicate Python slug")
    if len(problems) < 150:
        raise RuntimeError(f"Need >= 150 Python problems, found {len(problems)}")
    return problems
