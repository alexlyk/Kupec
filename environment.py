from accounting import AccountingController
from timer import Timer
from datafeeder import HistoricalDataFeeder
from orderprocessor import OrderProcessor
from performance_reporter import PerformanceReporter
from strategies.generic import StrategyBase

class Environment:
    """Окружение бэктеста: все объекты системы и цикл прогона по timeline из datafeeder.

    В бэктесте именно Environment двигает таймер.
    """

    def __init__(self, timer: Timer, datafeeder: HistoricalDataFeeder, accountingController: AccountingController,
                 orderProcessor: OrderProcessor, strategy: StrategyBase, reporter: PerformanceReporter):
        self.timer = timer
        self.datafeeder = datafeeder
        self.accountingController = accountingController
        self.orderProcessor = orderProcessor
        self.strategy = strategy
        self.reporter = reporter

    def run(self) -> dict:
        """Прогнать стратегию по всем моментам timeline и вернуть метрики. Запускается один раз."""
        if self.reporter.history:
            raise RuntimeError('Бэктест уже прогнан. Пересоберите окружение перед повторным запуском.')
        for t in self.datafeeder.timeline:
            self.timer._time = t
            self.strategy.on_execute()
            self.reporter.on_dayend()
        return self.reporter.report()
