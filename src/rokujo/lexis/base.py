from abc import ABC, abstractmethod
from collections import Counter
from typing import Any


class AnalysisStrategy(ABC):
    """
    The base class for the analysis strategies.
    """
    @abstractmethod
    def execute(self, doc: Any) -> list:
        pass

    def _to_freq_list(self, items: list[str]) -> list[list]:
        return [list(item) for item in Counter(items).most_common()]
