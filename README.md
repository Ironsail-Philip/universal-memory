# 🧠 Universal AI Memory

**RAG-enabled unified memory system for AI coding assistants**

**Version:** 3.0.0 | **Architecture:** Retrieval-Augmented Generation (RAG)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](https://github.com/Ironsail-Philip/universal-memory/releases)

---

## 🎯 What Is This?

Universal AI Memory is a **RAG-based memory system** that enables AI coding assistants to remember and build on previous work. Instead of starting fresh each session, AI models can:

- 🧠 **Retrieve context from past work** (Short-Term Memory)
- 🔍 **Query historical knowledge on-demand** (Long-Term Memory)
- 🔗 **Reference specific past decisions by ID**
- 🔄 **Build continuity across sessions and AI systems**

Currently supports: **Claude Code** and **Codex CLI**

---

## ✨ Key Features

### For Users
- ✅ **Cross-system memory** - See work from all AI tools in one place
- ✅ **Automatic extraction** - Zero manual effort, just work normally
- ✅ **Fast search** - Find anything in <100ms
- ✅ **Never lose context** - Work continues seamlessly across sessions

### For AI Models
- ✅ **RAG-aware** - AI actively uses memory, not just passive storage
- ✅ **STM/LTM separation** - Working memory + deep historical knowledge
- ✅ **Memory IDs** - Reference specific past work: `[mem:abc123]`
- ✅ **Instructed behavior** - AI knows when and how to query memory

### Technical
- ✅ **100% local** - All data stays on your machine
- ✅ **File locking** - Safe concurrent writes
- ✅ **Indexed retrieval** - Topic, date, source indexes
- ✅ **Hourly extraction** - Automatic background processing

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Ironsail-Philip/universal-memory.git
cd universal-memory

# Run the installer
./install.sh
```

The installer will:
- Copy files to `~/.universal-memory/`
- Set up analyzers for Claude Code and Codex CLI
- Configure LaunchAgents for automatic extraction
- Set up session hooks for memory infusion

### Usage

Once installed, memory works automatically!

**At session start**, you'll see recent memories:
```
════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (STM) - Recent Context
   20 entries across all AI systems
════════════════════════════════════════════════════════════════

🔵 🤖 2025-10-29: Working on RAG architecture [mem:abc123]
🟢 🤖 2025-10-29: Fixed initialization bug [mem:def456]
...

💡 I can search LONG-TERM MEMORY (164+ entries) with:
   • uni-mem search "<keyword>"
   • uni-mem topics "<topic>"
   • uni-mem show --claude
```

**Search your memory:**
```bash
# Find past work
uni-mem search "authentication"

# Show recent memories
uni-mem show 10

# See only Claude Code work
uni-mem show --claude

# List all topics
uni-mem topics

# View statistics
uni-mem stats
```

---

## 📖 Documentation

Comprehensive documentation is included:

| Document | Purpose |
|----------|---------|
| **[DOCUMENTATION.md](docs/DOCUMENTATION.md)** | Master navigation index |
| **[README.md](docs/README.md)** | User guide with commands |
| **[RAG-SYSTEM-OVERVIEW.md](docs/RAG-SYSTEM-OVERVIEW.md)** | System concepts and architecture |
| **[RAG-ARCHITECTURE.md](docs/RAG-ARCHITECTURE.md)** | Technical specification |
| **[LLM-MEMORY-INSTRUCTIONS.md](docs/LLM-MEMORY-INSTRUCTIONS.md)** | How AI models use memory |
| **[CHANGES-v3.0.md](docs/CHANGES-v3.0.md)** | What's new in v3.0 |

---

## 🏗️ How It Works

### RAG Architecture

```
                   TWO-TIER MEMORY SYSTEM
                ┌─────────────────────────┐
                │  SHORT-TERM MEMORY (STM)│
                │  Last 20 memories       │
                │  Shown at session start │
                └───────────┬─────────────┘
                            │
                ┌───────────┴─────────────┐
                │  LONG-TERM MEMORY (LTM) │
                │  All historical memories│
                │  Searchable via uni-mem │
                └───────────┬─────────────┘
                            │
                   ONE UNIFIED STORAGE
                ~/.universal-memory/
                        ↑↑
                        ││
            ┌───────────┘└───────────┐
            │                        │
    Claude Code                  Codex CLI
   (auto-extract)            (auto-extract)
            │                        │
    Hourly analyzer           Hourly analyzer
```

### Memory Tiers

**Short-Term Memory (STM):**
- Last 20 memories across all AI systems
- Automatically shown at session start
- Provides immediate context
- Includes memory IDs for reference

**Long-Term Memory (LTM):**
- All historical memories (searchable)
- Retrieved on-demand by AI models
- Indexed by topic, date, source
- Fast search (<100ms)

---

## 💻 System Requirements

- **macOS** (tested) or **Linux** (compatible)
- **Python 3.6+**
- **Claude Code** and/or **Codex CLI**
- ~500KB disk space

---

## 🔧 Configuration

The system works out of the box with sensible defaults. Advanced users can configure:

- **LaunchAgent frequency** (default: hourly)
- **STM size** (default: 20 entries)
- **Session hook behavior**

See [RAG-ARCHITECTURE.md](docs/RAG-ARCHITECTURE.md) for details.

---

## 📊 Example Output

### Session Start
```
════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (STM) - Recent Context
   20 entries across all AI systems
════════════════════════════════════════════════════════════════

🔵 🤖 2025-10-29: Working on authentication [mem:a8380efc]
🟢 🤖 2025-10-29: Fixed database bug [mem:6250c57e]
🔵 ✍️ 2025-10-28: Decided on PostgreSQL [mem:304b1b0b]
...
```

### Search Results
```bash
$ uni-mem search "authentication"

Found 3 memories:
🔵 🤖 2025-10-15: Implemented OAuth with JWT [mem:abc123]
🔵 ✍️ 2025-10-10: Decided on auth strategy [mem:def456]
🔵 🤖 2025-10-08: Set up user database [mem:ghi789]
```

### Statistics
```bash
$ uni-mem stats

Total Entries: 164
By Source:
  🔵 claude: 140
  🟢 codex: 10
  ⚪ unified: 14

By Type:
  🤖 auto: 136
  ✍️ manual: 28
```

---

## 🛠️ Troubleshooting

### Memory not showing at session start?

```bash
# Check hook configuration
cat ~/.claude/settings.json | grep hooks

# Test manually
~/.universal-memory/hooks/claude-session-start.sh
```

### Memories not being extracted?

```bash
# Check LaunchAgents
launchctl list | grep universal

# Check logs
tail -50 ~/.universal-memory/logs/claude-analyzer.log
```

### Search not working?

```bash
# Rebuild indexes
uni-mem reindex

# Verify data
cat ~/.universal-memory/memories.jsonl | wc -l
```

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Credits

Built with Claude Code in a meta moment - this memory system captured its own creation!

---

## 🔗 Links

- **Repository:** https://github.com/Ironsail-Philip/universal-memory
- **Issues:** https://github.com/Ironsail-Philip/universal-memory/issues
- **Releases:** https://github.com/Ironsail-Philip/universal-memory/releases

---

## 🎯 What's New in v3.0

### Major Changes
- ✅ **RAG Architecture** - True retrieval-augmented generation
- ✅ **STM/LTM Separation** - Working memory + deep storage
- ✅ **Session-based Tracking** - Guaranteed memory infusion (not time-suppressed)
- ✅ **LLM Instructions** - AI models know how to use memory
- ✅ **Memory IDs** - Reference specific past work
- ✅ **Comprehensive Docs** - 3,500+ lines of documentation

See [CHANGES-v3.0.md](docs/CHANGES-v3.0.md) for complete changelog.

---

## 🚀 Quick Links

- **Install:** `git clone ... && cd ... && ./install.sh`
- **Use:** `uni-mem stats` and `uni-mem search "<keyword>"`
- **Docs:** `cat ~/.universal-memory/DOCUMENTATION.md`

---

**Universal AI Memory v3.0 - Never lose context again!**
