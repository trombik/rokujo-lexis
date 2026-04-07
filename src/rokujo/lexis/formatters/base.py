from abc import ABC, abstractmethod
from typing import Any
from collections import Counter


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, data: Counter) -> Any:
        """
        Perform formatting.
        """
        pass

    @abstractmethod
    def extension(self) -> str:
        """
        Returns the fie extension string.
        """
        pass
