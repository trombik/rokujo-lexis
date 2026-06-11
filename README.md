## Usage

```console

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
