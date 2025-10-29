# Universal AI Memory v1.0.2 - Release Notes

Copy this into the GitHub release description:

---

## 🧠 Universal AI Memory - Smart Startup Release

**Cleaner session banners + automated Claude hook configuration**

### ✨ Highlights

- **Smart dedupe guard** — Session banners show once even if you reopen Codex/Claude immediately.
- **Automated Claude setup** — Installer + updater now patch `SessionStart` hooks for you (with backups).
- **Codex wrapper refresh** — Wrapper captures loader output, respects dedupe, then launches the real `codex`.
- **Docs refreshed** — README, status, and verification guides now reflect the streamlined workflow.

### 🧩 What Changed

- `hooks/load-memory.py` gains a runtime sentinel (`--dedupe-*` flags) shared by both hooks.
- `scripts/codex-with-memory` prints the banner only when new output exists and delegates via `command codex`.
- `scripts/configure-claude-hook.py` added; `install.sh`/`update.sh` call it automatically.
- Documentation updated to describe dedupe behavior, wrapper usage, and automated hooks.

### 🚀 Upgrade Steps

```bash
git pull
./update.sh
source ~/.zshrc   # or reload your shell
```

### ✅ Post-Install Checklist

1. `~/.universal-memory/codex-with-memory --version` → Banner once, then version output.
2. `bash ~/.universal-memory/hooks/claude-session-start.sh` twice → Second run within 5s stays quiet.
3. Confirm `~/.claude/settings.local.json` (or `settings.json`) contains the SessionStart hook + fresh backup.

### 📖 Documentation

- [Installation Guide](INSTALL.md)
- [Updated README](README.md)
- [Codex Integration](docs/CODEX-INTEGRATION.md)
- [System Status Report](SYSTEM-STATUS.md)

### 🖥️ Platform Support

- ✅ macOS (LaunchAgents)
- ✅ Linux (cron)
- ❌ Windows (not yet supported)

### 📄 License

MIT License — see [LICENSE](LICENSE)

---

Happy coding with a cleaner startup experience! 🎉
