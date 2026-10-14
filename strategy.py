
from accounting import Accounting
from datafeeder import DataFeeder
from orderprocessor import OrderProcessor

class StrategyBase:
    """Базовый класс торговой стратегии.

    Получает рыночные данные из DataFeeder, принимает решения и передаёт
    целевые позиции в OrderProcessor через DoNeedPosition().
    """

    def __init__(self, datafeeder: DataFeeder, orderProcessor: OrderProcessor):
        """
        Args:
            datafeeder: источник рыночных данных.
            orderProcessor: исполнитель целевых позиций.
        """
        self.datafeeder = datafeeder
        self.orderProcessor = orderProcessor

    def on_execute(self):
        """Один шаг стратегии (например, по событию OnDayEnd от Datafeed).
        Реализуется в наследниках.
        """
        raise NotImplementedError("Subclasses should implement this!")



class StrategyOFZ(StrategyBase):
    """Стратегия на ОФЗ: фиксированные купоны против флоатеров с хеджем через IRS."""

    def __init__(self, datafeeder: DataFeeder, orderProcessor: OrderProcessor, fixes: list[Accounting], floaters: list[Accounting], irs:list[Accounting]):
        """
        Args:
            datafeeder: источник рыночных данных.
            orderProcessor: исполнитель целевых позиций.
            fixes: Accounting по ОФЗ с фиксированным купоном.
            floaters: Accounting по ОФЗ с плавающим купоном.
            irs: Accounting по открытым позициям IRS.
        """
        super().__init__(datafeeder, orderProcessor)
        self.fixes = fixes
        self.floaters = floaters
        self.irs = irs # opened positions for IRS

    def on_execute(self):
        """Сравнить цены первого фикса и первого флоатера; если фикс дороже —
        нужны: короткая позиция по фиксу, длинная по флоатеру, короткая по IRS.
        """
        px1 = self.datafeeder.get_price(self.fixes[0].instrument_info)
        px2 = self.datafeeder.get_price(self.floaters[0].instrument_info)
        if px1 > px2:
            self.orderProcessor.DoNeedPosition(self.fixes[0], "SELL")
            self.orderProcessor.DoNeedPosition(self.floaters[0], "BUY")
            self.orderProcessor.DoNeedPosition(self.irs[0], "SELL")
            # Если такого IRS нет, то создаём Accounting для IRS в этом месте. Передаём его в orderProcessor.DoNeedPosition.
