import torch.nn as nn


def build_loss(cfg):

    cfg = cfg["loss"]

    name = cfg["name"]
    params = cfg.get("params", {})

    if not hasattr(nn, name):
        raise ValueError(f"Unknown loss: {name}")

    loss_cls = getattr(nn, name)
    return loss_cls(**params)
