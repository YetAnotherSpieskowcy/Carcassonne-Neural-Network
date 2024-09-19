import pytest
from carcassonne_engine import GameEngine, TileSet, tiletemplates


@pytest.fixture
def engine(tmp_path):
    with GameEngine(1, tmp_path) as engine:
        yield engine


@pytest.fixture
def small_tileset():
    t1 = tiletemplates.monastery_with_single_road()
    t2 = tiletemplates.roads_turn()
    tiles = [t1, t2, t1]
    return TileSet.from_tiles(
        tiles,
        starting_tile=tiletemplates.single_city_edge_straight_roads(),
    )
