from accounting import Accounting
from accounting import AccountingController
from datafeeder import DataFeeder


class OrderProcessor:
    """Преобразует целевые позиции от стратегии в заявки и управляет их исполнением.

    Работает в двух режимах: симуляция (сделки сразу попадают в Accounting)
    и реальная торговля через брокера/биржу. Режимы реализуются в наследниках.
    """

    def __init__(self, accountingController: AccountingController):
        """
        Args:
            accountingController: реестр Accounting, с которыми разрешено работать.
        """
        self.accountingController = accountingController

    def DoNeedPosition(self, accounting: Accounting, quantity: float):
        """Сообщить, какая позиция нужна стратегии по инструменту.

        OrderProcessor сам решает, какие заявки нужно выставить, чтобы
        привести текущую позицию в accounting к целевой.

        Args:
            accounting: учёт инструмента, по которому нужна позиция.
                Должен быть зарегистрирован в accountingController.
            quantity: целевая позиция со знаком: > 0 длинная, < 0 короткая, 0 закрыть.

        Raises:
            ValueError: если accounting не зарегистрирован в accountingController.
        """
        # Если такого accounting ещё нет в списке accountings, то бросаем ошибку!
        if accounting not in self.accountingController.accountings:
            raise ValueError("Accounting not found in the list of accountings!")
        self.send_order(accounting, quantity - accounting.position)

    def send_order(self, accounting: Accounting, quantity: float):
        """Выставить заявку на quantity (знак задаёт направление). Реализуется в наследниках."""
        raise NotImplementedError("Subclasses should implement this!")


class SimOrderProcessor(OrderProcessor):
    """Симулятор: заявка исполняется сразу по текущей цене из DataFeeder."""

    def __init__(self, accountingController: AccountingController, datafeeder: DataFeeder):
        super().__init__(accountingController)
        self.datafeeder = datafeeder

    def send_order(self, accounting: Accounting, quantity: float):
        if quantity == 0:
            return
        price = self.datafeeder.get_price(accounting.instrument_info)
        accounting.on_deal('Buy' if quantity > 0 else 'Sell', abs(quantity), price)
