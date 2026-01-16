from build_component import build_loss
from validate import validate
import json

def train(model, train_loader, val_loader, optimizer, cfg):
    epochs = cfg["epochs"]
    loss_functionn = build_loss(cfg)
    
    # --- FIX 1: Initialize the variable ---
    best_val_acc = 0.0 

    for epoch in range(epochs):
        model.train()
        train_loss, train_correct = 0.0, 0

        for data, label in train_loader:
            output = model(data)
            loss = loss_functionn(output, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * data.size(0)
            # Assuming labels are one-hot encoded based on your .argmax(1) usage
            train_correct += (output.argmax(1) == label.argmax(1)).sum().item()

        train_loss /= 50000
        train_acc = (train_correct / 50000) * 100

        # Validation step
        val_loss, val_acc = validate(model, val_loader, cfg)

        # --- FIX 2: Track the best accuracy ---
        if val_acc > best_val_acc:
            best_val_acc = val_acc

        print(
            f"Epoch {epoch+1}: "
            f"train_loss={train_loss:.6f}, train_acc={train_acc:.2f}%, "
            f"val_loss={val_loss:.6f}, val_acc={val_acc:.2f}%"
        )


    metrics = {
        "best_val_acc": best_val_acc,
        "epochs": cfg.epochs,
        "lr": cfg.lr,
        "hidden_dim": cfg.model.hidden_dim,
    }

    with open("metrics.json", "w") as f:
        json.dump(metrics, f)
        
    # Now best_val_acc is defined and holds the best score for Optuna
    return best_val_acc

    