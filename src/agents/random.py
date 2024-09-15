import random

from carcassonne_engine.models import SerializedGameWithID

from . import Agent


class RandomAgent(Agent):
    def policy(self, prob: float, action: SerializedGameWithID, q: float) -> float:
        """
        Policy evaluation function.
        Currently action is assigned random value until
        YetAnotherSpieskowcy/Carcassonne-Neural-Network/Policy network#4
        is finished.
        """
        rng = random.Random()
        return rng.random()

    def rollout(self, action: SerializedGameWithID) -> float:
        """
        Simulates outcome of specific state
        Currently action is assigned random value until
        YetAnotherSpieskowcy/Carcassonne-Neural-Network/Value network#3
        is finished.
        """
        rng = random.Random()
        return rng.random() + 1
