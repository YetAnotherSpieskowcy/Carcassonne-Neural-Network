from carcassonne_engine import GameEngine, TileSet
from carcassonne_engine.models import SerializedGameWithID
from carcassonne_engine.requests import PlayTurnRequest

from .agents import Agent
from .dispatch import GameDispatch
from .tokens import Timeout
from .tree import Tree
from .utils import assert_no_exception


class Game:
    def __init__(self, engine: GameEngine, tileset: TileSet):
        self.engine: GameEngine = engine
        self.tileset: TileSet = tileset

    def run(self, *agents: Agent):
        game: SerializedGameWithID = self.engine.generate_game(self.tileset)
        agent_ptr = 0
        while game.game.current_tile is not None:
            tree = Tree(agents[agent_ptr], game, GameDispatch(self.engine))
            tree.populate(Timeout(2))
            move = tree.execute().move
            resp = self.engine.send_play_turn_batch(
                [PlayTurnRequest(game_id=game.id, move=move)]
            )[0]
            assert_no_exception(resp)
            assert resp.game is not None
            game = SerializedGameWithID(resp.game_id, resp.game)
            agent_ptr += 1
            if agent_ptr >= len(agents):
                agent_ptr = 0
        print("Game concluded")
