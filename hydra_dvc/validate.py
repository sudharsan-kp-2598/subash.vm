import torch

from build_component import build_loss


def validate(model, val_loader, cfg):

    loss_functionn = build_loss(cfg)

    model.eval()

    val_loss, correct = 0.0, 0

    with torch.no_grad():

        for data, label in val_loader:

            out = model(data)

            val_loss += loss_functionn(out, label).item() * data.size(0)

            correct += (out.argmax(1) == label.argmax(1)).sum().item()

    val_loss /= 10000

    val_acc = (correct / 10000) * 100

    return val_loss, val_acc
