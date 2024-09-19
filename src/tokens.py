import time


class CancelationToken:
    def __call__(self, *args, **kwds) -> bool:
        return True


class IterationLimit(CancelationToken):
    def __call__(self, *args, **kwds) -> bool:
        self.iterations -= 1
        return self.iterations > 0

    def __init__(self, iterations) -> None:
        self.iterations = iterations


class Timeout(CancelationToken):
    def __call__(self, *args, **kwds) -> bool:
        return time.time() < self.timeout

    def __init__(self, timeout) -> None:
        self.timeout = time.time() + timeout
