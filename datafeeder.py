from instrument_info import InstrumentInfo

class DataFeeder:
    """Базовый класс поставщика рыночных данных (historical / live / on-demand).

    Конкретные источники данных реализуются в наследниках.
    """

    def __init__(self):
        pass

    def get_price(self, instrument: InstrumentInfo):
        """Вернуть текущую цену инструмента. Реализуется в наследниках.

        Args:
            instrument: инструмент, цену которого нужно получить.
        """
        raise NotImplementedError("Subclasses should implement this!")
