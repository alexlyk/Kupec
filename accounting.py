from typing import Literal, Callable
from datetime import datetime
from instrument_info import InstrumentInfo

class Deal:
    def __init__(self, iinfo: InstrumentInfo, side: Literal['Buy', 'Sell'], quantity: float, price: float, timestamp, owner: str):
        self.iinfo = iinfo
        self.side = side
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp  # время сделки по таймеру
        self.owner = owner          # id стратегии-владельца

class Accounting:
    """Учёт позиции, сделок и денег по одному инструменту.

    Является источником информации о текущем состоянии портфеля для Strategy
    и источником данных для PerformanceReporter.
    Создавать только через AccountingController.create_accounting().
    """

    def __init__(self, instrument_info: InstrumentInfo, owner: str, now: Callable[[], datetime]):
        """
        Args:
            instrument_info: инструмент, по которому ведётся учёт.
            owner: id стратегии, которой принадлежит accounting.
            now: функция, возвращающая текущее время, для таймстемпов сделок.
        """
        self.instrument_info = instrument_info
        self.owner = owner
        self.now = now
        self.deals: list[Deal] = []
        self.position = 0.0  # знак: + длинная, - короткая
        self.cash = 0.0      # деньги, полученные/потраченные по сделкам

    def on_deal(self, side: Literal['Buy', 'Sell'], quantity: float, price: float):
        """Обработать исполненную сделку (из симулятора или от брокера/биржи)
        и обновить позицию и деньги.
        """
        self.deals.append(Deal(self.instrument_info, side, quantity, price, self.now(), self.owner))
        sign = 1 if side == 'Buy' else -1
        self.position += sign * quantity
        self.cash -= sign * quantity * price

    @property
    def turnover(self) -> float:
        """Суммарный оборот по сделкам в деньгах."""
        return sum(d.quantity * d.price for d in self.deals)

    def value(self, price: float) -> float:
        """Стоимость счёта: деньги + позиция по рыночной цене."""
        return self.cash + self.position * price


class AccountingController:
# Всё accounting создаётся и управляется через этот контроллер.
    """Реестр всех объектов Accounting в системе.

    OrderProcessor проверяет по нему, что работает с зарегистрированным Accounting.
    """

    def __init__(self, now: Callable[[], datetime]):
        self.now = now
        self.accountings: list[Accounting] = []

    def create_accounting(self, instrument_info: InstrumentInfo, owner: str) -> Accounting:
        """Создать Accounting для инструмента и зарегистрировать его в контроллере.

        Args:
            instrument_info: инструмент, для которого заводится учёт.
            owner: id стратегии-владельца.

        Returns:
            Новый объект Accounting.
        """
        new_accounting = Accounting(instrument_info, owner, self.now)
        self.accountings.append(new_accounting)
        return new_accounting
