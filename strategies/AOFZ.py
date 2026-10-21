
from accounting import Accounting
from datafeeder import DataFeeder

from typing import Callable
from strategies.generic import StrategyBase

class StrategyOFZ(StrategyBase):
    """Стратегия на ОФЗ: фиксированные купоны против флоатеров с хеджем через IRS."""

    def __init__(self, id: str, datafeeder: DataFeeder, do_need_position: Callable[[Accounting, float], None], get_capital: Callable[[str], float], fixes: list[Accounting], floaters: list[Accounting], irs:list[Accounting]):
        """
        Args:
            datafeeder: источник рыночных данных.
            do_need_position: функция, задающая целевую позицию.
            fixes: Accounting по ОФЗ с фиксированным купоном.
            floaters: Accounting по ОФЗ с плавающим купоном.
            irs: Accounting по открытым позициям IRS.
        """
        super().__init__(id, datafeeder, do_need_position, get_capital)
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
            self.do_need_position(self.fixes[0], -1)
            self.do_need_position(self.floaters[0], 1)
            self.do_need_position(self.irs[0], -1)
            # Если такого IRS нет, то создаём Accounting для IRS в этом месте. Передаём его в orderProcessor.DoNeedPosition.
