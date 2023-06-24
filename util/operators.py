__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from typing import Any, TypeVar, NoReturn

OperatorsType = TypeVar('OperatorsType', bound='Operators')


class Operators:
    def __init__(self, value: Any):
        Operators.__validate(value)
        self.value = value

    def __add__(self, other: OperatorsType) -> OperatorsType:
        return Operators(self.value + other.value)

    def __mul__(self, other: OperatorsType) -> OperatorsType:
        return Operators(self.value * other.value)

    def __str__(self):
        return str(self.value)

    @staticmethod
    def __validate(value: Any) -> NoReturn:
        if value.__class__.__name__ not in ["AnyStr", "str", "int", "long", "float"]:
            raise TypeError(f'type {value.__class__.__name__} is not supported')


if __name__ == '__main__':
    x = Operators(3.45)
    y = Operators(3.1)
    print(x*y)
