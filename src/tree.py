import math

from carcassonne_engine.models import SerializedGameWithID
from carcassonne_engine.requests import MoveWithState

from tqdm import tqdm

from .agents import Agent
from .dispatch import GameDispatch
from .tokens import CancelationToken
from .utils import upper_confidence_bound

DISCOUNT_FACTOR = 0.9
EXPLORATION_WEIGHT = 0.01


class Tree:
    def __init__(
        self, agent: Agent, initial_game: SerializedGameWithID, dispatch: GameDispatch
    ) -> None:
        self.initial_game = dispatch.sub_clone(initial_game)
        states = dispatch.gen_initial_states(
            self.initial_game.id, self.initial_game.game.current_tile
        )
        prob = [1.0 for _ in states]
        self.root = Node(dispatch, self)

        self.root.state = self.initial_game
        self.root.states = states
        self.root.probabilities = prob
        self.agent: Agent = agent

    def populate(self, token: CancelationToken) -> None:
        while token():
            self.root.select(0)

    def execute(self) -> MoveWithState:
        return max(self.root.children, key=lambda it: it.q / it.selection_count).action


class Node:
    def __init__(self, dispatch: GameDispatch, tree: Tree) -> None:
        self.is_expanded: bool = False
        self.q: float = 0
        self.selection_count: int = 1
        self.dispatch: GameDispatch = dispatch
        self.children: list[Node] = []
        self.state: SerializedGameWithID | None = None
        self.tree: Tree = tree

    #def __del__(self):
    #    if self.state is not None:
    #        self.dispatch.destroy(self.state)

    def expand(self, state: SerializedGameWithID, action) -> None:
        self.action: MoveWithState = action
        self.state = self.dispatch.simulate_move(state, action)
        states, probabilities = self.dispatch.gen_states(self.state.id)
        self.states: list[MoveWithState] = states
        self.probabilities: list[float] = probabilities

    def select(self, depth: int) -> float:
        # Expand every child node
        if not self.is_expanded:
            cum_q: float = 0
            for action in tqdm(self.states, desc=f"Expansion at depth {depth}"):
                # Simulate remaining game states
                child = Node(self.dispatch, self.tree)
                assert self.state is not None
                child.expand(self.state, action)
                child.q = self.tree.agent.rollout(child.state)
                cum_q += child.q
                self.children.append(child)
            self.is_expanded = True
            return cum_q
        else:
            if len(self.children) == 0:
                # Game has ended return score based on the outcome
                return 0
            # Select most promising action according to policy
            selected_pair: tuple[float, Node] = max(
                zip(self.probabilities, self.children),
                key=lambda it: upper_confidence_bound(
                    self.tree.agent.policy(it[0], it[1].state, self.q),
                    it[1].selection_count,
                    self.q,
                    EXPLORATION_WEIGHT,
                ),
            )
            selected = selected_pair[1]
            selected.selection_count += 1
            # Update q values of preceding nodes
            self.q += selected.select(depth + 1)
            return self.q * math.pow(DISCOUNT_FACTOR, depth) * selected_pair[0]
