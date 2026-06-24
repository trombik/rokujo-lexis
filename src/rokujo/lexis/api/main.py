from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

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
)
from rokujo.lexis.readers import ReaderFactory

app = FastAPI(
    title="Rokujo Text Analysis API",
    description="API server inspired by the Rokujo CLI architecture.",
    version="0.1.0"
)

StrategyType = Literal["compound", "noun", "numeral", "proper"]
FormatType = Literal["csv", "tsv"]

STRATEGY_MAP = {
    "noun": ChunkCounter,
    "compound": CompoundCounter,
    "proper": ProperNounCounter,
    "numeral": NumeralExtractor,
}

FORMATTER_MAP = {
    "csv": CSVFormatter,
    "tsv": TSVFormatter,
}


class AnalysisRequest(BaseModel):
    text: str = Field(..., description="The raw content to be parsed")
    ext: str = Field(..., description="The file format/extension to determine the reader")
    strategy: StrategyType = Field("noun", description="Analysis strategy to use")


class AnalysisResponse(BaseModel):
    strategy: StrategyType
    format: FormatType
    result: str


@app.post(
    "/v1/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract, analyze, and format text"
)
async def analyze_text(request: AnalysisRequest, format_type: FormatType = "csv"):
    ext = request.ext.lower()
    if not ext.startswith("."):
        ext = f".{ext}"

    with NamedTemporaryFile(mode="w", delete=False, suffix=ext, encoding="utf-8") as tmp:
        tmp.write(request.text)
        tmp_path = Path(tmp.name)

    try:
        reader = ReaderFactory.get_reader(tmp_path)
        combined_text = reader.read(tmp_path)
        tmp_path.unlink()

        engine = AnalyzerEngine(model="en_core_web_md")
        strategy = STRATEGY_MAP[request.strategy]()
        formatter = FORMATTER_MAP[format_type]()

        merged_result = engine.run(combined_text, strategy)
        formatted_data = formatter.format(merged_result, "\n")

        return AnalysisResponse(
            strategy=request.strategy,
            format=format_type,
            result=formatted_data
        )

    except Exception as e:
        if tmp_path.exists():
            tmp_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Analysis failed: {str(e)}"
        )


current_dir = Path(__file__).parent
static_dir_path = current_dir / "static"

app.mount("/", StaticFiles(directory=static_dir_path, html=True), name="static")
