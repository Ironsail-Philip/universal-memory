# Universal AI Memory - Installation Guide

## Quick Install

### Option 1: From GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/Ironsail-Philip/universal-memory.git
cd universal-memory

# Run installer
./install.sh
```

### Option 2: Download Zip

1. Download the latest release from GitHub
2. Extract the zip file
3. Open terminal in the extracted directory
4. Run: `./install.sh`

### Option 3: One-Command Install

```bash
# Coming soon - direct download and install
curl -fsSL https://example.com/install.sh | bash
```

---

## System Requirements

### Supported Platforms
- ✅ **macOS** (10.15+)
- ✅ **Linux** (Ubuntu, Debian, Fedora, etc.)
- ❌ **Windows** (not yet supported)

### Required Software
- **Python 3** (3.7+) - Usually pre-installed on macOS and Linux
- **Claude Code** or **Codex CLI** (at least one)

### Optional
- **Git** - For easy updates via `git pull`

---

## Installation Process

The installer will automatically:

1. ✅ Create `~/.universal-memory/` directory
2. ✅ Install application files (analyzers, CLI, hooks)
3. ✅ Set proper permissions
4. ✅ Configure Claude Code hooks
5. ✅ Set up automatic extraction (hourly)
   - macOS: LaunchAgents
   - Linux: Cron jobs
6. ✅ Add shell aliases (`uni-mem`, `codex-mem`)
7. ✅ Initialize empty storage
8. ✅ Run initial extraction
9. ✅ Verify installation

---

## What Gets Installed

### Application Files (in `~/.universal-memory/`)
```
analyzers/          # Conversation extractors
  ├── common.py
  ├── claude-analyzer.py
  └── codex-analyzer.py
hooks/              # Session startup scripts
  ├── claude-session-start.sh
  └── load-memory.py
config/             # Configuration files
  └── launchagents/
uni-mem             # Main CLI tool
codex-with-memory   # Codex wrapper
```

### User Data (created but initially empty)
```
memories.jsonl      # Your memories (initially empty)
logs/               # Runtime logs
sessions/           # Processing state
index/              # Search indexes
```

### System Integration
- **Shell aliases** added to `~/.zshrc` or `~/.bashrc`
- **Claude hook** added to `~/.claude/settings.json`
- **LaunchAgents** (macOS) or **cron jobs** (Linux) for hourly extraction

---

## Post-Installation

### 1. Reload Your Shell

```bash
# For zsh (macOS default)
source ~/.zshrc

# For bash
source ~/.bashrc
```

### 2. Verify Installation

```bash
# Check system status
uni-mem status

# View statistics
uni-mem stats

# Show recent memories
uni-mem show
```

### 3. Start Using

**Claude Code:**
- Just start Claude Code normally
- Memories will auto-load at startup

**Codex CLI:**
```bash
# Use the wrapper for memory loading
codex-mem

# Or check manually before starting
uni-mem show
codex
```

---

## Manual Configuration

### Claude Code Hook (if not auto-configured)

Add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "matchers": ["startup", "resume"],
      "hooks": [{
        "type": "command",
        "command": "/Users/Ironsail-Philip/.universal-memory/hooks/claude-session-start.sh"
      }]
    }]
  }
}
```

Replace `Ironsail-Philip` with your actual username.

### Shell Aliases (if not auto-added)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Universal AI Memory aliases
alias uni-mem="$HOME/.universal-memory/uni-mem"
alias codex-mem="$HOME/.universal-memory/codex-with-memory"
```

---

## Troubleshooting

### "Command not found: uni-mem"

**Solution:** Reload your shell or use full path:
```bash
source ~/.zshrc
# Or
~/.universal-memory/uni-mem stats
```

### "Permission denied" errors

**Solution:** Set proper permissions:
```bash
chmod +x ~/.universal-memory/uni-mem
chmod +x ~/.universal-memory/analyzers/*.py
```

### LaunchAgents not running (macOS)

**Check status:**
```bash
launchctl list | grep universal
```

**Reload:**
```bash
launchctl bootout gui/$(id -u)/com.universal.memory.claude
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.universal.memory.claude.plist
```

### Cron jobs not running (Linux)

**Check crontab:**
```bash
crontab -l | grep universal
```

**View logs:**
```bash
tail -f ~/.universal-memory/logs/cron-claude.log
```

### No memories showing up

**Run analyzers manually:**
```bash
python3 ~/.universal-memory/analyzers/claude-analyzer.py
python3 ~/.universal-memory/analyzers/codex-analyzer.py
```

**Check logs:**
```bash
tail -f ~/.universal-memory/logs/claude-analyzer.log
```

---

## Reinstalling

To reinstall (updates application, preserves data):

```bash
cd universal-memory
./install.sh
```

The installer will:
- Detect existing installation
- Ask for confirmation
- Backup existing memories
- Install new version

---

## Updating

### From Git

```bash
cd universal-memory
git pull
./update.sh
```

### From Zip

1. Download latest version
2. Extract
3. Run `./update.sh`

The updater will:
- Backup your data
- Update application files
- Preserve all memories
- Verify installation

---

## Uninstalling

To completely remove Universal AI Memory:

```bash
cd universal-memory
./uninstall.sh
```

The uninstaller will:
- Offer to backup your memories
- Remove LaunchAgents/cron jobs
- Remove shell aliases
- Remove installation directory
- Prompt about Claude Code hook

---

## Migration from Old Systems

If you previously used separate `~/.claude-memory/` or `~/.codex-memory/` systems:

```bash
python3 ~/.universal-memory/migrate-old-memories.py
```

This will:
- Import old memories
- Tag them as migrated
- Preserve all data
- Suggest archiving old systems

---

## Advanced Configuration

### Change Extraction Frequency

**macOS (LaunchAgents):**

Edit `~/Library/LaunchAgents/com.universal.memory.claude.plist`:
```xml
<key>StartInterval</key>
<integer>1800</integer>  <!-- 30 minutes instead of 3600 (1 hour) -->
```

Then reload:
```bash
launchctl bootout gui/$(id -u)/com.universal.memory.claude
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.universal.memory.claude.plist
```

**Linux (cron):**

Edit crontab:
```bash
crontab -e
```

Change `0 * * * *` (hourly) to `*/30 * * * *` (every 30 minutes)

---

## Getting Help

### Check System Status
```bash
uni-mem status
```

### View Logs
```bash
# Claude analyzer
tail -50 ~/.universal-memory/logs/claude-analyzer.log

# Codex analyzer
tail -50 ~/.universal-memory/logs/codex-analyzer.log
```

### Documentation
```bash
cat ~/.universal-memory/README.md
cat ~/.universal-memory/UNIFIED-ARCHITECTURE.md
```

### GitHub Issues
Report problems at: https://github.com/Ironsail-Philip/universal-memory/issues

---

## Next Steps

Once installed, see:
- `README.md` - User guide and features
- `UNIFIED-ARCHITECTURE.md` - Technical details
- `CODEX-INTEGRATION.md` - Codex-specific info

**Happy coding with perfect memory!** 🧠✨
