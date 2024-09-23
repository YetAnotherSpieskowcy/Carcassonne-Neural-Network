import random

from carcassonne_engine.models import SerializedGameWithID

from . import Agent


class RandomAgent(Agent):
    def policy(self, prob: float, action: SerializedGameWithID, q: float) -> float:
        """
        Policy evaluation function.
        Action is assigned random value.
        """
        rng = random.Random()
        return rng.random()

    def rollout(self, action: SerializedGameWithID, mid_scores: dict[int, int]) -> float:
        """
        Simulates outcome of specific state
        Action is assigned random value.
        """
        rng = random.Random()
        return rng.random() + 1
