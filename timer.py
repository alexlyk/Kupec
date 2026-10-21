from datetime import datetime

class Timer:
    """Часы бэктеста: время двигает Environment, остальные получают метод Now как функцию.

    В живой торговле вместо него можно передать любую функцию без аргументов,
    например datetime.now.
    """

    def __init__(self):
        self._time: datetime = None

    def Now(self) -> datetime:
        return self._time
