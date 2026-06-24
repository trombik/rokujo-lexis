import sys
import os

import typer
from pathlib import Path
from enum import Enum
from typing import Optional, List

from rokujo.lexis.engine import AnalyzerEngine
from rokujo.lexis.strategies.noun import (
    CompoundCounter,
    ChunkCounter,
    ProperNounCounter,
)
from rokujo.lexis.strategies.ents import (
    NumeralExtractor,
)
from rokujo.lexis.formatters.impl import (
    CSVFormatter,
    TSVFormatter,
    ExcelFormatter,
)
from rokujo.lexis.readers import ReaderFactory


class StrategyType(str, Enum):
    compound = "compound"
    noun = "noun"
    numeral = "numeral"
    proper = "proper"


class FormatType(str, Enum):
    csv = "csv"
    tsv = "tsv"
    xlsx = "xlsx"


class LineEnding(str, Enum):
    auto = "auto"
    lf = "lf"
    crlf = "crlf"


def get_os_line_ending():
    """
    Detect the appropriate line ending for the current operating system.
    Returns '\r\n' for Windows, '\n' for Unix-like systems.
    """
    return "\r\n" if os.name == "nt" else "\n"


app = typer.Typer()


@app.command()
def analyze(
    patterns: List[str] = typer.Argument(
        ..., help="Glob patterns or file paths to analyze"
    ),
    format_type: FormatType = typer.Option(FormatType.csv, "--format", "-f"),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path. Use '-' for stdout (text formats only).",
    ),
    strategy_name: StrategyType = typer.Option(
        StrategyType.noun,
        "--strategy",
        "-s",
        help=(
            "Analysis strategy to use: "
            "noun (counts noun chunks), "
            "compound (counts compound nouns), "
            "proper (counts proper nouns), "
            "numeral (extracts numeral phrases)"
        ),
    ),
    model: str = typer.Option(
        "en_core_web_md", "--model", "-m", help="spaCy model name"
    ),
    line_ending: LineEnding = typer.Option(
        LineEnding.auto,
        "--line-ending",
        help=(
            "Line ending style: "
            "crlf (CRLF, RFC 4180 compliant), "
            "lf (LF, Unix style), or auto (detect from OS)"
        ),
    ),
):
    """
    Analyze multiple files and merge results into a single output.
    """
    target_files = set()

    for pattern in patterns:
        p = Path(pattern)
        if p.is_file():
            target_files.add(p)
        else:
            for matched_file in Path(".").glob(pattern):
                if matched_file.is_file():
                    target_files.add(matched_file)

    if not target_files:
        typer.secho(
            "No files matched the provided patterns or paths.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(code=0)

    is_stdout = output is not None and str(output) == "-"

    if format_type == FormatType.xlsx and is_stdout:
        typer.secho(
            "Error: Excel format does not support output to stdout.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    engine = AnalyzerEngine(model=model)

    strategy_map = {
        StrategyType.noun: ChunkCounter(),
        StrategyType.compound: CompoundCounter(),
        StrategyType.proper: ProperNounCounter(),
        StrategyType.numeral: NumeralExtractor(),
    }
    strategy = strategy_map[strategy_name]

    formatters = {
        FormatType.csv: CSVFormatter(),
        FormatType.tsv: TSVFormatter(),
        FormatType.xlsx: ExcelFormatter(),
    }
    formatter = formatters[format_type]

    # Convert line ending enum to actual line ending string
    if line_ending == LineEnding.auto:
        line_ending_str = get_os_line_ending()
    elif line_ending == LineEnding.crlf:
        line_ending_str = "\r\n"
    else:  # LineEnding.lf
        line_ending_str = "\n"

    combined_text = ""
    for file_path in sorted(target_files):
        typer.secho(f"Reading: {file_path}", fg=typer.colors.CYAN, err=True)
        reader = ReaderFactory.get_reader(file_path)
        combined_text += reader.read(file_path)

    merged_result = engine.run(combined_text, strategy)
    formatted_data = formatter.format(merged_result, line_ending_str)

    if is_stdout:
        sys.stdout.write(formatted_data)
    else:
        if output:
            out_path = Path(output)
        else:
            out_path = Path(f"summary.{formatter.extension()}")

        if out_path.exists():
            typer.secho(
                f"Error: File already exists: {out_path}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(1)

        if format_type == FormatType.xlsx:
            formatted_data.to_excel(out_path)
        else:
            out_path.write_text(
                formatted_data,
                encoding="utf-8",
            )

        typer.secho(f"Saved to: {out_path}", fg=typer.colors.GREEN, err=True)


if __name__ == "__main__":
    app()
