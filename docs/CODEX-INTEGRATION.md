# Codex CLI Integration Guide

## Overview

Codex CLI sessions are automatically extracted hourly by the Universal Memory system. However, unlike Claude Code, Codex doesn't have a native hook system for loading memory at startup.

## Current Status

✅ **Auto-Extraction:** Working - Sessions saved hourly
✅ **Search:** Working - Use `uni-mem` commands
⚠️ **Startup Hook:** Not natively supported by Codex

## Options for Using Memory with Codex

### Option 1: Use the Wrapper (Recommended)

Use `codex-with-memory` instead of `codex`:

```bash
# Instead of:
codex

# Use:
~/.universal-memory/codex-with-memory

# Or create an alias:
alias codex-mem="~/.universal-memory/codex-with-memory"
```

This will:
1. Display recent memories from all AI systems
2. Then start Codex normally

### Option 2: Manual Check Before Starting

Before starting a Codex session, check recent memories:

```bash
# Show recent work
uni-mem show

# Search for relevant context
uni-mem search "topic"

# Then start Codex
codex
```

### Option 3: During Codex Session

While working in Codex, open another terminal and use `uni-mem`:

```bash
# In another terminal
uni-mem show --claude      # See what you did in Claude
uni-mem search "keyword"   # Find related work
```

## Automatic Extraction

Regardless of which option you choose, **all your Codex sessions are automatically captured** every hour by the LaunchAgent.

Check extraction status:
```bash
tail -f ~/.universal-memory/logs/codex-analyzer.log
```

## Future Enhancement

When Codex adds support for startup hooks or configuration scripts, we can integrate memory loading natively like we did with Claude Code.

## Recommended Alias

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# Universal Memory CLI
alias uni-mem="~/.universal-memory/uni-mem"

# Codex with Memory
alias codex-mem="~/.universal-memory/codex-with-memory"
```

Then you can use:
- `codex-mem` - Start Codex with memory loaded
- `codex` - Start Codex normally (memory still extracted hourly)
- `uni-mem` - Access unified memory anytime
