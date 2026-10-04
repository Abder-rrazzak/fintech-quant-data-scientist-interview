"""Write the laboratory exercises, question bank, and project notes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from lab_specs.python_labs import all_python_problems  # noqa: E402
from lab_specs.questions import build_questions  # noqa: E402
from lab_specs.sql_bank import build_sql_problems  # noqa: E402


def main() -> None:
    python_problems = all_python_problems()
    sql_problems = build_sql_problems()
    _write_python(python_problems)
    _write_sql(sql_problems)
    questions = build_questions(sql_problems, python_problems)
    bank_path = ROOT / "mock-interviews" / "question_bank.json"
    bank_path.parent.mkdir(parents=True, exist_ok=True)
    bank_path.write_text(json.dumps(questions, indent=2), encoding="utf-8")
    _write_cases_and_designs()
    _write_notebooks()
    print(f"Python exercises: {len(python_problems)}")
    print(f"SQL exercises: {len(sql_problems)}")
    print(f"Interview questions: {len(questions)}")


def _write_python(problems) -> None:
    for problem in problems:
        folder = ROOT / "python" / problem.level / problem.slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "problem.md").write_text(
            "\n".join(
                [
                    f"# {problem.title}",
                    "",
                    f"Topic: {problem.topic}",
                    "",
                    problem.prompt,
                    "",
                    "Implement the function in `starter.py`. Do not open `solution.py` until you have a version that passes the tests.",
                    "",
                    "```bash",
                    "pytest " + str(folder / "test_solution.py").replace("\\", "/"),
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        starter = _module(problem, body="raise NotImplementedError")
        solution = _module(problem, body=problem.solution_body)
        (folder / "starter.py").write_text(starter, encoding="utf-8")
        (folder / "solution.py").write_text(solution, encoding="utf-8")
        (folder / "test_solution.py").write_text(problem.tests if problem.tests.endswith("\n") else problem.tests + "\n", encoding="utf-8")


def _module(problem, body: str) -> str:
    import textwrap

    indented = textwrap.indent(textwrap.dedent(body).strip("\n"), "    ")
    imports = problem.extra_imports.strip()
    import_block = f"{imports}\n" if imports else ""
    return (
        "from __future__ import annotations\n\n"
        f"{import_block}"
        f"def {problem.function_name}({problem.signature}):\n"
        f'    """{problem.title}."""\n'
        f"{indented}\n"
    )


def _write_sql(problems) -> None:
    for index, problem in enumerate(problems, start=1):
        if problem.level == "performance":
            folder = ROOT / "sql" / "performance"
        else:
            folder = ROOT / "sql" / problem.level
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{index:03d}_{problem.slug}.sql"
        path.write_text(
            "\n".join(
                [
                    f"-- {problem.title}",
                    f"-- Level: {problem.level}",
                    "-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.",
                    "--",
                    "-- " + problem.prompt.replace("\n", "\n-- "),
                    "--",
                    "-- Approach: " + problem.approach,
                    "-- Common mistake: " + problem.mistake,
                    "",
                    problem.solution,
                ]
            ),
            encoding="utf-8",
        )


def _write_cases_and_designs() -> None:
    from lab_specs.questions import CASE_STUDIES, COMMUNICATION, DESIGNS, BEHAVIORAL

    case_dir = ROOT / "case-studies"
    case_dir.mkdir(parents=True, exist_ok=True)
    for index, case in enumerate(CASE_STUDIES, start=1):
        (case_dir / f"case_{index:02d}.md").write_text(case, encoding="utf-8")
    comm = ROOT / "case-studies" / "business-communication"
    comm.mkdir(parents=True, exist_ok=True)
    for index, text in enumerate(COMMUNICATION, start=1):
        (comm / f"example_{index:02d}.md").write_text(text, encoding="utf-8")
    design = ROOT / "system-design"
    design.mkdir(parents=True, exist_ok=True)
    for index, text in enumerate(DESIGNS, start=1):
        (design / f"design_{index:02d}.md").write_text(text, encoding="utf-8")
    behavioral = ROOT / "behavioral"
    behavioral.mkdir(parents=True, exist_ok=True)
    (behavioral / "README.md").write_text(
        "\n".join(
            [
                "# Behavioral interview",
                "",
                "Use your own experience. The prompts below are scaffolds.",
                "Replace every bracket with something you actually did.",
                "Do not invent employment at a bank or a fraud team.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    for index, text in enumerate(BEHAVIORAL, start=1):
        (behavioral / f"prompt_{index:02d}.md").write_text(text, encoding="utf-8")


def _write_notebooks() -> None:
    import nbformat
    from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

    specs = [
        (
            "01_eda_financial_transactions.ipynb",
            "EDA on synthetic transactions",
            "Generate a small book and inspect fraud rate, missingness, and monthly volume. This is a laboratory, not a production extract.",
            "from data.generate import GenerateConfig, generate_dataset\n"
            "from data.quality import quality_report\n"
            "tables = generate_dataset(GenerateConfig(n_customers=400, n_transactions=5000, seed=42))\n"
            "report = quality_report(tables['transactions'])\n"
            "report['fraud_rate'], report['duplicate_transaction_ids']\n",
        ),
        (
            "02_credit_risk.ipynb",
            "Credit risk loop",
            "Probability of default is not an approval policy. Expected loss is PD x LGD x EAD.",
            "from risk.expected_loss import expected_loss\n"
            "expected_loss(0.02, 0.45, 10000)\n",
        ),
        (
            "03_fraud_detection.ipynb",
            "Fraud score to decision",
            "A rare label needs PR-AUC and a cost threshold, then an approve / review / block rule.",
            "import numpy as np\n"
            "from fraud.decisions import decide\n"
            "from evaluation.thresholds import select_threshold, threshold_cost_curve\n"
            "y = np.array([1, 0, 0, 1, 0])\n"
            "scores = np.array([0.9, 0.6, 0.2, 0.4, 0.05])\n"
            "curve = threshold_cost_curve(y, scores, fn_cost=500, fp_cost=5)\n"
            "best = select_threshold(curve)\n"
            "decide(scores, best['threshold'], min(0.99, best['threshold'] + 0.2))\n",
        ),
        (
            "04_customer_lifetime_value.ipynb",
            "RFM and a horizon label",
            "Features stop at the cutoff. Revenue after the cutoff is the label.",
            "import pandas as pd\n"
            "from models.clv import horizon_revenue_frame, simple_clv\n"
            "print(simple_clv(40, 6, 0.3, 2))\n"
            "tx = pd.DataFrame({'customer_id':[1,1],'transaction_id':[1,2],'timestamp':pd.to_datetime(['2024-01-01','2024-08-01']),'amount':[20.0,50.0]})\n"
            "horizon_revenue_frame(tx, pd.Timestamp('2024-06-01'))\n",
        ),
        (
            "05_time_series.ipynb",
            "Causal forecast split",
            "Train, validation, and test are ordered in time. Random row splits leak the future.",
            "import numpy as np\n"
            "import pandas as pd\n"
            "from forecasting.backtest import expanding_window_indices, assert_causal_splits\n"
            "from forecasting.series import log_returns\n"
            "splits = expanding_window_indices(24, min_train=12, test_size=3)\n"
            "assert_causal_splits(splits)\n"
            "log_returns(np.array([100.0, 110.0, 121.0]))\n",
        ),
        (
            "06_model_interpretability.ipynb",
            "What a coefficient is not",
            "A coefficient is a direction in the training feature space after scaling. It is not a business cause.",
            "import pandas as pd\n"
            "from evaluation.validation import find_leaky_columns\n"
            "find_leaky_columns(['amount', 'is_fraud', 'prior_delinquency_count'])\n",
        ),
    ]
    notebook_dir = ROOT / "notebooks"
    notebook_dir.mkdir(parents=True, exist_ok=True)
    for name, title, intro, code in specs:
        book = new_notebook()
        book.cells = [
            new_markdown_cell(f"# {title}\n\n{intro}\n\nSynthetic laboratory. Not a claim of production ownership."),
            new_code_cell("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path('..').resolve() / 'src'))\n"),
            new_code_cell(code),
        ]
        nbformat.write(book, notebook_dir / name)


if __name__ == "__main__":
    main()
