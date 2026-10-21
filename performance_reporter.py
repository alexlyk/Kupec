import numpy as np
import pandas as pd
from accounting import AccountingController
from datafeeder import DataFeeder
from strategies.generic import CapitalHandler

class PerformanceReporter:
    """Рассчитывает результаты торговли и показатели эффективности.

    Берёт сделки и позиции из Accounting, рыночные данные для оценки
    портфеля - из DataFeeder.
    """

    def __init__(self, datafeeder: DataFeeder, accountingController: AccountingController, capitalHandler: CapitalHandler):
        """
        Args:
            datafeeder: источник рыночных данных для оценки портфеля.
            accountingController: реестр Accounting, по которым строится отчёт.
            capitalHandler: реестр капитала стратегий (для метрик относительно капитала).
        """
        self.datafeeder = datafeeder
        self.accountingController = accountingController
        self.capitalHandler = capitalHandler
        self.history: list[tuple] = []  # (время, PL, оборот) нарастающим итогом

    def on_dayend(self):
        """В конце дня сохраняет состояние accountings: PL и оборот нарастающим итогом."""
        accs = self.accountingController.accountings
        pl = sum(a.value(self.datafeeder.get_price(a.instrument_info)) for a in accs)
        turnover = sum(a.turnover for a in accs)
        self.history.append((self.datafeeder.now(), pl, turnover))

    def report(self) -> dict:
        """Метрики по сохранённой истории. Безрисковая ставка = 0."""
        h = pd.DataFrame(self.history, columns=['time', 'pl', 'turnover']).set_index('time')
        pl, turnover = h.pl.iloc[-1], h.turnover.iloc[-1]
        drawdown = (h.pl.cummax() - h.pl).max()
        years = (h.index[-1] - h.index[0]).days / 365.25
        daily = h.pl.diff().dropna()
        owners = {a.owner for a in self.accountingController.accountings}
        capital = sum(self.capitalHandler.get_current_capital(o) for o in owners)
        return {
            'Капитал, руб.': capital,
            'PL, руб.': pl,
            'Доходность, %': pl / capital * 100,
            'Годовая доходность, %': pl / years / capital * 100,
            'Макс. просадка, %': drawdown / capital * 100,
            'Оборот, руб.': turnover,
            'PL / Оборот': pl / turnover if turnover else np.nan,
            'Кальмар': pl / years / drawdown if drawdown else np.nan,
            'Шарп': daily.mean() / daily.std() * np.sqrt(len(daily) / years) if daily.std() else np.nan,
        }
