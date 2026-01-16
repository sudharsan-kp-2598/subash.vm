import os
import random
import numpy as np
import torch
import hydra
#from omegaconf import DictConfig
from hydra.utils import instantiate

from data_builder import data_builder
from train import train

@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg):
    
    print(f"Running in mode: {cfg.get('experiment', 'base')}")
    print("CWD:", os.getcwd())
    print(type(cfg))

    random.seed(cfg.seed)
    np.random.seed(cfg.seed)
    torch.manual_seed(int(cfg.seed))
    os.environ["PYTHONHASHSEED"] = str(cfg.seed)

    train_loader, val_loader = data_builder(cfg)
    model = instantiate(cfg.model)
    optimizer = instantiate(cfg.optimizer, params=model.parameters())

    score = train(model, train_loader, val_loader, optimizer, cfg)

    torch.save(model.state_dict(), "model.pt")

    return score

if __name__ == "__main__":
    main()