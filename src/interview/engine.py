"""Mock interview loader, printer, and scorecard."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config.settings import SETTINGS

SCORECARD_ROWS = [
    ("Python", "python"),
    ("SQL", "sql"),
    ("Statistics", "statistics"),
    ("Machine Learning", "machine_learning"),
    ("Fraud", "fraud"),
    ("Credit Risk", "credit_risk"),
    ("Time Series", "time_series"),
    ("Spark", "spark"),
    ("AWS/Snowflake", "aws_snowflake"),
    ("System Design", "system_design"),
    ("Business", "business"),
    ("Communication", "communication"),
]

FULL_SECTIONS = [
    ("python", "Python", 10),
    ("sql", "SQL", 15),
    ("statistics", "Statistics", 10),
    ("machine_learning", "Machine Learning", 15),
    ("fraud", "FinTech / Risk", 15),
    ("system_design", "System Design", 15),
    ("behavioral", "Behavioral", 10),
]


@dataclass(frozen=True)
class Question:
    id: str
    topic: str
    difficulty: str
    section: str
    prompt: str
    answer_30s: str
    answer_2min: str
    deep_dive: str
    follow_ups: tuple[str, ...]
    common_mistake: str


def load_questions(path: Path | None = None) -> list[Question]:
    bank = path or SETTINGS.question_bank
    if not bank.exists():
        raise FileNotFoundError(
            f"Question bank not found at {bank}. Generate the laboratory content first."
        )
    raw = json.loads(bank.read_text(encoding="utf-8"))
    questions = []
    for item in raw:
        questions.append(
            Question(
                id=item["id"],
                topic=item["topic"],
                difficulty=item["difficulty"],
                section=item.get("section", item["topic"]),
                prompt=item["prompt"],
                answer_30s=item["answer_30s"],
                answer_2min=item["answer_2min"],
                deep_dive=item["deep_dive"],
                follow_ups=tuple(item.get("follow_ups", [])),
                common_mistake=item["common_mistake"],
            )
        )
    return questions


def filter_questions(
    questions: list[Question],
    topic: str | None = None,
    difficulty: str | None = None,
    limit: int | None = None,
) -> list[Question]:
    chosen = questions
    if topic:
        chosen = [q for q in chosen if q.topic == topic or q.section.lower() == topic.lower()]
    if difficulty:
        chosen = [q for q in chosen if q.difficulty == difficulty]
    if limit is not None:
        chosen = chosen[:limit]
    return chosen


def render_question(question: Question, reveal: bool = True) -> str:
    lines = [
        f"[{question.topic} | {question.difficulty}] {question.prompt}",
        "",
    ]
    if reveal:
        lines.extend(
            [
                "30-second answer:",
                question.answer_30s,
                "",
                "2-minute answer:",
                question.answer_2min,
                "",
                "Deep dive:",
                question.deep_dive,
                "",
                "Follow-up questions:",
                *[f"- {item}" for item in question.follow_ups],
                "",
                "Common mistake:",
                question.common_mistake,
                "",
            ]
        )
    return "\n".join(lines)


def render_scorecard(scores: dict[str, int] | None = None) -> str:
    lines = ["INTERVIEW SCORECARD", ""]
    recorded: list[int] = []
    for label, key in SCORECARD_ROWS:
        if scores and key in scores:
            value = int(scores[key])
            recorded.append(value)
            shown = f"{value}/5"
        else:
            shown = "-/5"
        lines.append(f"{label + ':':<22}{shown}")
    lines.append("")
    if not recorded:
        lines.extend(
            [
                "Strengths: not scored. Re-run with --interactive or --scores to record a self-assessment.",
                "Weaknesses: not scored.",
                "Recommended revision topics: work the section you could not answer in two minutes without notes.",
                "Next interview level: complete a scored 90-minute run before deciding.",
            ]
        )
        return "\n".join(lines)
    mean = sum(recorded) / len(recorded)
    strengths = [label for label, key in SCORECARD_ROWS if scores and scores.get(key, 0) >= 4]
    weaknesses = [label for label, key in SCORECARD_ROWS if scores and key in scores and scores[key] <= 2]
    lines.append("Strengths: " + (", ".join(strengths) if strengths else "none at 4 or above yet."))
    lines.append("Weaknesses: " + (", ".join(weaknesses) if weaknesses else "none at 2 or below."))
    lines.append(
        "Recommended revision topics: "
        + (", ".join(weaknesses) if weaknesses else "timed mixed practice and business write-ups.")
    )
    if mean >= 4:
        level = "Practice senior-loop system design and stakeholder conflict."
    elif mean >= 3:
        level = "Mid-level loop, with another pass on the weak rows before the onsite."
    else:
        level = "Another full preparation cycle before a live loop."
    lines.append(f"Next interview level: {level}")
    return "\n".join(lines)


def render_full_session(questions: list[Question], scores: dict[str, int] | None = None) -> str:
    lines = [
        "FULL MOCK INTERVIEW",
        "Synthetic laboratory. Score yourself. The printed answers are a reference, not a claim that you said them.",
        "",
        "Agenda",
    ]
    for _topic, label, minutes in FULL_SECTIONS:
        lines.append(f"- {label}: {minutes} min")
    lines.append("")
    for topic, label, minutes in FULL_SECTIONS:
        pool = filter_questions(questions, topic=topic, limit=1)
        lines.append(f"## {label} ({minutes} min)")
        if not pool:
            lines.append("No question loaded for this section.")
            lines.append("")
            continue
        lines.append(render_question(pool[0], reveal=True))
    lines.append(render_scorecard(scores))
    return "\n".join(lines)


def parse_scores(text: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    if not text.strip():
        return scores
    for part in text.split(","):
        key, raw = part.split("=")
        value = int(raw)
        if value < 0 or value > 5:
            raise ValueError(f"Score for {key} must be between 0 and 5.")
        scores[key.strip()] = value
    return scores
