from typing import Literal
import decimal
from instrument_info import InstrumentInfo

class Deal:
    def __init__(self, iinfo: InstrumentInfo, side: Literal['Buy', 'Sell'], quantity: float, price: float):
        self.iinfo = iinfo
        self.side = side
        self.quantity = quantity
        self.price = price

class Accounting:
    """Учёт позиции, сделок и денег по одному инструменту.

    Является источником информации о текущем состоянии портфеля для Strategy
    и источником данных для PerformanceReporter.
    Создавать только через AccountingController.create_accounting().
    """

    def __init__(self, instrument_info: InstrumentInfo):
        """
        Args:
            instrument_info: инструмент, по которому ведётся учёт.
        """
        self.instrument_info = instrument_info
        self.deals: list[Deal] = []

    def on_deal(self, side:Literal['Buy','Sell'], quantity: float, price: float):
        """Обработать исполненную сделку (из симулятора или от брокера/биржи)
        и обновить позицию и деньги. Не реализовано.
        """
        new_deal = Deal(self.instrument_info, side, quantity, price)
        self.deals.append(new_deal)
        


class AccountingController:
# Всё accounting создаётся и управляется через этот контроллер.
    """Реестр всех объектов Accounting в системе.

    OrderProcessor проверяет по нему, что работает с зарегистрированным Accounting.
    """

    def __init__(self):
        self.accountings: list[Accounting] = []

    def create_accounting(self, instrument_info: InstrumentInfo) -> Accounting:
        """Создать Accounting для инструмента и зарегистрировать его в контроллере.

        Args:
            instrument_info: инструмент, для которого заводится учёт.

        Returns:
            Новый объект Accounting.
        """
        new_accounting = Accounting(instrument_info)
        self.accountings.append(new_accounting)
        return new_accounting
