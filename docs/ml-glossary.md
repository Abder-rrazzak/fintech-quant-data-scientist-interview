# ML glossary

| Term | Meaning here |
| --- | --- |
| Baseline | The simple score you have to beat. A rule for fraud, a credit-score rank for default. |
| PR-AUC | Area under precision-recall. The useful ranking summary when positives are rare. |
| ROC-AUC | Ranking summary that can look strong while precision at the operating point is poor. |
| Calibration | Predicted probabilities match observed frequencies in bins. Platt scaling in this lab is fit on training scores. |
| Leakage | A feature or a split that uses information from after the decision, or the label itself. |
| Censoring | The outcome window has not finished. Those rows are not negatives yet. |
| Class weight | A training adjustment so the rare class influences the fit. It does not replace a cost threshold. |
| Threshold | The score cutoff that maps to an action. Chosen on validation cost, then frozen for test. |
| Drift | Inputs, scores, or the relationship between inputs and labels moved. PSI watches the first two. Performance needs matured labels. |
| Training-serving skew | The feature in training is not the feature in the service. |
| Group split | All rows of one customer stay in one fold. |
| Walk-forward | Each forecast origin uses only data before that origin. |
