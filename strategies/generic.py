
from accounting import Accounting
from datafeeder import DataFeeder
from orderprocessor import OrderProcessor

class CapitalHandler:
    """Единый реестр капитала, выделенного стратегиям, по их id."""

    def __init__(self):
        self.capital: dict[str, float] = {}

    def get_current_capital(self, strategy_id: str) -> float:
        return self.capital[strategy_id]

    def set_capital(self, strategy_id: str, capital: float):
        self.capital[strategy_id] = capital

class StrategyBase:
    """Базовый класс торговой стратегии.

    Получает рыночные данные из DataFeeder, принимает решения и передаёт
    целевые позиции в OrderProcessor через DoNeedPosition().
    """

    def __init__(self, id: str, datafeeder: DataFeeder, orderProcessor: OrderProcessor, capitalHandler: CapitalHandler):
        """
        Args:
            id: уникальное имя стратегии.
            datafeeder: источник рыночных данных.
            orderProcessor: исполнитель целевых позиций.
            capitalHandler: реестр капитала стратегий.
        """
        self.id = id
        self.datafeeder = datafeeder
        self.orderProcessor = orderProcessor
        self.capitalHandler = capitalHandler

    def on_execute(self):
        """Один шаг стратегии (например, по событию OnDayEnd от Datafeed).
        Реализуется в наследниках.
        """
        raise NotImplementedError("Subclasses should implement this!")
