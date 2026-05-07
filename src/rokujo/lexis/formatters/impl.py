import csv
import io
from .base import OutputFormatter
from typing import Any


class CSVFormatter(OutputFormatter):
    def format(self, data: list, line_ending: str) -> str:
        output = io.StringIO(newline="")
        writer = csv.writer(output, lineterminator=line_ending)
        writer.writerow(["Term", "Count"])

        for item in data:
            if isinstance(item, list):
                writer.writerow(item)
            else:
                writer.writerow([item])
        return output.getvalue()

    def extension(self) -> str:
        return "csv"


class TSVFormatter(OutputFormatter):
    def format(self, data: list, line_ending: str) -> str:
        output = io.StringIO(newline="")
        writer = csv.writer(output, delimiter="\t", lineterminator=line_ending)
        writer.writerow(["Term", "Count"])

        for item in data:
            if isinstance(item, list):
                writer.writerow(item)
            else:
                writer.writerow([item])
        return output.getvalue()

    def extension(self) -> str:
        return "tsv"


class ExcelFormatter(OutputFormatter):
    def format(self, data: list) -> Any:
        import pandas as pd

        if data and isinstance(data[0], list):
            df = pd.DataFrame(data, columns=["Term", "Count"])
        else:
            df = pd.DataFrame(data, columns=["Term"])
        return df

    def extension(self) -> str:
        return "xlsx"
