import csv
import io
from collections import Counter
from .base import OutputFormatter
from typing import Any


class CSVFormatter(OutputFormatter):
    def format(self, data: Counter) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Term", "Count"])
        for term, count in data.most_common():
            writer.writerow([term, count])
        return output.getvalue()

    def extension(self) -> str:
        return "csv"


class TSVFormatter(OutputFormatter):
    def format(self, data: Counter) -> str:
        output = io.StringIO()
        writer = csv.writer(output, delimiter="\t")
        writer.writerow(["Term", "Count"])
        for term, count in data.most_common():
            writer.writerow([term, count])
        return output.getvalue()

    def extension(self) -> str:
        return "tsv"


class ExcelFormatter(OutputFormatter):
    def format(self, data: Counter) -> Any:
        import pandas as pd
        df = pd.DataFrame(data.most_common(), columns=["Term", "Count"])
        return df

    def extension(self) -> str:
        return "xlsx"
