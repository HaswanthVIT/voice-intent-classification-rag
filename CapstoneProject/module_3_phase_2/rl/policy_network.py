import torch
import torch.nn as nn

class IntentPolicyNetwork(nn.Module):
    def __init__(self, input_dim=15, output_dim=6):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.SiLU(),
            nn.Linear(64, 64),
            nn.SiLU(),
            nn.Linear(64, output_dim),
            nn.Softplus()
        )

    def forward(self, x):
        return self.net(x)