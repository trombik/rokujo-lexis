import pytest
from rokujo.lexis.strategies.noun import (
    CompoundCounter,
    ChunkCounter,
    ProperNounCounter,
)


class TestChunkCounter:
    def setup_method(self):
        self.strategy = ChunkCounter()

    def test_excludes_pronoun(self, engine):
        doc = engine.nlp("It was perfect.")
        result = self.strategy.execute(doc)

        assert "it" not in [item[0] for item in result]

    def test_excludes_articles(self, engine):
        doc = engine.nlp("The man went to a pub.")
        result = self.strategy.execute(doc)

        assert "man" in [item[0] for item in result]
        assert "pub" in [item[0] for item in result]

    def test_normalizes_to_lemma(self, engine):
        doc = engine.nlp("These codes were written by me.")
        result = self.strategy.execute(doc)

        assert "code" in [item[0] for item in result]
        assert "codes" not in [item[0] for item in result]

    def test_raises_value_error_with_none(self, engine):
        with pytest.raises(ValueError):
            self.strategy.execute(None)


class TestCompoundCounter:
    def setup_method(self):
        self.strategy = CompoundCounter()

    def test_compound_nouns(self, engine):
        doc = engine.nlp(
            "I am studying natural language processing and information security."
        )  # noqa E501
        result = self.strategy.execute(doc)

        assert "language processing" in [item[0] for item in result]
        assert "information security" in [item[0] for item in result]

    def test_normalizes_to_lemma(self, engine):
        doc = engine.nlp("This code has security vulnerabilities.")
        result = self.strategy.execute(doc)

        assert "security vulnerability" in [item[0] for item in result]
        assert "security vulnerabilities" not in [item[0] for item in result]

    def test_does_not_normalize_to_lemma_with_proper_nouns(self, engine):
        doc = engine.nlp("We don't use Google Clouds.")
        result = self.strategy.execute(doc)

        assert "Google Clouds" in [item[0] for item in result]
        assert "Google Cloud" not in [item[0] for item in result]

    def test_excludes_single_noun(self, engine):
        doc = engine.nlp("We don't use Google Clouds for the project.")
        result = self.strategy.execute(doc)

        assert "project" not in [item[0] for item in result]
        assert "we" not in [item[0] for item in result]

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


class TestProperNounCounter:
    def setup_method(self):
        self.strategy = ProperNounCounter()

    def test_extracts_products(self, engine):
        doc = engine.nlp("Apple is looking at buying U.K. startup for $1 billion.")
        result = self.strategy.execute(doc)

        assert "Apple" in [item[0] for item in result]
        assert "U.K." in [item[0] for item in result]
        assert "$1 billion" not in [item[0] for item in result]

    def test_ignore_quantity(self, engine):
        doc = engine.nlp("about 50km (30 miles) southeast of the city of Isfahan.")
        result = self.strategy.execute(doc)

        print(result)
        assert "about 50km" not in [item[0] for item in result]
        assert "30 miles" not in [item[0] for item in result]
