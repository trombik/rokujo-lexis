from ..base import AnalysisStrategy


class ChunkCounter(AnalysisStrategy):
    """
    Counts noun chunks.

    """

    def execute(self, doc) -> list[list]:
        if doc is None:
            raise ValueError

        chunks = []
        for chunk in doc.noun_chunks:
            if chunk.root.pos_ == "PRON":
                continue
            words = [t.lemma_.lower() for t in chunk if t.pos_ != "DET"]
            chunks.append(" ".join(words))

        return self._to_freq_list(chunks)


class CompoundCounter(AnalysisStrategy):
    """
    Counts compound nouns
    """

    def execute(self, doc) -> list[list]:
        if doc is None:
            raise ValueError

        compounds = []
        current_compound = []

        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"]:
                value = token.text if token.pos_ == "PROPN" else token.lemma_
                current_compound.append(value)
            else:
                if len(current_compound) > 1:
                    compounds.append(" ".join(current_compound))
                current_compound = []
        if len(current_compound) > 1:
            compounds.append(" ".join(current_compound))

        return self._to_freq_list(compounds)


class ProperNounCounter(AnalysisStrategy):
    """
    Counts proper nouns.
    """

    def execute(self, doc) -> list[list]:
        if doc is None:
            raise ValueError

        ignored_labels = [
            "CARDINAL",
            "DATE",
            "LANGUAGE",
            "MONEY",
            "ORDINAL",
            "PERCENT",
            "QUANTITY",
            "TIME",
        ]
        proper_nouns = []
        for ent in doc.ents:
            if ent.label_ not in ignored_labels:
                proper_nouns.append(ent.text)
                print(f"{ent.text}: {ent.label_}")
        return self._to_freq_list(proper_nouns)
