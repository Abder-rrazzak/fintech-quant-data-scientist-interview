"""Local feature store: offline Parquet history plus a latest-value online cache.

Point-in-time correctness matters because financial labels are defined on a
future outcome (default within 12 months, fraud confirmed later). If training
joins the customer's *current* utilization or *current* risk score, the model
sees information that did not exist at the decision, validation numbers are
fiction, and production will not match them.

Training-serving skew is the same bug in production form: the offline job and
the online cache compute a feature differently, or they read it at different times.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class ParquetFeatureStore:
    """Offline store with backward as-of joins."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, name: str, frame: pd.DataFrame, entity_keys: list[str], event_time: str) -> None:
        if event_time not in frame.columns:
            raise ValueError(f"Missing event time column {event_time}")
        for key in entity_keys:
            if key not in frame.columns:
                raise ValueError(f"Missing entity key {key}")
        ordered = frame.sort_values(entity_keys + [event_time], kind="mergesort")
        ordered.to_parquet(self.root / f"{name}.parquet", index=False)
        meta = {"entity_keys": entity_keys, "event_time": event_time}
        (self.root / f"{name}.meta.json").write_text(json.dumps(meta), encoding="utf-8")

    def get_as_of(self, name: str, entities: pd.DataFrame, as_of_col: str) -> pd.DataFrame:
        meta = json.loads((self.root / f"{name}.meta.json").read_text(encoding="utf-8"))
        features = pd.read_parquet(self.root / f"{name}.parquet")
        keys: list[str] = meta["entity_keys"]
        event_time: str = meta["event_time"]
        if len(keys) != 1:
            raise ValueError("This laboratory store demonstrates a single entity key.")
        key = keys[0]
        left = entities.sort_values(as_of_col, kind="mergesort")
        right = features.sort_values(event_time, kind="mergesort")
        merged = pd.merge_asof(
            left,
            right,
            left_on=as_of_col,
            right_on=event_time,
            by=key,
            direction="backward",
        )
        return merged


class OnlineFeatureCache:
    """Latest feature vector per entity, which is what a low-latency API often reads."""

    def __init__(self) -> None:
        self._values: dict[str, dict] = {}

    def upsert(self, entity_id: str, features: dict, event_time: pd.Timestamp) -> None:
        current = self._values.get(entity_id)
        stamp = pd.Timestamp(event_time)
        if current is None or stamp >= current["event_time"]:
            self._values[entity_id] = {"features": dict(features), "event_time": stamp}

    def get_latest(self, entity_id: str) -> dict | None:
        found = self._values.get(entity_id)
        if found is None:
            return None
        return dict(found["features"])


def training_serving_skew(offline_value: float, online_value: float, atol: float = 1e-8) -> bool:
    """True when the value used in training disagrees with the served value."""
    return abs(float(offline_value) - float(online_value)) > atol
