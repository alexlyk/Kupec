import numpy as np
from accounting import Accounting
from datafeeder import DataFeeder
from orderprocessor import OrderProcessor
from strategies.generic import StrategyBase, CapitalHandler

class StrategyPair(StrategyBase):
    """Парная стратегия: спред = log(P1 / P2).

    Сигнал -1 (short leg1, long leg2), если спред > mean + k*sigma;
    +1 (long leg1, short leg2), если спред < mean - k*sigma; иначе 0 (позиции закрываются).
    mean и sigma считаются по предыдущим window значениям спреда.
    Капитал из CapitalHandler равен гросс-позиции: по половине на каждую ногу.
    """

    def __init__(self, id: str, datafeeder: DataFeeder, orderProcessor: OrderProcessor, capitalHandler: CapitalHandler,
                 leg1: Accounting, leg2: Accounting, window: int = 60, k: float = 3):
        super().__init__(id, datafeeder, orderProcessor, capitalHandler)
        self.leg1, self.leg2, self.window, self.k = leg1, leg2, window, k
        self.spreads: list[float] = []
        self.signal = 0

    def on_execute(self):
        p1 = self.datafeeder.get_price(self.leg1.instrument_info)
        p2 = self.datafeeder.get_price(self.leg2.instrument_info)
        spread = np.log(p1 / p2)
        hist = self.spreads[-self.window:]
        self.spreads.append(spread)
        signal = 0
        if len(hist) >= self.window:
            mean, sigma = np.mean(hist), np.std(hist)
            if spread > mean + self.k * sigma:
                signal = -1
            elif spread < mean - self.k * sigma:
                signal = 1
        if signal == self.signal:
            return
        self.signal = signal
        notional = self.capitalHandler.get_current_capital(self.id) / 2  # капитал = гросс, делится между ногами
        a1, a2 = {1: ('BUY', 'SELL'), -1: ('SELL', 'BUY'), 0: ('FLAT', 'FLAT')}[signal]
        self.orderProcessor.DoNeedPosition(self.leg1, a1, int(notional / p1))
        self.orderProcessor.DoNeedPosition(self.leg2, a2, int(notional / p2))
