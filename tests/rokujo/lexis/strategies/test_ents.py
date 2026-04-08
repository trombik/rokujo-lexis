import pytest
from rokujo.lexis.strategies.ents import (
    NumeralExtractor
)


class TestNumeralExtractor:
    def setup_method(self):
        self.strategy = NumeralExtractor()

    def test_extract_one_item(self, engine):
        doc = engine.nlp("I just need one item.")
        result = self.strategy.execute(doc)

        assert "one item" in result

    def test_extract_plural(self, engine):
        doc = engine.nlp("I just need two items.")
        result = self.strategy.execute(doc)

        assert "two items" in result

    def test_extract_tems_with_numeric(self, engine):
        doc = engine.nlp("I just need 2 items.")
        result = self.strategy.execute(doc)

        assert "2 items" in result

    def test_extract_price(self, engine):
        doc = engine.nlp("It costs 1 million yen.")
        result = self.strategy.execute(doc)

        assert "1 million yen" in result

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extract_price_with_prefix(self, engine):
        doc = engine.nlp("It costs JPY 1 million.")
        result = self.strategy.execute(doc)

        assert "JPY 1 million" in result

    def test_extract_number_with_period(self, engine):
        doc = engine.nlp("It costs 1.1 million yen.")
        result = self.strategy.execute(doc)

        assert "1.1 million yen" in result

    def test_extract_english_numbers(self, engine):
        doc = engine.nlp("It costs one thousand yen.")
        result = self.strategy.execute(doc)

        assert "one thousand yen" in result

    def test_extract_decimal_numbers_with_units(self, engine):
        doc = engine.nlp("It takes 1.5 hours.")
        result = self.strategy.execute(doc)

        assert "1.5 hours" in result

    def test_extract_bytes(self, engine):
        doc = engine.nlp("It is 1.5 MB.")
        result = self.strategy.execute(doc)

        assert "1.5 MB" in result

    def test_extract_numbers_with_commmas(self, engine):
        doc = engine.nlp("It took 1,000,000 years.")
        result = self.strategy.execute(doc)

        assert "1,000,000 years" in result

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extract_spelled_out_numbers_with_and(self, engine):
        doc = engine.nlp("It took one hundred and fifteen minutes.")
        result = self.strategy.execute(doc)

        assert "one hundred and fifteen minutes" in result

    def test_positive_percents(self, engine):
        doc = engine.nlp("The sales are good, 10% and 12.5%, for each.")
        result = self.strategy.execute(doc)

        assert "10%" in result
        assert "12.5%" in result

    def test_negative_percents(self, engine):
        doc = engine.nlp("The sales are bad, -10% and -12.5%, for each.")
        result = self.strategy.execute(doc)

        assert "-10%" in result
        assert "-12.5%" in result

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extarct_cardinal_items(self, engine):
        doc = engine.nlp("He is the first person to go. She is the second.")
        result = self.strategy.execute(doc)

        assert "the first person" in result
        assert "the second" in result

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extarct_cardinal_items_with_or_without_dash(self, engine):
        doc = engine.nlp("He is the twenty-first person to go. She is the twenty second.") # noqa E501
        result = self.strategy.execute(doc)

        assert "the twenty-first person" in result
        assert "the twenty second" in result

    def test_extract_dates(self, engine):
        doc = engine.nlp("In Jan. 1, 2026, she was born.")
        result = self.strategy.execute(doc)

        assert "Jan. 1" in result

    def test_extract_dates_with_cardinal(self, engine):
        doc = engine.nlp("In Jan. 1st, 2026, she was born.")
        result = self.strategy.execute(doc)

        assert "Jan. 1st" in result
