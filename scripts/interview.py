"""Run a mock interview from the question bank."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interview.engine import (  # noqa: E402
    filter_questions,
    load_questions,
    parse_scores,
    render_full_session,
    render_question,
    render_scorecard,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Financial data science mock interview.")
    parser.add_argument("--topic", type=str, default=None)
    parser.add_argument("--difficulty", type=str, default=None)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument(
        "--scores",
        type=str,
        default="",
        help="Self-scores such as python=4,sql=3,fraud=2",
    )
    args = parser.parse_args()
    questions = load_questions()
    scores = parse_scores(args.scores)
    if args.interactive:
        scores = _interactive(questions, args, scores)
    if args.full:
        print(render_full_session(questions, scores or None))
        return
    chosen = filter_questions(questions, topic=args.topic, difficulty=args.difficulty, limit=args.count)
    if not chosen:
        raise SystemExit("No questions matched the filters.")
    for question in chosen:
        print(render_question(question, reveal=not args.interactive))
        print("-" * 60)
    print(render_scorecard(scores or None))


def _interactive(questions, args, scores: dict[str, int]) -> dict[str, int]:
    if args.full:
        plan = [
            ("python", "python"),
            ("sql", "sql"),
            ("statistics", "statistics"),
            ("machine_learning", "machine_learning"),
            ("fraud", "fraud"),
            ("system_design", "system_design"),
            ("behavioral", "communication"),
        ]
        selected = []
        for topic, score_key in plan:
            pool = filter_questions(questions, topic=topic, limit=1)
            if pool:
                selected.append((pool[0], score_key))
    else:
        selected = [
            (question, args.topic or question.topic)
            for question in filter_questions(
                questions, topic=args.topic, difficulty=args.difficulty, limit=args.count
            )
        ]
    for question, key in selected:
        print(render_question(question, reveal=False))
        raw = input(f"Score your answer for {key} from 0 to 5: ").strip()
        scores[key] = int(raw)
        print(render_question(question, reveal=True))
    return scores


if __name__ == "__main__":
    main()
