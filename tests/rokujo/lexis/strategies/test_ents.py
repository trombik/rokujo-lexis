import pytest
from rokujo.lexis.strategies.ents import (
    NumeralExtractor
)


class TestNumeralExtractor:
    def setup_method(self):
        self.strategy = NumeralExtractor()

    def assert_extracted_text(self, expected_text: str, results: list[list]):
        extracted_texts = [item[0] for item in results]
        assert expected_text in extracted_texts, (
            f"'{expected_text}' was not found in extracted results.\n"
            f"Extracted: {extracted_texts}"
        )

    def test_extract_one_item(self, engine):
        doc = engine.nlp("I just need one item.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("one item", result)

    def test_extract_plural(self, engine):
        doc = engine.nlp("I just need two items.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("two items", result)

    def test_extract_tems_with_numeric(self, engine):
        doc = engine.nlp("I just need 2 items.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("2 items", result)

    def test_extract_price(self, engine):
        doc = engine.nlp("It costs 1 million yen.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("1 million yen", result)

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extract_price_with_prefix(self, engine):
        doc = engine.nlp("It costs JPY 1 million.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("JPY 1 million", result)

    def test_extract_number_with_period(self, engine):
        doc = engine.nlp("It costs 1.1 million yen.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("1.1 million yen", result)

    def test_extract_english_numbers(self, engine):
        doc = engine.nlp("It costs one thousand yen.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("one thousand yen", result)

    def test_extract_decimal_numbers_with_units(self, engine):
        doc = engine.nlp("It takes 1.5 hours.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("1.5 hours", result)

    def test_extract_bytes(self, engine):
        doc = engine.nlp("It is 1.5 MB.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("1.5 MB", result)

    def test_extract_numbers_with_commmas(self, engine):
        doc = engine.nlp("It took 1,000,000 years.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("1,000,000 years", result)

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extract_spelled_out_numbers_with_and(self, engine):
        doc = engine.nlp("It took one hundred and fifteen minutes.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("one hundred and fifteen minutes", result)

    def test_positive_percents(self, engine):
        doc = engine.nlp("The sales are good, 10% and 12.5%, for each.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("10%", result)
        self.assert_extracted_text("12.5%", result)

    def test_negative_percents(self, engine):
        doc = engine.nlp("The sales are bad, -10% and -12.5%, for each.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("-10%", result)
        self.assert_extracted_text("-12.5%", result)

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extarct_cardinal_items(self, engine):
        doc = engine.nlp("He is the first person to go. She is the second.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("the first person", result)
        self.assert_extracted_text("the second", result)

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_extarct_cardinal_items_with_or_without_dash(self, engine):
        doc = engine.nlp("He is the twenty-first person to go. She is the twenty second.") # noqa E501
        result = self.strategy.execute(doc)

        self.assert_extracted_text("the twenty-first person", result)
        self.assert_extracted_text("the twenty second", result)

    def test_extract_dates(self, engine):
        doc = engine.nlp("In Jan. 1, 2026, she was born.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("Jan. 1", result)

    def test_extract_dates_with_cardinal(self, engine):
        doc = engine.nlp("In Jan. 1st, 2026, she was born.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("Jan. 1st", result)

    def test_extract_four_point_two_million_of(self, engine):
        doc = engine.nlp("The shogun controlled land producing roughly 4.2 million koku of rice. One of the students left early.") # noqa E501
        result = self.strategy.execute(doc)

        self.assert_extracted_text("roughly 4.2 million koku of rice", result)
        self.assert_extracted_text("One of the students", result)

    @pytest.mark.xfail(reason="Need to implement complex merging logic")
    def test_verify_numeral_qualify_noun_with_nmod(self, engine):
        doc = engine.nlp("From 1843 reports started to circulate.")
        result = self.strategy.execute(doc)

        self.assert_extracted_text("1843", result)
