
from accounting import Accounting
from instrument_info import InstrumentInfo
from accounting import AccountingController


class OrderProcessor:
    """Преобразует целевые позиции от стратегии в заявки и управляет их исполнением.

    Работает в двух режимах: симуляция (сделки сразу попадают в Accounting)
    и реальная торговля через брокера/биржу. Режимы реализуются в наследниках.
    """

    def __init__(self,accountingController: AccountingController):
        """
        Args:
            accountingController: реестр Accounting, с которыми разрешено работать.
        """
        self.accountingController = accountingController

    def DoNeedPosition(self, accounting:Accounting, action):
        """Сообщить, какая позиция нужна стратегии по инструменту.

        OrderProcessor сам решает, какие заявки нужно выставить, чтобы
        привести текущую позицию в accounting к целевой.

        Args:
            accounting: учёт инструмента, по которому нужна позиция.
                Должен быть зарегистрирован в accountingController.
            action: целевое направление позиции: "BUY" — длинная, "SELL" — короткая.

        Raises:
            ValueError: если accounting не зарегистрирован в accountingController.
        """
        # Если такого accounting ещё нет в списке accountings, то бросаем ошибку!
        if accounting not in self.accountingController.accountings:
            raise ValueError("Accounting not found in the list of accountings!")
        raise NotImplementedError("Subclasses should implement this!")
