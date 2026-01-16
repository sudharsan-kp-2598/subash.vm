import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import random
import os
import urllib.request
import gzip
import pickle
import numpy as np

###### Config ######

seed = 42  
epochs = 60
lr = 2
batch_size = 16

random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
os.environ["PYTHONHASHSEED"] = str(seed)

####################

mnist_url = "https://github.com/mnielsen/neural-networks-and-deep-learning/raw/master/data/mnist.pkl.gz"
mnist_filename = "mnist.pkl.gz"

if not os.path.exists(mnist_filename):
    print("Downloading MNIST data...")
    urllib.request.urlretrieve(mnist_url, mnist_filename)
    print("Download complete.")
else:
    print("MNIST data already exists.")


def load_data():

    with gzip.open("mnist.pkl.gz", "rb") as f:
        training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    return (training_data, validation_data, test_data)

def one_hot(j):

    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

def data_builder():


    tr_d, va_d, _ = load_data()

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [one_hot(y) for y in tr_d[1]]

    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_results = [one_hot(y) for y in va_d[1]]

    #test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    #test_results = [one_hot(y) for y in te_d[1]]

    train_inputs = torch.tensor(np.array(training_inputs), dtype=torch.float32).squeeze(-1)
    train_labels = torch.tensor(np.array(training_results), dtype=torch.float32).squeeze(-1)

    val_inputs = torch.tensor(np.array(validation_inputs), dtype=torch.float32).squeeze(-1)
    val_labels = torch.tensor(np.array(validation_results), dtype=torch.float32).squeeze(-1)

    train_set = TensorDataset(train_inputs, train_labels)
    val_set = TensorDataset(val_inputs, val_labels)

    g = torch.Generator().manual_seed(seed)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True , generator= g)
    val_loader   = DataLoader(val_set, batch_size=batch_size, shuffle=False )

    return train_loader,val_loader

def build_model():
    model = nn.Sequential(
        nn.Linear(784, 50),
        nn.Sigmoid(),
        nn.Linear(50, 10),
        nn.Sigmoid(),
    )
    return model

def build_optimizer(model):
    return torch.optim.SGD(model.parameters(), lr=lr)

loss_functionn = nn.MSELoss()

def validate(model, val_loader):
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

def train(model, train_loader, val_loader, optimizer):
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
            train_correct += (output.argmax(1) == label.argmax(1)).sum().item()

        train_loss /= 50000
        train_acc = (train_correct / 50000) * 100

        val_loss, val_acc = validate(model, val_loader)

        print(
            f"Epoch {epoch+1}: "
            f"train_loss={train_loss:.6f}, train_acc={train_acc:.2f}%, "
            f"val_loss={val_loss:.6f}, val_acc={val_acc:.2f}%"
        )



def main():
    train_loader, val_loader = data_builder()
    model = build_model()
    optimizer = build_optimizer(model)

    train(model, train_loader, val_loader, optimizer)

if __name__ == "__main__":
    main()
