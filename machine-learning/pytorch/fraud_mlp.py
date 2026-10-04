"""A small fraud network, used only when PyTorch imports.

Classical models are the default in this laboratory. A network is justified
when the same later-window metric beats a calibrated gradient-boosted model
by enough to pay for the extra monitoring, and when the features are already
served. A rare 0.1% label on a few numeric columns is usually not that case.
"""

from __future__ import annotations

import numpy as np


def torch_available() -> bool:
    try:
        import torch  # noqa: F401

        return True
    except ImportError:
        return False


def train_fraud_mlp(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_valid: np.ndarray,
    y_valid: np.ndarray,
    epochs: int = 20,
    seed: int = 42,
) -> dict:
    """Train a one-hidden-layer network and return validation probabilities."""
    import torch
    from torch import nn

    torch.manual_seed(seed)
    x_t = torch.tensor(np.asarray(x_train, dtype=np.float32))
    y_t = torch.tensor(np.asarray(y_train, dtype=np.float32)).view(-1, 1)
    x_v = torch.tensor(np.asarray(x_valid, dtype=np.float32))
    model = nn.Sequential(nn.Linear(x_t.shape[1], 16), nn.ReLU(), nn.Linear(16, 1))
    positive = max(float(y_t.sum()), 1.0)
    weight = torch.tensor([(len(y_t) - positive) / positive])
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-2, weight_decay=1e-3)
    best_state = None
    best_loss = float("inf")
    stall = 0
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        loss = loss_fn(model(x_t), y_t)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            valid_loss = float(loss_fn(model(x_v), torch.tensor(np.asarray(y_valid, dtype=np.float32)).view(-1, 1)))
        if valid_loss + 1e-4 < best_loss:
            best_loss = valid_loss
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
            stall = 0
        else:
            stall += 1
            if stall >= 5:
                break
    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        probability = torch.sigmoid(model(x_v)).numpy().ravel()
    return {"valid_probability": probability, "valid_loss": best_loss, "epochs_run": epochs}
