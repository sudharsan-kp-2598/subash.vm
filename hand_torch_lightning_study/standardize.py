import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

epochs, lr, batch_size = 20, 2.0, 32


dataset = datasets.MNIST(
    root="data",
    train=True,
    transform=transforms.ToTensor(),  
    download=True
)

loader = DataLoader(dataset, batch_size=60000, shuffle=False)


images, _ = next(iter(loader)) 
print("Shape:", images.shape)  

pixels = images.view(-1)

mean = pixels.mean()
std = pixels.std()

print(mean)
print(std)

print(f"Mean: {mean.item():.6f}")
print(f"Std: {std.item():.6f}")