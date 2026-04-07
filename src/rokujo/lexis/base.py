from abc import ABC, abstractmethod
from typing import Any


class AnalysisStrategy(ABC):
    """
    The base class for the analysis strategies.
    """
    @abstractmethod
    def execute(self, doc: Any) -> Any:
        pass
