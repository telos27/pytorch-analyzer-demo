#!/usr/bin/env python3
"""
Example PyTorch training script with gradient management bug.
This file contains a bug that should be detected by the CLI bug detector.
"""

import torch
import torch.nn as nn
import torch.optim as optim

def train_model_with_bug():
    """Training function with missing backward() call"""

    # Setup model and optimizer
    model = nn.Linear(10, 1)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    # Simulate training data
    inputs = torch.randn(32, 10)
    targets = torch.randn(32, 1)

    # Training step with BUG
    optimizer.zero_grad()

    # Forward pass
    outputs = model(inputs)
    loss = criterion(outputs, targets)

    # BUG: Missing loss.backward() here!
    # The gradients are never computed

    optimizer.step()  # This should be flagged as a bug!

    print(f"Loss: {loss.item()}")

def another_buggy_function():
    """Another function with the same bug pattern"""

    optimizer = optim.SGD([torch.tensor([1.0], requires_grad=True)], lr=0.1)

    optimizer.zero_grad()
    loss = torch.tensor(5.0, requires_grad=True)

    # Missing loss.backward() again!
    optimizer.step()  # Another bug here

if __name__ == "__main__":
    train_model_with_bug()
    another_buggy_function()