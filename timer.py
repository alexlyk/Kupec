class Timer:
    """Источник текущего времени системы.

    Кто двигает время, зависит от режима: в бэктесте это Environment,
    в живой торговле другой класс. Публичный метод один: Now().
    """

    def __init__(self):
        self._time = None

    def Now(self):
        return self._time
