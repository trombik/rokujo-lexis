from pathlib import Path
import pytest

from rokujo.lexis.readers import (
    PlainTextReader,
    DocxReader,
    XliffReader,
    MarkdownReader,
)

FIXTURE_DIR = Path(__file__).parents[2] / "fixtures"


@pytest.fixture
def txt_file() -> Path:
    return FIXTURE_DIR / "test.txt"


@pytest.fixture
def docx_file() -> Path:
    return FIXTURE_DIR / "test.docx"


@pytest.fixture
def xlf_file() -> Path:
    return FIXTURE_DIR / "test-xliff-2.0.xliff"


@pytest.fixture
def xlf12_file() -> Path:
    return FIXTURE_DIR / "test-xliff-1.2.xliff"


@pytest.fixture
def md_file() -> Path:
    return FIXTURE_DIR / "test.md"


class TestPlainTextReader:
    def test_read(self, txt_file: Path):
        reader = PlainTextReader()
        result = reader.read(txt_file)
        assert isinstance(result, str)
        assert result == "A text.\n"


class TestDocxReader:
    def test_read(self, docx_file: Path):
        reader = DocxReader()
        result = reader.read(docx_file)

        assert isinstance(result, str)
        assert len(result.split("\n")) == 6
        assert "Heading 1" in result
        assert "Heading 2" in result
        assert "This is a test document." in result
        assert "Item 1" in result
        assert "Item 2" in result


class TestXliffReader:
    def test_read(self, xlf_file: Path):
        reader = XliffReader()
        result = reader.read(xlf_file)

        assert isinstance(result, str)
        assert len(result.split("\n")) == 3
        assert "Quetzal" in result
        assert "An application to manipulate and process XLIFF documents" in result
        assert "XLIFF Data Manager" in result

    def test_read_v_1_2(self, xlf12_file: Path):
        reader = XliffReader()
        result = reader.read(xlf12_file)

        assert isinstance(result, str)
        assert "Quetzal" in result
        assert "An application to manipulate and process XLIFF documents" in result
        assert "XLIFF Data Manager" in result
        assert len(result.split("\n")) == 3


class TestMarkdownReader:
    def test_read(self, md_file: Path):
        reader = MarkdownReader()
        result = reader.read(md_file)

        assert isinstance(result, str)
        assert "Document Title" in result
        assert "This is a basic paragraph introducing the document."
        assert "*" not in result
        assert "multiple lines\n is processed as-is"
        assert "hyperlink" in result
        assert "https://example.com" not in result
        assert "First item" in result
        assert "Second item with a hyperlink" in result
        assert "Third item" in result
        assert "This is a blockquote text" in result

        assert "code block should be ignored" not in result
