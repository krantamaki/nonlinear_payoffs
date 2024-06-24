from __future__ import annotations
from abc import ABC, abstractmethod


class Option(ABC):
    """
    TODO: Documentation
    """

    @abstractmethod
    def __call__(self, underlying_value: float) -> float:
        pass


class PutOption(Option):
    """
    TODO: Documentation
    """
    pass


class CallOption(Option):
    """
    TODO: Documentation
    """

    def __init__(self, strike: float, position: str, position_size: float) -> None:
        """
        TODO: Documentation
        :param strike:
        :param position:
        :param position_size:
        """
        self.__strike = strike
        self.__position = position
        self.__position_size = position_size

    def __call__(self, underlying_value: float) -> float:
        """
        TODO: Documentation
        :param underlying_value:
        :return:
        """
        if self.__strike >= underlying_value:
            return 0.0

        mult = 1.0 if self.__position == "long" else -1.0
        return mult * self.__position_size * (underlying_value - self.__strike)



