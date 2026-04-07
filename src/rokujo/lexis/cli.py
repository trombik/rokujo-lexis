import typer
from pathlib import Path
from enum import Enum

from rokujo.lexis.engine import AnalyzerEngine
from rokujo.lexis.strategies.noun import (
    CompoundCounter,
    ChunkCounter,
)


class StrategyType(str, Enum):
    noun = "noun"
    compound = "compound"


app = typer.Typer()


@app.command()
def analyze(
    file_path: Path = typer.Argument(..., help="Path to the text file to analyze"), # noqa E501
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

    engine = AnalyzerEngine(model=model)

    strategy_map = {
        StrategyType.noun: ChunkCounter(),
        StrategyType.compound: CompoundCounter(),
    }
    strategy = strategy_map[strategy_name]

    text = file_path.read_text(encoding="utf-8")
    result = engine.run(text, strategy)

    typer.secho(f"--- Results (Strategy: {strategy_name.value}) ---", fg=typer.colors.CYAN) # noqa E501
    for word, count in result.most_common(20):
        print(f"{count: >4}: {word}")


if __name__ == "__main__":
    app()
