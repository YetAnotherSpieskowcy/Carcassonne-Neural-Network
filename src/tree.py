import math
import random

from carcassonne_engine.models import SerializedGameWithID
from carcassonne_engine.requests import MoveWithState

from dispatch import GameDispatch
from tokens import CancelationToken

DISCOUNT_FACTOR = 0.9
EXPLORATION_WEIGHT = 0.01


class Tree:
    def __init__(
        self, initial_game: SerializedGameWithID, dispatch: GameDispatch
    ) -> None:
        self.initial_game = initial_game
        states = dispatch.gen_initial_states(
            initial_game.id, initial_game.game.current_tile
        )
        prob = [1.0 for _ in states]
        self.root = Node(dispatch)

        self.root.state = initial_game
        self.root.states = states
        self.root.probabilities = prob

    def populate(self, token: CancelationToken) -> None:
        while token():
            self.root.select(0)

    def execute(self) -> MoveWithState:
        return max(self.root.children, key=lambda it: it.q / it.selection_count).action


class Node:
    def __init__(self, dispatch: GameDispatch) -> None:
        self.is_expanded: bool = False
        self.q: float = 0
        self.selection_count: int = 1
        self.dispatch: GameDispatch = dispatch
        self.children: list[Node] = []
        self.state: SerializedGameWithID | None = None

    def __del__(self):
        if self.state is not None:
            self.dispatch.destroy(self.state)

    def expand(self, state: SerializedGameWithID, action) -> None:
        self.action: MoveWithState = action
        self.state = self.dispatch.simulate_move(state, action)
        states, probabilities = self.dispatch.gen_states(self.state.id)
        self.states: list[MoveWithState] = states
        self.probabilities: list[float] = probabilities

    def select(self, depth: int) -> float:
        # Expand every child node
        cum_q: float = 0
        if not self.is_expanded:
            for action in self.states:
                # Simulate remaining game states
                n = Node(self.dispatch)
                assert self.state is not None
                n.expand(self.state, action)
                n.q = rollout(n)
                cum_q += n.q
                self.children.append(n)
            self.is_expanded = True
        if len(self.children) == 0:
            # Game has ended return score based on the outcome
            return 0
        # Select most promising action according to policy
        selected_pair: tuple[float, Node] = max(
            zip(self.probabilities, self.children), key=lambda it: policy(it, cum_q)
        )
        selected = selected_pair[1]
        selected.selection_count += 1
        # Update q values of preceding nodes
        cum_q += selected.select(depth + 1)
        self.q += cum_q
        return cum_q * math.pow(DISCOUNT_FACTOR, depth) * selected_pair[0]


def upper_confidence_bound(pi: float, n: int, q: float) -> float:
    return pi + EXPLORATION_WEIGHT * math.sqrt(math.log(1 + q) / n)


def policy(action: tuple[float, Node], q: float) -> float:
    """
    Policy evaluation function.
    Currently action is assigned random value until
    YetAnotherSpieskowcy/Carcassonne-Neural-Network/Policy network#4
    is finished.
    """
    rng = random.Random()
    return upper_confidence_bound(rng.random(), action[1].selection_count, q)


def rollout(action: Node) -> float:
    """
    Simulates outcome of specific state
    Currently action is assigned random value until
    YetAnotherSpieskowcy/Carcassonne-Neural-Network/Value network#3
    is finished.
    """
    rng = random.Random()
    return rng.random() + 1
