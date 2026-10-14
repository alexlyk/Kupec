from accounting import AccountingController
from datafeeder import DataFeeder

class PerformanceReporter:
    """Рассчитывает результаты торговли и показатели эффективности.

    Берёт сделки и позиции из Accounting, рыночные данные для оценки
    портфеля — из DataFeeder.
    """

    def __init__(self, datafeeder: DataFeeder, accountingController: AccountingController):
        """
        Args:
            datafeeder: источник рыночных данных для оценки портфеля.
            accountingController: реестр Accounting, по которым строится отчёт.
        """
        self.datafeeder = datafeeder
        self.accountingController = accountingController

    def on_dayend(self):
        """В конце дня сохраняет состояние accountings."""
        raise NotImplementedError("Subclasses should implement this!")
