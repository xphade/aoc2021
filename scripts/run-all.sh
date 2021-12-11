#!/usr/bin/env bash
# run-all.sh - Run all (currently implemented) days

cd "$(dirname "$0")/.."
echo

for i in {01..25}; do
    # Continue if file does not (yet) exist
    file=(./${i}_*.py)
    if [[ ! -f ${file[0]} ]]; then
        continue
    fi

    echo "Day $i:"
    eval "./${i}_*.py data/${i}_*.txt"
    echo
done