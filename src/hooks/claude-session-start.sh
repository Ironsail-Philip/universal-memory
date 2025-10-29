#!/bin/bash
# Claude Code Session Start Hook
# Loads unified memory at the start of each Claude session

python3 ~/.universal-memory/hooks/load-memory.py --source all --limit 12 \
  --dedupe-seconds 5 --dedupe-key claude
