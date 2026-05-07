import re
from dateutil import parser
from datetime import datetime

from typing import Callable, List
from spacy.tokens import Doc
from ..base import AnalysisStrategy


class NumeralExtractor(AnalysisStrategy):
    """
    Extract a list of numeral word chunks from a Doc.

    The chunks include not only numerals but also associated contexts that are
    useful for human verification (e.g., "one person", "1.5 MB",
    "roughly 4.2 million koku of rice").
    """

    def __init__(self):
        # extra rules capture numerals and expands phrases with useful
        # contexts.
        self.expansion_rules: List[Callable[[Doc, int], int]] = [
            self._rule_direct_noun,
            self._rule_preposition_phrase,
        ]

    def execute(self, doc: Doc) -> List[List]:
        results = []
        processed_indices = set()

        # these labels are simpler than other patterns. doc.ents (almost)
        # correctly captures what we want.
        simple_labels = {
            "DATE",
            "TIME",
            "MONEY",
            "PERCENT",
            "ORDINAL",
            "QUANTITY"
        }

        for ent in doc.ents:
            if ent.label_ in simple_labels:
                # doc.ents does not necessarily includes useful contexts for
                # humans. expand the captured result with extra rules.
                extended_end = self._find_span_end(doc, ent.end - 1)
                full_span = doc[ent.start: extended_end]

                results.append([full_span.text, "", ent.label_])
                for token in full_span:
                    processed_indices.add(token.i)

        # capture numerals with extra rules.
        i = 0
        while i < len(doc):
            token = doc[i]
            if i in processed_indices or not (token.like_num or token.pos_ == "NUM"): # noqa E510
                i += 1
                continue

            # apply the extra rules
            span_end = self._find_span_end(doc, i)
            span = doc[i:span_end]
            results.append([span.text, "", ""])

            for t in span:
                processed_indices.add(t.i)
            i = span_end

        for index, result in enumerate(results):
            if result[1] == "" and result[2] == "DATE":
                results[index][1] = self._en_date_to_ja_date(result[0])

        results.sort()
        return results

    def _find_span_end(self, doc: Doc, start_index: int) -> int:
        """
        Recursively expand the span from a numeric starting point.

        This method applies a set of expansion rules iteratively until the span
        no longer grows. This allows capturing complex phrases such as
        "4.2 million koku of rice" by chaining simple rules.

        Examples:
        * Start with "4.2" -> find "million" -> find "koku" -> find "of rice".
        """
        current_end = start_index + 1

        while True:
            changed = False
            for rule in self.expansion_rules:
                new_end = rule(doc, current_end)
                if new_end > current_end:
                    current_end = new_end
                    changed = True
            if not changed:
                break

        return current_end

    def _rule_direct_noun(self, doc: Doc, current_end: int) -> int:
        """
        Capture a noun that is directly modified by the preceding numeral,
        such as "NUM + noun".

        Examples:

        * 123 domains
        * one hundred people
        """
        if current_end < len(doc) and doc[current_end].pos_ in {"NOUN", "PROPN"}: # noqa E501
            return current_end + 1
        return current_end

    def _rule_preposition_phrase(self, doc: Doc, current_end: int) -> int:
        """
        Capture "NUM + of + noun phrase".

        Examples:
        * One of the students
        * 4.2 million koku of rice
        """
        if current_end < len(doc) and doc[current_end].lower_ == "of":
            idx = current_end + 1
            while idx < len(doc) and doc[idx].pos_ in {"DET", "ADJ"}:
                idx += 1
            if idx < len(doc) and doc[idx].pos_ in {"NOUN", "PROPN"}:
                return idx + 1
        return current_end

    def _en_year_to_ja_year_with_one_word(self, text: str) -> str:
        if len(text.split()) != 1:
            return ""

        if re.search(r"^\d{1,}$", text):
            return f"{text}年"

        match = re.search(r"^(\d{3,4})'s$", text)
        if match:
            return f"{match.group(1)}年代"

        sentinel_year = 9999
        default_dt = datetime(sentinel_year, 1, 1)

        try:
            dt = parser.parse(text, default=default_dt)
            if dt.year == sentinel_year:
                return f"{dt.month}月"
        except (parser.ParserError, OverflowError):
            pass
        return ""

    def _en_year_to_ja_year_with_two_words(self, text: str) -> str:
        if len(text.split()) != 2:
            return ""

        match = re.search(r"^[Tt]he\s+(\d{3,4})s$", text)
        if match:
            return f"{match.group(1)}年代"

        sentinel_year = 9999
        default_dt = datetime(sentinel_year, 1, 1)

        try:
            dt = parser.parse(text, default=default_dt)
            if dt.year == sentinel_year:
                return f"{dt.month}月{dt.day}日"
            else:
                return f"{dt.year}年{dt.month}月"
        except (parser.ParserError, OverflowError):
            return ""

    def _en_date_to_ja_date(self, text: str) -> str:
        """
        """

        print(text.split())
        if len(text.split()) == 1:
            return self._en_year_to_ja_year_with_one_word(text)

        if len(text.split()) == 2:
            return self._en_year_to_ja_year_with_two_words(text)

        sentinel_year = 9999
        default_dt = datetime(sentinel_year, 1, 1)

        try:
            dt = parser.parse(text, default=default_dt)
            if dt.year == sentinel_year:
                return f"{dt.month}月{dt.day}日"
            else:
                return f"{dt.year}年{dt.month}月{dt.day}日"
        except (parser.ParserError, OverflowError):
            return ""
