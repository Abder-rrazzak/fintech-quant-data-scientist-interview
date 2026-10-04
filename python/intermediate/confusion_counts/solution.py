from __future__ import annotations

def confusion_counts(y_true: list[int], y_pred: list[int]):
    """Confusion counts."""
    if len(y_true) != len(y_pred):
        raise ValueError('length')
    tp = fp = tn = fn = 0
    for truth, pred in zip(y_true, y_pred):
        if pred == 1 and truth == 1:
            tp += 1
        elif pred == 1 and truth == 0:
            fp += 1
        elif pred == 0 and truth == 0:
            tn += 1
        else:
            fn += 1
    return {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}
