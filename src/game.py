from pathlib import Path

from carcassonne_engine import GameEngine, TileSet, tiletemplates
from carcassonne_engine.models import SerializedGameWithID
from carcassonne_engine.requests import PlayTurnRequest

import utils
from dispatch import GameDispatch
from tokens import Timeout
from tree import Tree

with GameEngine(1, Path("./logs")) as engine:
    tile = tiletemplates.roads_turn()
    t1 = tiletemplates.monastery_with_single_road()
    t2 = tiletemplates.roads_turn()
    tiles = [t1, t2, t1]
    tile_set = TileSet.from_tiles(
        tiles,
        starting_tile=tiletemplates.single_city_edge_straight_roads(),
    )
    game = engine.generate_game(tile_set)
    for i in range(3):
        tree = Tree(game, GameDispatch(engine))
        tree.populate(Timeout(2))
        move = tree.execute().move
        resp = engine.send_play_turn_batch(
            [PlayTurnRequest(game_id=game.id, move=move)]
        )[0]
        utils.assert_no_exception(resp)
        assert resp.game is not None
        game = SerializedGameWithID(resp.game_id, resp.game)
        print("turn")
