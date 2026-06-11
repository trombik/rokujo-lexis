# rokujo-lexis

`lexis` is a CLI tool to help translators generate terminology files, analyze
source texts, and avoid inconsistencies. It extracts key linguistic elements
from source texts into structured CSV files. `lexis` can identify named
entities, frequently-used nouns, compound nouns, and numeral entities.

## Requirements

* `python` 3.11+ ([Download Python](https://www.python.org/downloads/))
* `uv` ([Installing uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv))
* `git` ([Git - Install](https://git-scm.com/install/))

## Installation

Clone the repository and update the project's environment:

```console
git clone https://github.com/trombik/rokujo-lexis.git
cd rokujo-lexis
uv sync
```

Optionally, activate the virtual environment:

```console
# macOS / Linux / Unix variants
source .venv/bin/activate
```

```console
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## Usage

```console
> uv run lexis --help

 Usage: lexis [OPTIONS] FILE_PATH

 Analyze a text file using a specific strategy.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    file_path      PATH  Path to the text file to analyze [required]                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ --format              -f      [csv|tsv|xlsx]                  [default: csv]                            │
│ --output              -o      PATH                                                                      │
│ --strategy            -s      [compound|noun|numeral|proper]  Analysis strategy to use: noun (counts    │
│                                                               noun chunks), compound (counts compound   │
│                                                               nouns), proper (counts proper nouns),     │
│                                                               numeral (extracts numeral phrases)        │
│                                                               [default: noun]                           │
│ --model               -m      TEXT                            spaCy model name                          │
│                                                               [default: en_core_web_md]                 │
│ --line-ending                 [auto|lf|crlf]                  Line ending style: crlf (CRLF, RFC 4180   │
│                                                               compliant), lf (LF, Unix style), or auto  │
│                                                               (detect from OS)                          │
│                                                               [default: auto]                           │
│ --install-completion                                          Install completion for the current shell. │
│ --show-completion                                             Show completion for the current shell, to │
│                                                               copy it or customize the installation.    │
│ --help                                                        Show this message and exit.               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

The following command generates a list of noun chunks in `sample.txt`, writes
the result to `noun.csv`.

```console
uv run lexis -s noun -o noun.csv sample.txt
```
## Strategies

The command accepts one of analysis strategies; `noun`, `compound`, `numeral`,
and `proper`.

`noun` strategy counts noun *chunks* in the text, such as: `fact`, `large
number`, `eight or nine armoured division`.

```
house,8
war,7
sea,6
enemy,6
moment,5
...
```

`compound` strategy counts compound nouns, such as: `Air Force`, `opening
day`, `sea power`.

```
British Expeditionary Force,4
French Armies,3
Belgian Army,3
Air Force,3
Royal Air Force,3
...
```

`numeral` strategy extracts numeral phrases, such as `1,000 Frenchmen`,
`thousand airmen`, `21st March, 1918`. This strategy also tries to convert
common numeral phrases into Japanese where possible. For instance, `21st March,
1918` is converted to `1918年3月21日`.

```
"1,000 Frenchmen",,,1
"1,000 ships of all kinds",,,1
20 divisions,,,1
"21st March, 1918",1918年3月21日,DATE,1
220 light warships,,QUANTITY,1
...
```

`proper` strategy counts proper nouns, such as: `the British Expeditionary Force`,
`England`, `Napoleon`.

```
British,18
French,13
House,8
Army,8
Island,7
...
```

For complete results, see [example outputs](examples).

## License

[MIT](LICENSE)
