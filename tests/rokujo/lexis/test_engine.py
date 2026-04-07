from rokujo.lexis.base import AnalysisStrategy


class MockStrategy(AnalysisStrategy):
    def execute(self, doc):
        return "success"


def test_engine_initialization(engine):
    assert engine.nlp is not None


def test_engine_run_calls_strategy(engine):
    strategy = MockStrategy()
    result = engine.run("Hello world", strategy)
    assert result == "success"
