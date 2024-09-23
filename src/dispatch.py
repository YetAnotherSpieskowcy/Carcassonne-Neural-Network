from carcassonne_engine import GameEngine, SerializedGame
from carcassonne_engine.models import SerializedGameWithID
from carcassonne_engine.requests import (
    GetLegalMovesRequest,
    GetMidGameScoreRequest,
    GetRemainingTilesRequest,
    MoveWithState,
    PlayTurnRequest,
    Tile,
)

from .utils import assert_no_exception


class GameDispatch:
    def __init__(self, engine: GameEngine) -> None:
        self.engine = engine

    def destroy(self, game: SerializedGameWithID) -> None:
        self.engine.delete_games([game.id])

    def sub_clone(self, game: SerializedGameWithID) -> SerializedGameWithID:
        cloned = SerializedGameWithID(
            self.engine.sub_clone_game(game.id, 1)[0], game.game
        )
        return cloned

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
        assert_no_exception(resp)
        assert resp.game is not None
        return SerializedGameWithID(resp.game_id, resp.game)

    def gen_initial_states(self, game_id: int, tile: Tile) -> list[MoveWithState]:
        assert tile is not None
        (resp,) = self.engine.send_get_legal_moves_batch(
            [GetLegalMovesRequest(base_game_id=game_id, tile_to_place=tile)]
        )
        assert_no_exception(resp)
        assert resp.moves is not None
        return resp.moves

    def gen_states(self, game_id: int) -> tuple[list[MoveWithState], list[float]]:
        (resp,) = self.engine.send_get_remaining_tiles_batch(
            [GetRemainingTilesRequest(base_game_id=game_id)]
        )
        assert_no_exception(resp)
        assert resp.tile_probabilities is not None
        move_requests = []
        ps = []
        for tile in resp.tile_probabilities:
            ps.append(tile.probability)
            move_requests.append(
                GetLegalMovesRequest(base_game_id=game_id, tile_to_place=tile.tile)
            )
        legal_moves = self.engine.send_get_legal_moves_batch(move_requests)
        states = []
        probs: list[float] = []
        i = 0
        for move_response in legal_moves:
            assert_no_exception(move_response)
            assert move_response.moves is not None
            moves: list[MoveWithState] = move_response.moves
            for move in moves:
                probs.append(ps[i])
                states.append(move)
            i += 1
        return (states, probs)
    
    def get_mid_scores(self, game: SerializedGameWithID) -> dict[int, int]:
        (resp,) = self.engine.send_get_mid_game_score_batch(
            [GetMidGameScoreRequest(base_game_id=game.id)]
        )
        assert_no_exception(resp)
        assert resp.player_scores is not None
        return resp.player_scores
