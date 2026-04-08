from typing import List
from spacy.tokens import Doc
from ..base import AnalysisStrategy


class NumeralExtractor(AnalysisStrategy):
    """
    Extarct a list of numeral word chunks.
    """

    def execute(self, doc: Doc) -> List[str]:
        results = []

        # Simple cases.
        simple_labels = {
            "DATE",
            "TIME",
            "MONEY",
            "PERCENT",
            "ORDINAL",
            "QUANTITY",
        }
        processed_tokens = set()
        for ent in doc.ents:
            if ent.label_ in simple_labels:
                results.append(ent.text)
                for token in ent:
                    processed_tokens.add(token.i)

        # other complicated ones. join the qualified noun or propn.
        for token in doc:
            if token.i in processed_tokens:
                continue

            if token.like_num or token.pos_ == "NUM":
                span_end = token.i + 1
                if span_end < len(doc):
                    next_token = doc[span_end]
                    if next_token.pos_ in {"NOUN", "PROPN"}:
                        span_end += 1

                span = doc[token.i: span_end]
                results.append(span.text)
                for t in span:
                    processed_tokens.add(t.i)

        return results
