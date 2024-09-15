from src.agents import RandomAgent
from src.game import Game


def test_random_agent_game(engine, small_tileset):
    Game(engine, small_tileset).run(RandomAgent(), RandomAgent())
