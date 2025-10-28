# 🧠 Universal AI Memory

**One unified memory system for all your AI coding assistants**

Never lose context when switching between Claude Code and Codex CLI. Everything captured, everything searchable, everything automatic.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS | Linux](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)]()

---

## 🎯 What Is This?

Universal AI Memory captures and indexes **all your work** across different AI coding assistants into **one unified storage**. No more forgetting what you did in Claude when working in Codex, or vice versa.

### Key Features

- 🔵 **See Claude Code work** when using Codex CLI
- 🟢 **See Codex CLI work** when using Claude Code
- 🔍 **Search everything** from one interface
- 📊 **Track all your work** across all AI systems
- ⚡ **Automatic extraction** - zero manual effort
- 🔒 **100% local** - your data never leaves your machine

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Ironsail-Philip/universal-memory.git
cd universal-memory

# Run one-command installer
./install.sh
```

That's it! The installer automatically:
- ✅ Installs to `~/.universal-memory/`
- ✅ Configures Claude Code hooks
- ✅ Sets up hourly extraction
- ✅ Adds CLI aliases
- ✅ Initializes storage

### First Commands

```bash
# View recent work from all AI systems
uni-mem show

# Search everything
uni-mem search "keyword"

# See statistics
uni-mem stats

# Start Codex with memory loaded
codex-mem
```

---

## 💡 How It Works

### Architecture

```
                ONE UNIFIED STORAGE
             ~/.universal-memory/
                     ↑↑
                     ││
         ┌───────────┘└───────────┐
         │                        │
   Claude Code                Codex CLI
  (auto-extract)           (auto-extract)
         │                        │
   Hourly analyzer          Hourly analyzer
         │                        │
         └──→ unified storage ────┘
```

### Automatic Extraction

- **LaunchAgents** (macOS) or **cron jobs** (Linux) run hourly
- Conversations automatically captured from both AI systems
- Indexed by source, topic, date
- Available instantly via CLI

### Session Integration

**Claude Code:**
- Memories auto-load at startup
- See context from both AI systems

**Codex CLI:**
- Use `codex-mem` wrapper
- Or check manually with `uni-mem show`

---

## 📊 Example Output

```bash
$ uni-mem show

Recent Memory (10 entries):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔵 🤖 2025-10-28: Implemented authentication system
🟢 🤖 2025-10-28: Reviewed API endpoints
⚪ ✍️ 2025-10-28: Important architecture decision
🔵 🤖 2025-10-27: Fixed database migration bug
🟢 🤖 2025-10-27: Added unit tests
...
```

### Icons
- 🔵 Claude Code | 🟢 Codex CLI | ⚪ Manual
- 🤖 Auto-extracted | ✍️ Manually saved

---

## 🎨 Features

### CLI Commands

```bash
# Show recent memories
uni-mem show              # Last 10 entries
uni-mem show 20           # Last 20 entries
uni-mem show --claude     # Only Claude memories
uni-mem show --codex      # Only Codex memories

# Search
uni-mem search "keyword"
uni-mem search "bug fix" --claude

# Save manually
uni-mem save "Important decision made"

# Topics
uni-mem topics                    # List all topics
uni-mem topics "authentication"   # Show entries for topic

# Statistics
uni-mem stats             # Overall stats
uni-mem status            # System health check
```

### Automatic Features

- ⏰ **Hourly extraction** - New work captured automatically
- 📊 **Real-time indexing** - Instant search
- 🔄 **Cross-system context** - See all your work in one place
- 💾 **Safe concurrent writes** - File locking prevents corruption

---

## 📁 What Gets Installed

### Application Files (`~/.universal-memory/`)
```
analyzers/          # Conversation extractors
hooks/              # Session startup scripts
uni-mem             # Main CLI
codex-with-memory   # Codex wrapper
```

### User Data (created but initially empty)
```
memories.jsonl      # Your memories (JSONL format)
logs/               # Runtime logs
sessions/           # Processing state
index/              # Search indexes
```

**Your data stays 100% local. Nothing is ever uploaded.**

---

## 🔧 Requirements

### Supported Platforms
- ✅ macOS (10.15+)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ❌ Windows (not yet supported)

### Required Software
- Python 3 (3.7+)
- Claude Code or Codex CLI

### Optional
- Git (for easy updates)

---

## 📖 Documentation

- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[docs/README.md](docs/README.md)** - User guide and features
- **[docs/UNIFIED-ARCHITECTURE.md](docs/UNIFIED-ARCHITECTURE.md)** - Technical architecture
- **[docs/CODEX-INTEGRATION.md](docs/CODEX-INTEGRATION.md)** - Codex-specific info

---

## 🔄 Updating

```bash
cd universal-memory
git pull
./update.sh
```

Your memories and configuration are preserved during updates.

---

## 🗑️ Uninstalling

```bash
cd universal-memory
./uninstall.sh
```

The uninstaller offers to backup your memories before removal.

---

## 🛠️ Development

### Project Structure

```
universal-memory/
├── install.sh              # One-command installer
├── update.sh               # Update script
├── uninstall.sh            # Uninstaller
├── src/                    # Application source
│   ├── analyzers/         # Conversation extractors
│   ├── hooks/             # Session integration
│   ├── cli/               # CLI tool
│   └── config/            # Configuration files
├── scripts/               # Helper scripts
└── docs/                  # Documentation
```

### Running Tests

```bash
# Test CLI
~/.universal-memory/uni-mem stats

# Test analyzers manually
python3 ~/.universal-memory/analyzers/claude-analyzer.py
python3 ~/.universal-memory/analyzers/codex-analyzer.py

# Check logs
tail -f ~/.universal-memory/logs/claude-analyzer.log
```

---

## 🌟 Key Achievements

- ✅ **Unified Storage** - Single source of truth for all AI work
- ✅ **Zero-Effort Operation** - Automatic extraction and indexing
- ✅ **Cross-System Context** - See work from all AI systems
- ✅ **Fast & Efficient** - Sub-100ms searches
- ✅ **Extensible Design** - Easy to add new AI systems

---

## 🚧 Roadmap

### Phase 2: Associations (Planned)
- Link related memories across systems
- Knowledge graph connections

### Phase 3: Advanced Features (Planned)
- Semantic search with embeddings
- AI-powered summaries
- Importance scoring

### Phase 4: Distribution (In Progress)
- ✅ GitHub distribution
- ✅ One-command installer
- 🔄 Homebrew package
- 🔄 npm package

---

## 🤝 Contributing

Contributions welcome! This project is built to help developers maintain context across AI coding assistants.

### Areas for Contribution
- Windows support
- Additional AI system integrations (GitHub Copilot, Cursor, etc.)
- Semantic search features
- UI/visualization tools

---

## 📝 Technical Highlights

### Storage Format
- **JSONL** (newline-delimited JSON) for efficient append operations
- **File locking** (fcntl.flock) for safe concurrent writes
- **Pre-computed indexes** for fast searches

### Memory Entry Schema
```json
{
  "id": "uuid-v4",
  "timestamp": "2025-10-28T10:00:00.123456",
  "date": "2025-10-28",
  "source": "claude|codex|unified",
  "type": "manual|auto",
  "summary": "One sentence description",
  "details": {
    "topics": ["topic1", "topic2"],
    "files_modified": ["file.ts"],
    "message_count": 25
  }
}
```

### Performance
- **Search:** <100ms for 1000+ entries
- **Storage:** ~300KB per 1000 entries
- **Memory Usage:** <50MB

---

## 🙏 Credits

Built with Claude Code in a meta moment - creating a memory system while the system captured its own creation!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/Ironsail-Philip/universal-memory/issues)
- **Documentation:** See `docs/` directory
- **Status Check:** Run `uni-mem status`

---

## 🎉 Success Stories

With Universal Memory, you can:

1. **Continue work seamlessly** - Start in Claude, finish in Codex
2. **Never lose context** - All work captured automatically
3. **Find anything instantly** - Full-text search across everything
4. **See the big picture** - Timeline view of all work
5. **Track your progress** - Comprehensive statistics

---

**Happy coding with perfect memory!** 🧠✨

---

## Star History

If you find this project helpful, please consider giving it a star ⭐

---

**Questions? Check out the [documentation](docs/) or open an [issue](https://github.com/Ironsail-Philip/universal-memory/issues)!**
