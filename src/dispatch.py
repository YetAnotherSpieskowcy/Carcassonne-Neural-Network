from carcassonne_engine import GameEngine, SerializedGame
from carcassonne_engine.models import SerializedGameWithID
from carcassonne_engine.requests import (GetLegalMovesRequest,
                                         GetRemainingTilesRequest,
                                         MoveWithState, PlayTurnRequest, Tile)

import utils


class GameDispatch:
    def __init__(self, engine: GameEngine) -> None:
        self.engine = engine

    def destroy(self, game: SerializedGameWithID) -> None:
        # self.engine.delete_games([game.id])
        ...

    def simulate_move(
        self, game: SerializedGameWithID, move: MoveWithState
    ) -> SerializedGame:
        """
        Perform a move on a cloned game and return the resulting game
        """
        clone = self.engine.sub_clone_game(game.id, 1)[0]
        (resp,) = self.engine.send_play_turn_batch(
            [PlayTurnRequest(game_id=clone, move=move.move)]
        )
        utils.assert_no_exception(resp)
        assert resp.game is not None
        return SerializedGameWithID(resp.game_id, resp.game)

    def gen_initial_states(self, game: int, tile: Tile) -> list[MoveWithState]:
        assert tile is not None
        (resp,) = self.engine.send_get_legal_moves_batch(
            [GetLegalMovesRequest(base_game_id=game, tile_to_place=tile)]
        )
        utils.assert_no_exception(resp)
        assert resp.moves is not None
        return resp.moves

    def gen_states(self, game: int) -> tuple[list[MoveWithState], list[float]]:
        (resp,) = self.engine.send_get_remaining_tiles_batch(
            [GetRemainingTilesRequest(base_game_id=game)]
        )
        utils.assert_no_exception(resp)
        assert resp.tile_probabilities is not None
        r = []
        ps = []
        for tile in resp.tile_probabilities:
            ps.append(tile.probability)
            r.append(GetLegalMovesRequest(base_game_id=game, tile_to_place=tile.tile))
        rr = self.engine.send_get_legal_moves_batch(r)
        states = []
        probs: list[float] = []
        i = 0
        for re in rr:
            utils.assert_no_exception(re)
            assert re.moves is not None
            moves: list[MoveWithState] = re.moves
            for move in moves:
                probs.append(ps[i])
                states.append(move)
            i += 1
        return (states, probs)
