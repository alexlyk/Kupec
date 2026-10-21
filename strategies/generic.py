
from typing import Callable
from accounting import Accounting
from datafeeder import DataFeeder

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
    целевые позиции через функцию do_need_position (обычно OrderProcessor.DoNeedPosition).
    """

    def __init__(self, id: str, datafeeder: DataFeeder, do_need_position: Callable[[Accounting, float], None],
                 get_capital: Callable[[str], float]):
        """
        Args:
            id: уникальное имя стратегии.
            datafeeder: источник рыночных данных.
            do_need_position: функция (accounting, quantity), задающая целевую позицию; знак quantity задаёт направление.
            get_capital: функция id стратегии -> её капитал (обычно CapitalHandler.get_current_capital).
        """
        self.id = id
        self.datafeeder = datafeeder
        self.do_need_position = do_need_position
        self.get_capital = get_capital

    def on_execute(self):
        """Один шаг стратегии (например, по событию OnDayEnd от Datafeed).
        Реализуется в наследниках.
        """
        raise NotImplementedError("Subclasses should implement this!")
