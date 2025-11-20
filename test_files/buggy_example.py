"""
Sample PyTorch training script with bugs for testing the analyzer.
This file is public - it contains NO proprietary analyzer code.
"""

import torch
import torch.nn as nn
import torch.optim as optim


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)


def train_missing_backward():
    """BUG: Missing loss.backward() before optimizer.step()"""
    model = SimpleModel()
    optimizer = optim.Adam(model.parameters())
    criterion = nn.CrossEntropyLoss()

    data = torch.randn(32, 128)
    target = torch.randint(0, 10, (32,))

    optimizer.zero_grad()
    output = model(data)
    loss = criterion(output, target)
    # BUG: Missing loss.backward() here!
    optimizer.step()


def train_conditional_bug(use_amp=False):
    """BUG: Missing backward in else branch"""
    model = SimpleModel()
    optimizer = optim.Adam(model.parameters())
    criterion = nn.CrossEntropyLoss()

    data = torch.randn(32, 128)
    target = torch.randint(0, 10, (32,))

    optimizer.zero_grad()
    output = model(data)
    loss = criterion(output, target)

    if use_amp:
        loss.backward()
    else:
        # BUG: Missing backward in else branch
        pass

    optimizer.step()


if __name__ == "__main__":
    train_missing_backward()
# Test change to trigger workflow
