import gzip
import os
import pickle
import urllib.request

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

mnist_url = "https://github.com/mnielsen/neural-networks-and-deep-learning/raw/master/data/mnist.pkl.gz"
mnist_filename = "mnist.pkl.gz"

if not os.path.exists(mnist_filename):
    print("Downloading MNIST data...")
    urllib.request.urlretrieve(mnist_url, mnist_filename)
    print("Download complete.")
else:
    print("MNIST data already exists.")


def load_data():

    with gzip.open("/home/subash-nts0300/Hydra_DVC/run2/model1/mnist.pkl.gz", "rb") as f:
        training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    return (training_data, validation_data, test_data)


def one_hot(j):

    e = np.zeros((10, 1))
    e[j] = 1.0
    return e


def data_builder(cfg):

    tr_d, va_d, _ = load_data()

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [one_hot(y) for y in tr_d[1]]

    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_results = [one_hot(y) for y in va_d[1]]

    # test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    # test_results = [one_hot(y) for y in te_d[1]]

    train_inputs = torch.tensor(np.array(training_inputs), dtype=torch.float32).squeeze(
        -1
    )
    train_labels = torch.tensor(
        np.array(training_results), dtype=torch.float32
    ).squeeze(-1)

    val_inputs = torch.tensor(np.array(validation_inputs), dtype=torch.float32).squeeze(
        -1
    )
    val_labels = torch.tensor(
        np.array(validation_results), dtype=torch.float32
    ).squeeze(-1)

    train_set = TensorDataset(train_inputs, train_labels)
    val_set = TensorDataset(val_inputs, val_labels)

    g = torch.Generator().manual_seed(cfg["seed"])
    train_loader = DataLoader(
        train_set, batch_size=cfg["batch_size"], shuffle=True, generator=g
    )
    val_loader = DataLoader(val_set, batch_size=cfg["batch_size"], shuffle=False)

    return train_loader, val_loader
