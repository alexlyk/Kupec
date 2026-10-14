from instrument_info import InstrumentInfo

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

    def on_deal(self):
        """Обработать исполненную сделку (из симулятора или от брокера/биржи)
        и обновить позицию и деньги. Не реализовано.
        """
        raise NotImplementedError("Not implemented!")


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
