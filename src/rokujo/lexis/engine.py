import spacy
from .base import AnalysisStrategy


class AnalyzerEngine:
    """
    the engine to run strategies and the result.
    """
    def __init__(self, model: str = "en_core_web_md"):
        self.nlp = spacy.load(model)

    def run(self, text: str, strategy: AnalysisStrategy):
        doc = self.nlp(text)
        return strategy.execute(doc)
