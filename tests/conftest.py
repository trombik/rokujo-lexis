import pytest
from rokujo.analyzer.engine import AnalyzerEngine


@pytest.fixture(scope="module")
def engine():
    return AnalyzerEngine()
