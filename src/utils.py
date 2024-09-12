from carcassonne_engine.requests import BaseResponse


def assert_no_exception(resp: BaseResponse):
    if resp.exception is not None:
        print(resp.exception)
        assert resp.exception is None
