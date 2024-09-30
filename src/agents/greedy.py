from carcassonne_engine.models import SerializedGameWithID

from . import Agent


class GreedyAgent(Agent):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id

    def policy(self, prob: float, action: SerializedGameWithID, q: float) -> float:
        """
        Policy evaluation function.
        Action is assigned its point value.
        """
        return float(action.game.players[self.ID].score)

    def rollout(self, action: SerializedGameWithID, mid_scores: dict[int, int]) -> float:
        """
        Simulates outcome of specific state
        Action is assigned its point value.
        """
        return float(mid_scores[self.ID+1])
