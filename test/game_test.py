from carcassonne_engine.tilesets import standard_tile_set
from src.agents import GreedyAgent, RandomAgent
from src.game import Game

import pytest


def test_random_agent_game(engine, small_tileset):
    Game(engine, small_tileset).run(RandomAgent(), RandomAgent())


def test_greedy_agent_game(engine, small_tileset):
    Game(engine, small_tileset).run(GreedyAgent(0), GreedyAgent(1))


@pytest.mark.skip()
def test_greedy_agent_full_game(engine):
    Game(engine, standard_tile_set()).run(GreedyAgent(0), GreedyAgent(1))
