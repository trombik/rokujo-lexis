from abc import ABC, abstractmethod
from typing import Any
from collections import Counter


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, data: list, line_ending: str = "\r\n") -> Any:
        """
        Perform formatting.

        Args:
            data: Data to format
            line_ending: Line ending style ('\r\n' for CRLF, '\n' for LF)
        """
        pass

    @abstractmethod
    def extension(self) -> str:
        """
        Returns the fie extension string.
        """
        pass
