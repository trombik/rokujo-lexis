@echo off
set "STRATEGIES=noun proper compound numeral"

for %%S in (%STRATEGIES%) do (
    uv run lexis -s "%%S" -o "%%S.csv" --line-ending lf sample.txt
)
