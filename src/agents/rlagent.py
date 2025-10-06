import torch
from torch import nn, optim
import torch.nn.functional as F
import numpy as np

from carcassonne_engine.models import SerializedGameWithID

from . import Agent


class Net(nn.Module):
    def __init__(self, board_size, num_tile_types):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(num_tile_types + 1, 128, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(128)
        self.conv2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.policy_conv = nn.Conv2d(64, 4, kernel_size=1)
        self.policy_bn = nn.BatchNorm2d(4)
        self.policy_fc = nn.Linear(4 * board_size * board_size, 1)
        self.value_conv = nn.Conv2d(64, 2, kernel_size=1)
        self.value_bn = nn.BatchNorm2d(2)
        self.value_fc1 = nn.Linear(2 * board_size * board_size, 256)
        self.value_fc2 = nn.Linear(256, 1)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))

        policy = F.relu(self.policy_bn(self.policy_conv(x)))
        policy = policy.view(policy.size(0), -1)
        policy = F.log_softmax(self.policy_fc(policy), dim=1)
        value = F.relu(self.value_bn(self.value_conv(x)))
        value = value.view(value.size(0), -1)
        value = F.relu(self.value_fc1(value))
        value = torch.tanh(self.value_fc2(value))

        return policy, value


class RLAgent(Agent):
    def __init__(self, board_size, num_tile_types, lr=0.001, weight_decay=1e-4):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = Net(board_size, num_tile_types).to(self.device)
        self.optimizer = optim.Adam(
            self.net.parameters(), lr=lr, weight_decay=weight_decay
        )

    def policy(self, prob: float, action: SerializedGameWithID, q: float) -> float:
        board_tensor = action.game.binary_tiles().unsqueeze(0).to(self.device)
        with torch.no_grad():
            policy, _ = self.net(board_tensor)
        return prob * policy.item()

    def rollout(
        self, action: SerializedGameWithID, mid_scores: dict[int, int]
    ) -> float:
        board_tensor = action.game.binary_tiles().unsqueeze(0).to(self.device)
        with torch.no_grad():
            _, value = self.net(board_tensor)
        return value.item()

    def reward(self, back: list):
        self.optimizer.zero_grad()

        total_policy_loss = 0
        total_value_loss = 0

        for board, pi, v in back:
            board_tensor = board.game.binary_tiles().unsqueeze(0).to(self.device)
            target_pi = torch.FloatTensor(pi).to(self.device)
            target_v = torch.FloatTensor([v]).to(self.device)

            out_log_pi, out_v = self.net(board_tensor)

            policy_loss = -torch.sum(target_pi * out_log_pi) / target_pi.size()[0]
            value_loss = F.mse_loss(out_v.view(-1), target_v)

            total_policy_loss += policy_loss
            total_value_loss += value_loss

        total_loss = total_policy_loss + total_value_loss
        total_loss.backward()
        self.optimizer.step()
