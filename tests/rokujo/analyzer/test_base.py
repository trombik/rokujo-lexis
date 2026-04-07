import pytest
from rokujo.analyzer.base import AnalysisStrategy


def test_abstract_base_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AnalysisStrategy()


def test_subclass_must_implement_execute():
    class IncompleteStrategy(AnalysisStrategy):
        pass

    with pytest.raises(TypeError):
        IncompleteStrategy()
