from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class Option(ABC):

    @abstractmethod
    def __call__(self, underlying_value: float) -> float:
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


class PutOption(Option):
    
    def __init__(self, strike: float, position: str, position_size: float, premium: float = 0) -> None:

        self.__strike = strike
        self.__position = position
        self.__position_size = position_size
        self.__premium = premium

    def __call__(self, underlying_value: float) -> float:
        mult = 1.0 if self.__position == "long" else -1.0

        if self.__strike <= underlying_value:
            return -mult * self.__premium

        return mult * (self.__position_size * (self.__strike - underlying_value) - self.__premium)


class CallOption(Option):

    def __init__(self, strike: float, position: str, position_size: float, premium: float = 0) -> None:

        self.__strike = strike
        self.__position = position
        self.__position_size = position_size
        self.__premium = premium

    def __call__(self, underlying_value: float) -> float:
        mult = 1.0 if self.__position == "long" else -1.0

        if self.__strike >= underlying_value:
            return -mult * self.__premium

        return mult * (self.__position_size * (underlying_value - self.__strike) - self.__premium)



