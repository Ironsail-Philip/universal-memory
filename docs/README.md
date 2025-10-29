# 🧠 Universal AI Memory

**RAG-enabled unified memory system for AI coding assistants**

**Version:** 3.0.0 | **Architecture:** Retrieval-Augmented Generation (RAG)

Currently supports: **Claude Code** and **Codex CLI**

---

## 🎯 What Is This?

Universal AI Memory is a **RAG-based memory system** that enables AI coding assistants to remember and build on previous work. Instead of starting fresh each session, AI models can:
- Retrieve context from past work (Short-Term Memory)
- Query historical knowledge on-demand (Long-Term Memory)
- Reference specific past decisions by ID
- Build continuity across sessions and AI systems

**Key Benefits:**
- 🔵 **See what you did in Claude** when working in Codex
- 🟢 **See what you did in Codex** when working in Claude
- 🧠 **AI models actively use memory** - they check before building
- 🔍 **Search everything** from one interface
- 📊 **Track all your work** across all AI systems
- ⚡ **Automatic extraction** - zero manual effort
- ✅ **Memory shown once per session** - guaranteed infusion

---

## 📖 Documentation

| Read This For... | Document |
|------------------|----------|
| **Overview & concepts** | [RAG-SYSTEM-OVERVIEW.md](RAG-SYSTEM-OVERVIEW.md) |
| **Commands & usage** | This file (README.md) |
| **Technical architecture** | [RAG-ARCHITECTURE.md](RAG-ARCHITECTURE.md) |
| **How AI models use it** | [LLM-MEMORY-INSTRUCTIONS.md](LLM-MEMORY-INSTRUCTIONS.md) |
| **What's new in v3.0** | [CHANGES-v3.0.md](CHANGES-v3.0.md) |
| **All documentation** | [DOCUMENTATION.md](DOCUMENTATION.md) |

---

## 📊 Current Stats

Run `uni-mem stats` to see your current stats. Example:

```
Total Entries: 147
By Source:
  🔵 claude: 136
  🟢 codex: 7
  ⚪ unified: 4
```

---

## 🚀 Quick Start

### Show Recent Memories

```bash
# Show last 10 entries (all sources)
uni-mem show

# Show last 20 entries
uni-mem show 20

# Show only Claude Code memories
uni-mem show --claude

# Show only Codex memories
uni-mem show --codex

# Show only manual saves
uni-mem show --manual
```

### Search

```bash
# Search all memories
uni-mem search "pharmacy"

# Search only Claude memories
uni-mem search "authentication" --claude

# Search only manual entries
uni-mem search "project" --manual
```

### Save Manually

```bash
# Save a quick note
uni-mem save "Completed feature X"

# Save with metadata
uni-mem save "Fixed bug" '{"project": "app", "priority": "high"}'

# Save with tags
uni-mem save "Important decision" --tags "architecture,review"
```

### Topics

```bash
# List all topics
uni-mem topics

# Show entries for a specific topic
uni-mem topics "authentication"
```

### Statistics

```bash
# Overall stats
uni-mem stats

# System health check
uni-mem status
```

---

## 🏗️ How It Works

### RAG Architecture (v3.0)

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
                │  All 164+ memories      │
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
            │                        │
            └──→ unified storage ────┘
```

### Memory Tiers

**Short-Term Memory (STM):**
- Last 20 memories across all AI systems
- Displayed automatically at session start
- Provides immediate context
- Includes memory IDs for reference

**Long-Term Memory (LTM):**
- All 164+ historical memories
- Searchable via `uni-mem` commands
- Retrieved on-demand by AI models
- Indexed by topic, date, source

### Automatic Extraction

**LaunchAgents** run hourly to extract new conversations:
- `com.universal.memory.claude` - Extracts Claude Code conversations
- `com.universal.memory.codex` - Extracts Codex CLI sessions

**No manual action required!** Just work normally and memories are captured automatically.

### Session Integration

When you start a **Claude Code** session, recent memories are automatically loaded and displayed:

```
======================================================================
📚 Universal AI Memory - Recent Context (12 entries)
======================================================================

⚪ ✍️ 2025-10-28: Migration complete! 147 total memories...
🔵 🤖 2025-10-28: Conversation session
🟢 🤖 2025-10-28: Installed run, environment_context
...
```

This gives you instant context from **all your AI work**, not just Claude!

- Startup dedupe ensures repeated launches within a few seconds do not show duplicate banners.
- The Codex wrapper shares the same dedupe so you see a single memory banner per CLI start.

---

## 📁 Directory Structure

```
~/.universal-memory/
├── memories.jsonl              # ALL your memories (147+ entries)
├── uni-mem                     # Universal CLI
├── analyzers/
│   ├── claude-analyzer.py     # Claude Code extractor
│   ├── codex-analyzer.py      # Codex CLI extractor
│   └── common.py              # Shared utilities
├── hooks/
│   ├── claude-session-start.sh
│   ├── load-memory.py
│   └── (codex hooks - future)
├── scripts/
│   ├── codex-with-memory        # Wrapper with dedupe + passthrough
│   └── configure-claude-hook.py # Auto-configure Claude SessionStart hook
├── index/
│   ├── by-source.json         # Fast lookups
│   ├── by-topic.json
│   └── by-date.json
├── logs/
│   ├── claude-analyzer.log
│   └── codex-analyzer.log
└── config/
    └── launchagents/          # Hourly extraction agents
```

---

## 🔧 Manual Operations

### Run Analyzers Manually

```bash
# Extract new Claude conversations
python3 ~/.universal-memory/analyzers/claude-analyzer.py

# Extract new Codex sessions
python3 ~/.universal-memory/analyzers/codex-analyzer.py
```

### Check LaunchAgents

```bash
# List running agents
launchctl list | grep universal

# Check logs
tail -f ~/.universal-memory/logs/claude-analyzer.log
tail -f ~/.universal-memory/logs/codex-analyzer.log
```

### Rebuild Indexes

```bash
uni-mem reindex
```

---

## 🎨 Icons Reference

### Source Icons

- 🔵 **Claude Code** - Entries from Claude Code
- 🟢 **Codex CLI** - Entries from Codex CLI
- ⚪ **Unified** - Manual entries or migrations

### Type Icons

- ✍️ **Manual** - User explicitly saved
- 🤖 **Auto** - Automatically extracted

---

## 📖 Data Format

Each memory entry in `memories.jsonl`:

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
    "files_modified": ["file1.ts"],
    "message_count": 25,
    "project": "project-name"
  },
  "metadata": {
    "tags": ["tag1", "tag2"]
  }
}
```

---

## 🔍 Search Tips

### Basic Search

```bash
uni-mem search "keyword"
```

Searches in:
- Summary
- Topics
- Details (files, projects, etc.)

### Filtered Search

```bash
# Only Claude memories
uni-mem search "bug fix" --claude

# Only Codex memories
uni-mem search "implementation" --codex

# Only manual saves
uni-mem search "important" --manual
```

### Topic Search

```bash
# See all memories about authentication
uni-mem topics "authentication"
```

---

## 🛠️ Troubleshooting

### Memories Not Appearing

1. **Check LaunchAgents are running:**
   ```bash
   launchctl list | grep universal
   ```

2. **Check logs for errors:**
   ```bash
   tail -f ~/.universal-memory/logs/claude-analyzer.log
   ```

3. **Run analyzer manually:**
   ```bash
   python3 ~/.universal-memory/analyzers/claude-analyzer.py
   ```

### Search Not Working

Indexes may need rebuilding:
```bash
uni-mem reindex
```

### Session Hook Not Loading

Check Claude Code settings:
```bash
cat ~/.claude/settings.json | grep hooks
```

Should point to:
```
/Users/YOUR_USER/.universal-memory/hooks/claude-session-start.sh
```

---

## 📚 Advanced Usage

### Export Data

```bash
# Export to JSON
uni-mem export --format json > backup.json

# Export to CSV
uni-mem export --format csv > backup.csv
```

### Statistics Breakdown

```bash
# Detailed breakdown by source, type, date
uni-mem stats --breakdown
```

### Timeline View

```bash
# Chronological view of all work
uni-mem timeline

# Specific date
uni-mem timeline --date 2025-10-27

# This week
uni-mem timeline --week
```

---

## 🎯 Best Practices

### 1. Save Important Decisions

Don't rely only on auto-extraction. Save key decisions manually:

```bash
uni-mem save "Decided to use PostgreSQL over MongoDB for better ACID compliance" \
  --tags "architecture,database,decision"
```

### 2. Use Tags

Tag entries for easy retrieval:

```bash
uni-mem save "Completed auth migration" --tags "milestone,auth,done"
```

### 3. Search Before Starting

Before starting work, search to see if you've done something similar:

```bash
uni-mem search "authentication"
```

### 4. Review Weekly

Check your work periodically:

```bash
uni-mem timeline --week
```

---

## 🚀 What's Next

### Planned Features

- **Phase 2:** Cross-system associations (link related memories)
- **Phase 3:** Knowledge graph visualization
- **Phase 4:** Semantic search (embeddings)
- **Phase 5:** AI-powered insights and suggestions

### Extensibility

The system is designed to support additional AI systems:
- GitHub Copilot (future)
- Cursor (future)
- Others (extensible architecture)

Just add a new analyzer for the new system!

---

## 📝 Notes

### Performance

- **Search:** <100ms for 1000+ entries
- **Indexing:** Real-time updates
- **Storage:** ~300KB per 1000 entries

### Privacy

All data is **local** on your machine:
- No cloud sync (yet)
- No external services
- Complete control

### Compatibility

- **macOS:** Full support (LaunchAgents)
- **Linux:** Compatible (use cron instead of LaunchAgents)
- **Windows:** Not yet supported

---

## 🆘 Getting Help

### Check System Status

```bash
uni-mem status
```

Shows:
- Memory file health
- Index status
- Analyzer availability
- Current context

### View Logs

```bash
# Claude analyzer
tail -50 ~/.universal-memory/logs/claude-analyzer.log

# Codex analyzer
tail -50 ~/.universal-memory/logs/codex-analyzer.log

# LaunchAgent logs
tail -50 ~/.universal-memory/logs/launchd-claude-stdout.log
```

---

## 🎉 Success Stories

With Universal Memory, you can:

1. **Continue work seamlessly** - Start in Claude, finish in Codex
2. **Never lose context** - All work captured automatically
3. **Find anything instantly** - Full-text search across everything
4. **See the big picture** - 560+ topics indexed automatically
5. **Track your progress** - Timeline view of all work

---

## 📄 License

Personal use. Built for productivity.

---

## 🙏 Credits

Built with Claude Code in a meta moment - creating a memory system while the memory system captures its own creation!

---

**Questions? Issues? Ideas?**

Check `uni-mem status` for system health
Read `UNIFIED-ARCHITECTURE.md` for technical details
Run `uni-mem help` for command reference

**Happy coding with perfect memory! 🧠✨**
