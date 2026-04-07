import pytest
from rokujo.analyzer.strategies.noun import (
    CompoundNounCounter,
    NounChunkCounter
)


class TestNounChunkCounter:
    def setup_method(self):
        self.strategy = NounChunkCounter()

    def test_excludes_pronoun(self, engine):
        doc = engine.nlp("It was perfect.")
        result = self.strategy.execute(doc)

        assert "it" not in result

    def test_excludes_articles(self, engine):
        doc = engine.nlp("The man went to a pub.")
        result = self.strategy.execute(doc)

        assert "man" in result
        assert "pub" in result

    def test_normalizes_to_lemma(self, engine):
        doc = engine.nlp("These codes were written by me.")
        result = self.strategy.execute(doc)

        assert "codes" not in result
        assert "code" in result

    def test_raises_value_error_with_none(self, engine):
        with pytest.raises(ValueError):
            self.strategy.execute(None)


class TestCompoundNounCounter:
    def setup_method(self):
        self.strategy = CompoundNounCounter()

    def test_compound_nouns(self, engine):
        doc = engine.nlp("I am studying natural language processing and information security.") # noqa E501
        result = self.strategy.execute(doc)

        assert "language processing" in result
        assert "information security" in result

    def test_normalizes_to_lemma(self, engine):
        doc = engine.nlp("This code has security vulnerabilities.")
        result = self.strategy.execute(doc)

        assert "security vulnerability" in result
        assert "security vulnerabilities" not in result

    def test_does_not_normalize_to_lemma_with_proper_nouns(self, engine):
        doc = engine.nlp("We don't use Google Clouds.")
        result = self.strategy.execute(doc)

        assert "Google Clouds" in result
        assert "Google Cloud" not in result

    def test_excludes_single_noun(self, engine):
        doc = engine.nlp("We don't use Google Clouds for the project.")
        result = self.strategy.execute(doc)

        assert "project" not in result
        assert "we" not in result

    def test_returns_empty_list_with_no_compounds(self, engine):
        doc = engine.nlp("This sentence has no compounds.")
        result = self.strategy.execute(doc)

        assert len(result) == 0

    def test_retusn_empty_list_with_empty_string(self, engine):
        doc = engine.nlp("")
        result = self.strategy.execute(doc)

        assert len(result) == 0

    def test_raises_value_error_with_none(self, engine):
        with pytest.raises(ValueError):
            self.strategy.execute(None)
