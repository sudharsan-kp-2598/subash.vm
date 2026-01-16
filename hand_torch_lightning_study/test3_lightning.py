import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split, TensorDataset
import torch.nn.functional as F
import pytorch_lightning as pl
from torchmetrics.classification import MulticlassAccuracy
import random
import numpy as np
import os

seed = 42  
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)

import os
import urllib.request

mnist_url = "https://github.com/mnielsen/neural-networks-and-deep-learning/raw/master/data/mnist.pkl.gz"
mnist_filename = "mnist.pkl.gz"

if not os.path.exists(mnist_filename):
    print("Downloading MNIST data...")
    urllib.request.urlretrieve(mnist_url, mnist_filename)
    print("Download complete.")
else:
    print("MNIST data already exists.")

import gzip
import pickle
import numpy as np

np.random.seed(42)

def load_data():

    with gzip.open("mnist.pkl.gz", "rb") as f:
        training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    return (training_data, validation_data, test_data)

def one_hot(j):

    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

def data_builder():


    tr_d, va_d, te_d = load_data()

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [one_hot(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))

    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_results = [one_hot(y) for y in va_d[1]]
    validation_data = list(zip(validation_inputs, va_d[1]))

    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_results = [one_hot(y) for y in te_d[1]]
    test_data = list(zip(test_inputs, te_d[1]))

    return (training_inputs,training_results,validation_inputs,validation_results,test_inputs,test_results)

training_inputs,training_results,validation_inputs,validation_results,test_inputs,test_results = data_builder()

epochs, lr, batch_size = 60, 2, 16

train_inputs = torch.tensor(np.array(training_inputs), dtype=torch.float32).squeeze(-1)
train_labels = torch.tensor(np.array(training_results), dtype=torch.float32).squeeze(-1)

val_inputs = torch.tensor(np.array(validation_inputs), dtype=torch.float32).squeeze(-1)
val_labels = torch.tensor(np.array(validation_results), dtype=torch.float32).squeeze(-1)

train_set = TensorDataset(train_inputs, train_labels)
val_set = TensorDataset(val_inputs, val_labels)

g = torch.Generator().manual_seed(seed)
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True , generator=g)
val_loader   = DataLoader(val_set, batch_size=batch_size, shuffle=False)

class MNISTLit(pl.LightningModule):
    def __init__(self, lr=lr):

        super().__init__()
        self.save_hyperparameters()
        self.net = nn.Sequential(
                   nn.Linear(784, 50),
                   nn.Sigmoid(),
                   nn.Linear(50, 10),
                   nn.Sigmoid(),
                )
        
        self.loss_fn = nn.MSELoss()
        self.acc = MulticlassAccuracy(num_classes=10)
        self.valacc = MulticlassAccuracy(num_classes=10)


    def forward(self, x):
      return self.net(x)

    def train_step(self, batch, stage):

        data, label = batch

        output = self(data)

        loss = self.loss_fn(output, label)

        preds = output.argmax(1)
        targets = label.argmax(1)
        acc = (preds == targets).float().mean()

        self.log(f"{stage}_loss", loss, on_step=False, on_epoch=True, prog_bar=True)

        self.log(f"{stage}_acc", acc, on_step=False, on_epoch=True, prog_bar=True)
        return loss
    
    def val_step(self, batch, stage):

        data, label = batch

        output = self(data)

        loss = self.loss_fn(output, label)

        preds = output.argmax(1)

        targets = label.argmax(1)

        acc = (preds == targets).float().mean()

        self.log(f"{stage}_loss", loss, on_step=False, on_epoch=True, prog_bar=True)

        self.log(f"{stage}_acc", acc, on_step=False, on_epoch=True, prog_bar=True)
        
        return loss
    

    def training_step(self, batch, _):

      return self.train_step(batch, "train")

    def validation_step(self, batch, _):

      return self.val_step(batch, "val")

    def configure_optimizers(self):
      return torch.optim.SGD(self.net.parameters(), lr=self.hparams.lr)


model = MNISTLit()

trainer = pl.Trainer(max_epochs=epochs, enable_progress_bar=True)

trainer.fit(model, train_loader, val_loader)
