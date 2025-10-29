# Universal AI Memory v3.0.0 - Release Notes

**Release Date:** 2025-10-29
**Type:** Major Release
**Status:** Production Ready

---

## 🎉 Major Milestone: RAG-Enabled Memory System

Universal AI Memory v3.0.0 transforms the system from basic storage into a true **Retrieval-Augmented Generation (RAG) system** where AI models actively participate in memory management.

---

## 🚀 What's New

### 1. RAG Architecture
- **Short-Term Memory (STM)**: Last 20 memories shown at session start
- **Long-Term Memory (LTM)**: All historical memories searchable on-demand
- **Semantic associations**: Foundation for embedding-based retrieval (roadmap)

### 2. Session-Based Tracking
- **Guaranteed memory infusion**: Once per session, not time-suppressed
- **PID-based tracking**: Each unique session gets memory context
- **Automatic cleanup**: Old session locks removed after 24 hours
- **Fixes critical bug**: Memory no longer suppressed on rapid restarts

### 3. LLM Integration
- **AI models know how to use memory**: Complete instruction set included
- **Memory IDs displayed**: Reference specific past work `[mem:abc123]`
- **Active retrieval**: AI checks memory before building features
- **Cross-system awareness**: AI acknowledges work from other tools

### 4. Enhanced Display
- **STM/LTM terminology**: Clear distinction between memory tiers
- **Tips on querying**: LLM told how to search Long-Term Memory
- **Increased context**: 20 entries (up from 12)
- **Better formatting**: Professional, informative display

### 5. Comprehensive Documentation
- **3,500+ lines**: Complete system documentation
- **6 major documents**:
  - DOCUMENTATION.md (navigation index)
  - README.md (user guide, updated for v3.0)
  - RAG-SYSTEM-OVERVIEW.md (system concepts)
  - RAG-ARCHITECTURE.md (technical spec)
  - LLM-MEMORY-INSTRUCTIONS.md (AI model guide)
  - CHANGES-v3.0.md (changelog)
- **Clear navigation**: Easy to find what you need

---

## 🔧 Breaking Changes

**None!** v3.0.0 is 100% backward compatible with v2.0.

- Old `--dedupe-seconds` still works with `--legacy-time-based` flag
- All existing memories preserved
- No configuration changes required

---

## 📊 Improvements Over v2.0

| Feature | v2.0 | v3.0 |
|---------|------|------|
| **Architecture** | Storage only | RAG-enabled |
| **Memory infusion** | May be suppressed | Guaranteed once per session |
| **LLM awareness** | None | Full instruction set |
| **Memory display** | 12 entries | 20 entries with IDs |
| **Tracking** | Time-based (5 sec) | Session-based (PID) |
| **STM/LTM** | No distinction | Clear separation |
| **Documentation** | Basic (~500 lines) | Comprehensive (3,500+ lines) |
| **Memory IDs** | Not shown | Shown for reference |

---

## 🐛 Bug Fixes

### Critical Fix: Memory Suppression
**Problem:** Time-based dedupe could suppress memory if sessions restarted within 5 seconds (e.g., Claude crash & restart).

**Solution:** Session-based tracking using PID ensures each unique session gets memory infused exactly once.

**Impact:** Users now **guaranteed** to see memory context at every session start.

---

## 📁 File Changes

### New Files
- `hooks/load-memory.py` - Updated with session tracking
- `hooks/claude-session-start.sh` - Updated arguments
- `docs/DOCUMENTATION.md` - Master navigation index
- `docs/RAG-SYSTEM-OVERVIEW.md` - System overview
- `docs/RAG-ARCHITECTURE.md` - Technical architecture
- `docs/LLM-MEMORY-INSTRUCTIONS.md` - AI model guide
- `docs/CHANGES-v3.0.md` - Complete changelog

### Updated Files
- `README.md` - Updated for v3.0 RAG features
- `analyzers/claude-analyzer.py` - Minor improvements
- `analyzers/codex-analyzer.py` - Minor improvements
- `config/launchagents/*.plist` - Updated for v3.0

### Removed Files
- Old v1.0/v2.0 documentation (archived in working system)

---

## 💻 Installation

### New Installation

```bash
git clone https://github.com/Ironsail-Philip/universal-memory.git
cd universal-memory
./install.sh
```

### Upgrading from v2.0 or v1.0

Simply pull and re-run the installer:

```bash
cd universal-memory
git pull
./install.sh
```

**No data loss, no configuration changes needed!**

---

## 📖 Documentation

After installation, read:

1. **Quick start**: `cat ~/.universal-memory/DOCUMENTATION.md`
2. **User guide**: `cat ~/.universal-memory/README.md`
3. **System overview**: `cat ~/.universal-memory/RAG-SYSTEM-OVERVIEW.md`

---

## 🎯 System Requirements

- **macOS** (tested) or **Linux** (compatible)
- **Python 3.6+**
- **Claude Code** and/or **Codex CLI**
- ~500KB disk space

---

## ✅ Verification

After installation, verify the system:

```bash
# Check statistics
uni-mem stats

# Show recent memories
uni-mem show 5

# Test session hook
~/.universal-memory/hooks/claude-session-start.sh
```

You should see the new v3.0 STM/LTM display format.

---

## 🔮 Roadmap

### v3.1 (Planned)
- Semantic embeddings for all memories
- Association graph showing related work
- True semantic search (not just keywords)

### v3.2 (Planned)
- Relevance scoring algorithm
- Context-aware suggestions
- File/Git integration

### v3.3 (Planned)
- Separate STM/LTM storage files
- Automatic STM refresh
- LTM archival policies
- Performance optimization for 1000+ memories

---

## 🙏 Credits

Built with Claude Code in a meta moment - this RAG system captured its own transformation from basic storage to intelligent retrieval!

---

## 📝 License

MIT License - See [LICENSE](LICENSE)

---

## 🔗 Links

- **Repository**: https://github.com/Ironsail-Philip/universal-memory
- **Issues**: https://github.com/Ironsail-Philip/universal-memory/issues
- **Releases**: https://github.com/Ironsail-Philip/universal-memory/releases

---

## 📊 Statistics

- **Code changes**: ~150 lines modified
- **Documentation added**: ~3,000 lines
- **Files changed**: 10+
- **Bug fixes**: 1 critical (memory suppression)
- **New features**: 5 major (RAG, STM/LTM, session tracking, LLM integration, comprehensive docs)

---

**Universal AI Memory v3.0.0 - Never lose context again!**

*Released: 2025-10-29*
