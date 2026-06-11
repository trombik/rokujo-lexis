#!/bin/sh

STRATEGIES="noun proper compound numeral"
for S in ${STRATEGIES}; do
    uv run lexis -s "${S}" -o "${S}.csv" sample.txt
done
