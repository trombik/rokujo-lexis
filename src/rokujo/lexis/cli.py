import sys

import typer
from pathlib import Path
from enum import Enum
from typing import Optional

from rokujo.lexis.engine import AnalyzerEngine
from rokujo.lexis.strategies.noun import (
    CompoundCounter,
    ChunkCounter,
)
from rokujo.lexis.formatters.impl import (
    CSVFormatter,
    TSVFormatter,
    ExcelFormatter,
)


class StrategyType(str, Enum):
    noun = "noun"
    compound = "compound"


class FormatType(str, Enum):
    csv = "csv"
    tsv = "tsv"
    xlsx = "xlsx"
    terminal = "terminal"


app = typer.Typer()


@app.command()
def analyze(
    file_path: Path = typer.Argument(..., help="Path to the text file to analyze"), # noqa E501
    format_type: FormatType = typer.Option(FormatType.terminal,
                                           "--format", "-f"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    strategy_name: StrategyType = typer.Option(
        StrategyType.noun, "--strategy", "-s", help="Analysis strategy to use"
    ),
    model: str = typer.Option("en_core_web_md",
                              "--model", "-m", help="spaCy model name")
):
    """
    Analyze a text file using a specific strategy.
    """
    if not file_path.exists():
        typer.secho(f"Error: File not found: {file_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if format_type == FormatType.xlsx and str(output) == "-":
        typer.secho("Error: Excel format does not support output to stdout.",
                    fg=typer.colors.RED,
                    err=True)
        raise typer.Exit(1)

    engine = AnalyzerEngine(model=model)

    strategy_map = {
        StrategyType.noun: ChunkCounter(),
        StrategyType.compound: CompoundCounter(),
    }
    strategy = strategy_map[strategy_name]

    text = file_path.read_text(encoding="utf-8")
    result = engine.run(text, strategy)

    formatters = {
        FormatType.csv: CSVFormatter(),
        FormatType.tsv: TSVFormatter(),
        FormatType.xlsx: ExcelFormatter(),
    }

    if format_type == FormatType.terminal:
        for word, count in result.most_common(20):
            print(f"{count: >4}: {word}")
            return

    formatter = formatters[format_type]
    formatted_data = formatter.format(result)
    if str(output) == "-":
        sys.stdout.write(formatted_data)

    else:
        if output:
            out_path = Path(output)
        else:
            out_path = file_path.with_suffix(f".{formatter.extension()}")
        out_path.write_text(formatted_data, encoding="utf-8")
        typer.secho(f"Saved to: {out_path}", fg=typer.colors.GREEN, err=True)


if __name__ == "__main__":
    app()
