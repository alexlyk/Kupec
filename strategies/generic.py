
from accounting import Accounting
from datafeeder import DataFeeder
from orderprocessor import OrderProcessor

class CapitalHandler:
    def __init__(self):
        pass

    def get_current_capital(self):
        pass

    def set_capital(self):
        pass

class StrategyBase:
    """Базовый класс торговой стратегии.

    Получает рыночные данные из DataFeeder, принимает решения и передаёт
    целевые позиции в OrderProcessor через DoNeedPosition().
    """

    def __init__(self, datafeeder: DataFeeder, orderProcessor: OrderProcessor, capitalHandler: CapitalHandler):
        """
        Args:
            datafeeder: источник рыночных данных.
            orderProcessor: исполнитель целевых позиций.
        """
        self.datafeeder = datafeeder
        self.orderProcessor = orderProcessor
        self.capitalHandler = capitalHandler

    def on_execute(self):
        """Один шаг стратегии (например, по событию OnDayEnd от Datafeed).
        Реализуется в наследниках.
        """
        raise NotImplementedError("Subclasses should implement this!")


