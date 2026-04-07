import pytest
from rokujo.lexis.engine import AnalyzerEngine


@pytest.fixture(scope="module")
def engine():
    return AnalyzerEngine()
