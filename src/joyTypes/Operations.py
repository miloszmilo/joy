from abc import ABC, abstractmethod
from typing import override


class Operation(ABC):
    @abstractmethod
    def execute(self, *args: float) -> float:
        pass


class AddOperation(Operation):
    @override
    def execute(self, left: float, right: float) -> float:
        return float(left + right)


class SubtractOperation(Operation):
    @override
    def execute(self, left: float, right: float) -> float:
        return float(left - right)


class MultiplyOperation(Operation):
    @override
    def execute(self, left: float, right: float) -> float:
        return float(left * right)


class DivideOperation(Operation):
    @override
    def execute(self, left: float, right: float) -> float:
        return float(left / right)
