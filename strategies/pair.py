import numpy as np
from accounting import Accounting
from datafeeder import DataFeeder
from typing import Callable
from strategies.generic import StrategyBase

class StrategyPair(StrategyBase):
    """Парная стратегия: спред = log(P1 / P2).

    Сигнал -1 (short leg1, long leg2), если спред > mean + k*sigma;
    +1 (long leg1, short leg2), если спред < mean - k*sigma; иначе 0 (позиции закрываются).
    mean и sigma считаются по предыдущим window значениям спреда.
    Капитал стратегии равен гросс-позиции: по половине на каждую ногу.
    """

    def __init__(self, id: str, datafeeder: DataFeeder, do_need_position: Callable[[Accounting, float], None],
                 get_capital: Callable[[str], float], leg1: Accounting, leg2: Accounting, window: int = 60, k: float = 3):
        super().__init__(id, datafeeder, do_need_position, get_capital)
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
        notional = self.get_capital(self.id) / 2  # капитал = гросс, делится между ногами
        self.do_need_position(self.leg1, signal * int(notional / p1))
        self.do_need_position(self.leg2, -signal * int(notional / p2))
