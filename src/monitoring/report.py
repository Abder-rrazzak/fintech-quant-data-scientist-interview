"""Write a short monitoring note from stored metrics and PSI."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from monitoring.drift import alert


def render_monitoring_report(
    path: Path,
    fraud_metrics: dict,
    credit_metrics: dict,
    feature_psi: pd.DataFrame,
) -> str:
    lines = [
        "# Monitoring report",
        "",
        "Synthetic laboratory snapshot. Thresholds below are operating conventions for this lab.",
        "",
        "## Fraud model",
        f"- Split method: {fraud_metrics.get('split_method')}",
        f"- Validation PR-AUC: {fraud_metrics.get('valid', {}).get('pr_auc')}",
        f"- Test PR-AUC: {fraud_metrics.get('test', {}).get('pr_auc')}",
        f"- Selected review threshold: {fraud_metrics.get('review_threshold')}",
        "",
        "## Credit model",
        f"- Split method: {credit_metrics.get('split_method')}",
        f"- Validation ROC-AUC: {credit_metrics.get('valid', {}).get('roc_auc')}",
        f"- Test ROC-AUC: {credit_metrics.get('test', {}).get('roc_auc')}",
        f"- Test KS: {credit_metrics.get('test', {}).get('ks')}",
        "",
        "## Feature PSI (reference = train, current = test)",
        "",
        "| Feature | PSI | Alert |",
        "| --- | --- | --- |",
    ]
    for row in feature_psi.itertuples(index=False):
        lines.append(f"| {row.feature} | {row.psi:.4f} | {alert(float(row.psi))} |")
    lines.extend(
        [
            "",
            "## When to retrain",
            "",
            "Retrain when a large PSI alert coincides with a drop in the business metric",
            "(cost, recall at the agreed precision, or KS on a seasoned outcome window),",
            "or on a fixed schedule if the book mix changes faster than that signal.",
            "Do not retrain only because a dashboard turned red once.",
            "",
        ]
    )
    text = "\n".join(lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text
