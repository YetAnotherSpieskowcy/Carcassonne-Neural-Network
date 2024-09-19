import math

from carcassonne_engine.requests import BaseResponse


def upper_confidence_bound(pi: float, n: int, q: float, exp_weight: float) -> float:
    return pi + exp_weight * math.sqrt(math.log(1 + q) / n)


def assert_no_exception(resp: BaseResponse):
    if resp.exception is not None:
        print(resp.exception)
        assert resp.exception is None
