from pathlib import Path
import pandas as pd
from instrument_info import InstrumentInfo
from timer import Timer

class DataFeeder:
    """Базовый класс поставщика рыночных данных (historical / live / on-demand).

    Конкретные источники данных реализуются в наследниках.
    """

    def __init__(self, timer: Timer):
        """
        Args:
            timer: источник текущего времени, на который отдаются цены.
        """
        self.timer = timer

    def get_price(self, instrument: InstrumentInfo):
        """Вернуть текущую цену инструмента. Реализуется в наследниках.

        Args:
            instrument: инструмент, цену которого нужно получить.
        """
        raise NotImplementedError("Subclasses should implement this!")


class HistoricalDataFeeder(DataFeeder):
    """Исторические 30-минутные свечи Finam: raw/finam/candles_30m/{TICKER}/{YYYY}.csv.

    Цена на момент timer.Now(): close последней свечи, закрывшейся не позже этого момента.
    timeline: моменты "дата + at" для дней, когда торговались все инструменты.
    """

    def __init__(self, timer: Timer, root: str, instruments: list[InstrumentInfo], at: str = '18:00:00'):
        """
        Args:
            timer: источник текущего времени.
            root: папка raw с историческими данными.
            instruments: инструменты, которые нужно загрузить.
            at: время дня, на которое строится timeline.
        """
        super().__init__(timer)
        self.prices = {i.name: self._load(Path(root) / 'finam' / 'candles_30m' / i.name) for i in instruments}
        days = None
        for s in self.prices.values():
            start = s.index - pd.Timedelta('30min')
            d = set(start[s.index <= start.normalize() + pd.Timedelta(at)].normalize())
            days = d if days is None else days & d
        self.timeline = [d + pd.Timedelta(at) for d in sorted(days)]

    @staticmethod
    def _load(folder: Path) -> pd.Series:
        d = pd.concat(pd.read_csv(f, sep=';') for f in sorted(folder.glob('*.csv')))
        d.columns = [c.strip('<>') for c in d.columns]
        end = pd.to_datetime(d.DATE.astype(str) + d.TIME.astype(str).str.zfill(6), format='%Y%m%d%H%M%S') + pd.Timedelta('30min')
        s = pd.Series(d.CLOSE.values, index=end).sort_index()
        return s[~s.index.duplicated()]

    def get_price(self, instrument: InstrumentInfo) -> float:
        return float(self.prices[instrument.name].asof(self.timer.Now()))
