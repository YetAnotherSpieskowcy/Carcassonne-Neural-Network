from src.agents import GreedyAgent, RandomAgent
from src.game import Game


def test_random_agent_game(engine, small_tileset):
    Game(engine, small_tileset).run(RandomAgent(), RandomAgent())

def test_greedy_agent_game(engine, small_tileset):
    Game(engine, small_tileset).run(GreedyAgent(0), GreedyAgent(1))
