# PyTorch fraud example

## 1. Business problem

Same authorization decision as `fraud/`. A network is a candidate, not the default.

## 2. Dataset

The scaled numeric fraud matrix from a time split. Labels are the synthetic `is_fraud`.

## 3. Architecture

`fraud_mlp.py`: one hidden layer, weighted binary cross-entropy, Adam, early stopping on validation loss.

## 4. Data pipeline

Use the same preprocessor as the scikit-learn pipeline. Fit it on the training window only.

## 5. Feature engineering

The fraud contract in `src/config/settings.py`. No extra columns because a network can "learn them."

## 6. Baseline

The gradient-boosted model and the rule score. The network has to beat them on later-window PR-AUC by enough to pay for the extra monitoring.

## 7. Models

A small multilayer perceptron. Training runs only when PyTorch imports. The default `requirements.txt` does not require it. See `requirements-optional.txt`.

## 8. Validation

The same calendar split. Early stopping watches validation loss. The test window is not the stopping set.

## 9. Results

`train_fraud_mlp` returns validation probabilities. Compare them with `safe_pr_auc`. There is no stored claim that the network wins.

## 10. Business interpretation

On a 0.1% label and a handful of numeric features, a tree or a logistic model is usually the honest choice. Use the network when interactions or sequences earn their keep on a later window.

## 11. Limitations

This is not a sequence model. An LSTM would need an explicit history tensor built without future steps.

## 12. Production considerations

Export the weights with the preprocessing version. A notebook that scaled the matrix and a service that does not is training-serving skew.

## 13. Future improvements

A sequence model only after the tabular network has already beaten the boosted tree.
