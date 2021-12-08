#!/usr/bin/env bash
# format-code.sh - Format all python files in the repository

cd "$(dirname "$0")"
python3 -m black ../*.py