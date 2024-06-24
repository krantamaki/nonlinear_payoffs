from abc import ABC, abstractmethod
from typing import Optional
from copy import copy
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
             save_as: Optional[str] = None, format: str = '-', alpha: float = 1,
             linewidth: float = 1, label: str = '') -> None:
        """
        TODO: Documentation
        :param range:
        :param n_points:
        :param fig:
        :param save_as:
        :param format:
        :param alpha:
        :param linewidth:
        :param label:
        :return:
        """
        xx = np.linspace(range[0], range[1], n_points)
        yy = np.array([self(x) for x in xx])

        if fig is None:
            fig = plt.figure(figsize=(12, 6))

        # TODO: Process other kwargs

        plt.plot(xx, yy, format, alpha=alpha)

        if save_as is not None:
            fig.savefig(save_as)


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
        """
        TODO: Documentation
        :param lower_strike:
        :param diff:
        :param upper_strike:
        :param position_size:
        """
        self.__lower = lower_strike
        self.__diff = diff
        self.__upper = upper_strike
        self.__pos_size = position_size

        self.__options = [CallOption(self.__lower, "long", self.__pos_size),
                          CallOption(self.__lower + self.__diff, "short", self.__pos_size),
                          CallOption(self.__upper - self.__diff, "short", self.__pos_size),
                          CallOption(self.__upper, "long", self.__pos_size)]

    def __call__(self, underlying_value: float) -> float:
        """
        TODO: Documentation
        :param underlying_value:
        :return:
        """
        return sum([option(underlying_value) for option in self.__options])

    def options(self) -> list[Option]:
        """
        TODO: Documentation
        :return:
        """
        return copy(self.__options)


class CondorChain(Strategy):
    """
    TODO: Documentation
    """

    def __init__(self, inner_diff: float, side_diff: float, anchor_strike: float,
                 position_size: float, eval_range: (float, float)) -> None:
        """
        TODO: Documentation
        :param inner_diff:
        :param side_diff:
        :param anchor_strike:
        :param position_size:
        :param eval_range:
        """
        self.__inner_diff = inner_diff
        self.__side_diff = side_diff
        self.__anchor_strike = anchor_strike
        self.__position_size = position_size
        self.__eval_range = eval_range

        self.condors = [Condor(anchor_strike - inner_diff / 2 - side_diff, side_diff,
                               anchor_strike + inner_diff / 2 + side_diff, position_size)]

        outer_bound = anchor_strike + inner_diff / 2 + side_diff + inner_diff
        while eval_range[1] > outer_bound:
            new_outer_bound = outer_bound + inner_diff + 2 * side_diff
            self.condors.append(Condor(outer_bound, side_diff, new_outer_bound, position_size))
            outer_bound = new_outer_bound + inner_diff

        outer_bound = anchor_strike - inner_diff / 2 - side_diff - inner_diff
        while eval_range[0] < outer_bound:
            new_outer_bound = outer_bound - inner_diff - 2 * side_diff
            self.condors.insert(0, Condor(new_outer_bound, side_diff, outer_bound, position_size))
            outer_bound = new_outer_bound - inner_diff

        # print(len(self.condors))

    def __call__(self, underlying_value: float) -> float:
        """
        TODO: Documentation
        :param underlying_value:
        :return:
        """
        return sum([condor(underlying_value) for condor in self.condors])

    def options(self):
        """
        TODO: Documentation
        """
        return sum([condor.options() for condor in self.condors], [])


class StrategyCollection(Strategy):
    """

    """

    def __init__(self, strategies: list[Strategy], magnitude: float = 1.0) -> None:
        """
        TODO: Documentation
        :param strategies:
        :param magnitude:
        """
        self.__strategies = strategies
        self.__magnitude = magnitude

    def __call__(self, underlying_value: float) -> float:
        return self.__magnitude * sum([strategy(underlying_value) for strategy in self.__strategies])

    def options(self):
        return sum([strategy.options() for strategy in self.__strategies], [])
