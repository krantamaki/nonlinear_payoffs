from abc import ABC, abstractmethod
from typing import Optional
from copy import copy
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
from option import CallOption, PutOption, Option


class Strategy(ABC):
    """
    Abstract base class for option positions
    """

    @abstractmethod
    def __call__(self, underlying_value: float) -> float:
        pass

    @abstractmethod
    def options(self):
        pass

    def plot(self, range: (float, float), n_points: int = 1000, fig: Optional[plt.Figure] = None,
             save_as: Optional[str] = None, fmt: str = '-', alpha: float = 1,
             linewidth: float = 1, label: str = '') -> None:

        xx = np.linspace(range[0], range[1], n_points)
        yy = np.array([self(x) for x in xx])

        if fig is None:
            fig = plt.figure(figsize=(12, 6))

        plt.plot(xx, yy, fmt, alpha=alpha, linewidth=linewidth, label=label)

        if save_as is not None:
            fig.savefig(save_as)


class Butterfly(Strategy):
    """
    The butterfly option trading strategy consisting of four options (either all
    calls or all puts, this implementation uses calls) on the same underlying and
    with the same expiry date, but differing strikes. The options with outer strikes
    are bought and inner strikes sold. The strikes of the inner options are equal.
    """

    def __init__(self, inner_strike: float, spread: float,
                 position_size: float) -> None:

        self.__inner = inner_strike
        self.__spread = spread
        self.__pos_size = position_size

        self.__options = [CallOption(self.__inner - self.__spread, "long", self.__pos_size),
                          CallOption(self.__inner, "short", self.__pos_size),
                          CallOption(self.__inner, "short", self.__pos_size),
                          CallOption(self.__inner + self.__spread, "long", self.__pos_size)]

    def __call__(self, underlying_value: float) -> float:
        return sum([option(underlying_value) for option in self.__options])

    def options(self) -> list[Option]:
        return copy(self.__options)


class Condor(Strategy):
    """
    The condor option trading strategy consisting of four options (either all
    calls or all puts, this implementation uses calls) on the same underlying and
    with the same expiry date, but differing strikes. The options with outer strikes
    are bought and inner strikes sold. The difference between the two lowest strikes
    must be the same as the  difference between the two highest strikes.
    """

    def __init__(self, lower_strike: float, diff: float, upper_strike: float,
                 position_size: float) -> None:

        self.__lower = lower_strike
        self.__diff = diff
        self.__upper = upper_strike
        self.__pos_size = position_size

        self.__options = [CallOption(self.__lower, "long", self.__pos_size),
                          CallOption(self.__lower + self.__diff, "short", self.__pos_size),
                          CallOption(self.__upper - self.__diff, "short", self.__pos_size),
                          CallOption(self.__upper, "long", self.__pos_size)]

    def __call__(self, underlying_value: float) -> float:
        return sum([option(underlying_value) for option in self.__options])

    def options(self) -> list[Option]:
        return copy(self.__options)


class CondorChain(Strategy):

    def __init__(self, _lambda: float, _phi: float, _delta: float,
                 position_size: float, eval_range: (float, float)) -> None:

        inner_diff = _lambda / 2 - _delta
        shift = inner_diff / 2 + _delta

        i_range = [-i for i in range(1, ceil((_phi - eval_range[0]) / _lambda) + 1)] + \
                  [i for i in range(ceil((eval_range[1] - _phi) / _lambda) + 1)]

        self.condors = [Condor(_phi - shift + i * _lambda, _delta, _phi + shift + i * _lambda, position_size) for i in i_range]

    def __call__(self, underlying_value: float) -> float:
        return sum([condor(underlying_value) for condor in self.condors])

    def options(self):
        return sum([condor.options() for condor in self.condors], [])


class StrategyCollection(Strategy):

    def __init__(self, strategies: list[Strategy], magnitude: float = 1.0) -> None:

        self.__strategies = strategies
        self.__magnitude = magnitude

    def __call__(self, underlying_value: float) -> float:
        return self.__magnitude * sum([strategy(underlying_value) for strategy in self.__strategies])

    def options(self):
        return sum([strategy.options() for strategy in self.__strategies], [])

    def plot_strategies(self, range: (float, float), n_points: int = 1000, fig: Optional[plt.Figure] = None,
                        save_as: Optional[str] = None, fmt: str = '-', alpha: float = 1, linewidth: float = 1) -> None:

        for strategy in self.__strategies:
            strategy.plot(range, n_points=n_points, fig=fig, save_as=save_as, fmt=fmt, alpha=alpha, linewidth=linewidth)


class SineApproximation(Strategy):

    def __init__(self, _lambda: float, _phi: float, n: int, eval_range: (float, float), magnitude: float = 1) -> None:

        condor_chains = []
        mag_sum = 0
        magnitude = magnitude

        for i in range(1, n + 1):
            diff = (i * _lambda) / (2 * n)
            mag = np.sin(np.pi / 2 * i / n) * i / n
            mag_sum += mag
            condor_chains.append(CondorChain(_lambda, _phi, diff, (1 / diff) * mag, eval_range))

        self.__strategy = StrategyCollection(condor_chains, magnitude / mag_sum)

    def __call__(self, underlying_value: float) -> float:
        return self.__strategy(underlying_value)

    def options(self):
        return self.__strategy.options()

    def plot_condors(self, range: (float, float), n_points: int = 1000, fig: Optional[plt.Figure] = None,
                     save_as: Optional[str] = None, fmt: str = '-', alpha: float = 1, linewidth: float = 1) -> None:

        self.__strategy.plot_strategies(range, n_points=n_points, fig=fig, save_as=save_as, fmt=fmt, alpha=alpha, linewidth=linewidth)
