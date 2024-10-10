from abc import ABC, abstractmethod

from carcassonne_engine.models import SerializedGameWithID


class Agent(ABC):
    @abstractmethod
    def policy(self, prob: float, action: SerializedGameWithID, q: float) -> float: ...

    @abstractmethod
    def rollout(self, action: SerializedGameWithID, mid_scores: dict[int, int]) -> float: ...
