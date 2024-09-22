from carcassonne_engine.models import SerializedGameWithID

from . import Agent


class GreedyAgent(Agent):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.ID = id

    def policy(self, prob: float, action: SerializedGameWithID, q: float) -> float:
        """
        Policy evaluation function.
        Action is assigned it's point value.
        """
        return float(action.game.players[self.ID].score)

    def rollout(self, action: SerializedGameWithID) -> float:
        """
        Simulates outcome of specific state
        Action is assigned it's point value.
        """
        return float(action.game.players[self.ID].score)
