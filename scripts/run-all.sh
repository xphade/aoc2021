#!/usr/bin/env bash

cd "$(dirname "$0")/.."
echo

for i in {1..8}; do
    echo "Day $i:"
    eval "./0${i}_*.py data/0${i}_*.txt"
    echo
done