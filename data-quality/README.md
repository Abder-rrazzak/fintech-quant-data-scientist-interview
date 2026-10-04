# Data quality

## 1. Business problem

Know which rows are safe to train on, and keep the defects visible so you do not "fix" them by accident in the generator and forget they exist.

## 2. Dataset

Raw synthetic transactions. Defects are intentional: missing merchant category, missing device, impossible ages, negative purchases, duplicate transaction ids.

## 3. Architecture

`src/data/quality.py` is the contract. `data-quality/run_checks.py` writes a JSON report. Pandera is optional and is constructed in `pandera_transaction_schema` when the import works. The manual checks remain the contract if Pandera is absent.

## 4. Data pipeline

Training calls `clean_transactions`. The quality report should be run on the raw file, not only on the cleaned one. A clean report on an already cleaned file proves nothing.

## 5. Feature engineering

Schema first: the transaction columns listed in `TRANSACTION_COLUMNS`. Then ranges, categories, duplicates, and distribution shifts (PSI in monitoring).

## 6. Baseline

A raw extract must show a non-zero duplicate count at the generator's injection rate. If it does not, the generator changed.

## 7. Models

None. Bad rows should not become a feature of last resort.

## 8. Validation

`validate_transactions` returns human-readable issues. Strict mode is the training-table contract.

## 9. Results

`quality_report` returns row count, duplicate ids, missingness by column, negative purchases, invalid ages, null timestamps, and the fraud rate.

## 10. Business interpretation

A fraud-rate jump that is really a broken currency code is an incident, not a model failure. Check the report before you retrain.

## 11. Limitations

The checks are row-local plus a few aggregates. They do not prove the point-in-time windows are correct. That is a separate test.

## 12. Production considerations

Fail the batch on schema and on duplicate primary keys. Alert on a missingness rate that moves, not only on a null that is always there.

## 13. Future improvements

A Great Expectations-style suite with the same rules, once the manual contract is the one you mean. The concepts match; the dependency does not have to.
