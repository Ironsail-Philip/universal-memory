#!/bin/bash
# Claude Code Session Start Hook
# Loads unified memory at the start of each Claude session
# Uses session-based tracking (not time-based suppression)

python3 ~/.universal-memory/hooks/load-memory.py \
  --source all \
  --limit 20 \
  --session-key claude
