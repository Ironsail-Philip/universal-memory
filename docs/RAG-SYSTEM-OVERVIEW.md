# Universal AI Memory - RAG System Overview

**Complete Documentation for RAG-Enabled Memory System**
**Version:** 3.0.0
**Date:** 2025-10-29

---

## 📚 Document Index

This system has multiple documentation files for different audiences:

| Document | Audience | Purpose |
|----------|----------|---------|
| **RAG-SYSTEM-OVERVIEW.md** (this file) | Everyone | High-level understanding |
| **RAG-ARCHITECTURE.md** | Developers | Technical architecture & implementation |
| **LLM-MEMORY-INSTRUCTIONS.md** | AI Models | How LLMs should use memory |
| **README.md** | End Users | User guide and commands |
| **UNIFIED-ARCHITECTURE.md** | Developers | Original unified storage design |

---

## 🎯 What Is This System?

A **Retrieval-Augmented Generation (RAG) memory system** for AI coding assistants that:

1. **Stores all work** across Claude Code and Codex CLI in one place
2. **Retrieves relevant memories** semantically, not just by keywords
3. **Teaches LLMs** how to use memory through explicit instructions
4. **Separates STM/LTM** - working memory vs historical knowledge
5. **Guarantees memory infusion** once per session (not time-suppressed)

---

## 🧠 Core Concepts

### Traditional AI Assistant
```
User → Question → AI → Answer (from training data only)
```

**Problem:** No continuity, no memory, starts fresh every time

### RAG-Enabled AI Assistant (This System)
```
User → Question → AI → Check Memory → Retrieve Context → Answer
                        ↓
                   Save Decision
                        ↓
                   Long-Term Storage
```

**Benefit:** AI builds on previous work, maintains context, provides continuity

---

## 📊 System Architecture

### Two-Tier Memory

```
┌─────────────────────────────────────────────┐
│  SHORT-TERM MEMORY (STM)                    │
│  • Last 20 memories                         │
│  • Shown at session start                   │
│  • Immediate context                        │
│  • Cross-system (Claude + Codex)            │
└─────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────┐
│  LONG-TERM MEMORY (LTM)                     │
│  • All 164+ memories                        │
│  • Searchable via uni-mem                   │
│  • Indexed by topic/date/source             │
│  • Available on-demand                      │
└─────────────────────────────────────────────┘
```

### Data Flow

```
┌──────────────┐              ┌──────────────┐
│ CLAUDE CODE  │              │  CODEX CLI   │
│ User works   │              │  User works  │
└──────┬───────┘              └──────┬───────┘
       │                             │
       │ Hourly Extraction           │ Hourly Extraction
       │                             │
       ▼                             ▼
┌──────────────────────────────────────────────┐
│  UNIFIED STORAGE                             │
│  ~/.universal-memory/memories.jsonl          │
│  • All work from all AI systems              │
│  • Append-only with file locking             │
│  • Indexed for fast retrieval                │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  RETRIEVAL ENGINE                            │
│  • Session start: Load STM (20 recent)       │
│  • On-demand: Query LTM (164+ total)         │
│  • Semantic associations (future)            │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  LLM CONTEXT INJECTION                       │
│  • STM displayed at startup                  │
│  • LTM queried via uni-mem commands          │
│  • Instructions on how to use memory         │
└──────────────────────────────────────────────┘
```

---

## 🔄 Session Lifecycle

### Old Behavior (Time-Based Dedupe) ❌

```
Session 1 starts → Show memory → Create timestamp
    ↓
    Wait 3 seconds
    ↓
Session 2 starts (crashed & restarted)
    ↓
    Check timestamp → Within 5 seconds → SUPPRESS MEMORY ❌
    ↓
User doesn't see memory context!
```

### New Behavior (Session-Based Tracking) ✅

```
Session 1 starts (PID: 12345)
    ↓
Check: session-claude-12345.lock exists? NO
    ↓
Create lock file → SHOW MEMORY ✅
    ↓
Work happens... memory already shown, don't show again
    ↓
Session ends → Lock file remains (cleaned up after 24h)
    ↓
Session 2 starts (PID: 12346) - NEW SESSION
    ↓
Check: session-claude-12346.lock exists? NO
    ↓
Create lock file → SHOW MEMORY ✅
```

**Key Difference:** Each unique session gets memory, not time-suppressed!

---

## 💡 How LLMs Use This System

### At Session Start

LLM receives STM infusion:
```
════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (STM) - Recent Context
   20 entries across all AI systems
════════════════════════════════════════════════════════════════

🔵 🤖 2025-10-29: Working on RAG architecture [mem:a8380efc]
🟢 🤖 2025-10-29: Fixed initialization bug [mem:e4c016f0]
🔵 ✍️ 2025-10-28: Decided to use embeddings [mem:6250c57e]
...

💡 I can search LONG-TERM MEMORY (164+ entries) with:
   • uni-mem search "<keyword>"
   • uni-mem topics "<topic>"
   • uni-mem show --claude
```

### During Conversation

LLM actively queries LTM:

```
User: "Let's add authentication"

LLM (thinking): Should check if we've done this before...

[Runs: uni-mem search "authentication"]

LLM: "I found 3 related memories. We implemented OAuth in
     [mem:abc123] on 2025-10-15. Should we continue that
     approach or start fresh?"
```

### Key LLM Behaviors

1. **Check before building** - Search memory to avoid duplicates
2. **Reference memory IDs** - Cite specific work: `[mem:abc123]`
3. **Cross-system awareness** - Acknowledge Codex work in Claude
4. **Save decisions** - Suggest `uni-mem save` for important choices

See **LLM-MEMORY-INSTRUCTIONS.md** for complete LLM guide.

---

## 🗂️ File Structure

```
~/.universal-memory/
│
├── memories.jsonl ················· CORE STORAGE (164+ entries)
│
├── RAG-SYSTEM-OVERVIEW.md ········· This file (overview)
├── RAG-ARCHITECTURE.md ············ Technical architecture
├── LLM-MEMORY-INSTRUCTIONS.md ····· How LLMs use memory
├── README.md ···················· User guide
│
├── analyzers/ ····················· Auto-extraction
│   ├── claude-analyzer.py ········· Extract Claude conversations
│   ├── codex-analyzer.py ·········· Extract Codex sessions
│   └── common.py ·················· Shared logic
│
├── hooks/ ························· Session startup
│   ├── claude-session-start.sh ···· Claude hook (session-based)
│   └── load-memory.py ············· Memory loader (NEW: session tracking)
│
├── index/ ························· Fast retrieval
│   ├── by-source.json ············· claude/codex/unified
│   ├── by-topic.json ·············· Keyword topics
│   └── by-date.json ··············· Date index
│
├── runtime/ ······················· Session tracking
│   └── session-*.lock ············· Active session locks
│
├── logs/ ·························· System logs
│   ├── claude-analyzer.log
│   └── codex-analyzer.log
│
└── config/ ························ Configuration
    └── launchagents/ ·············· Hourly extraction
```

---

## 🔧 What Changed in v3.0

### From v2.0 (Basic Storage) to v3.0 (RAG-Enabled)

| Feature | v2.0 | v3.0 |
|---------|------|------|
| **Retrieval** | Keyword matching | Semantic associations (roadmap) |
| **Memory Tiers** | Single storage | STM + LTM separation |
| **LLM Awareness** | Passive display | Active instruction set |
| **Dedupe** | Time-based (5 sec) | Session-based (PID tracking) |
| **Infusion** | May be suppressed | Guaranteed once per session |
| **Instructions** | None | LLM-MEMORY-INSTRUCTIONS.md |
| **Display** | Simple list | STM/LTM context with tips |
| **Memory IDs** | Not shown | Shown for LLM reference |

### Code Changes

1. **`hooks/load-memory.py`:**
   - ✅ Session-based tracking (not time-based)
   - ✅ Automatic cleanup of old lock files
   - ✅ STM/LTM distinction in display
   - ✅ Memory IDs shown for reference
   - ✅ Tips on querying LTM

2. **`hooks/claude-session-start.sh`:**
   - ✅ Updated to use `--session-key` instead of `--dedupe-seconds`
   - ✅ Increased limit from 12 to 20 entries

3. **`codex-with-memory`:**
   - ✅ Updated to use session-based tracking
   - ✅ Same session-key approach

---

## 🚀 Usage Examples

### End User (in Claude Code)

Session starts automatically with memory:
```
Claude Code >

════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (STM) - Recent Context
   20 entries across all AI systems
════════════════════════════════════════════════════════════════
...

User: "Let's work on the pharmacy feature"

Claude: "I see we've been working on pharmacy integrations.
        In [mem:6250c57e] from yesterday, we added 25+
        pharmacies to the marketplace. Should we continue
        that or start something new?"
```

### LLM (actively using memory)

```
# User asks to add feature
Step 1: Check memory
  → uni-mem search "feature"

# Found related work
Step 2: Reference it
  → "We implemented this in [mem:abc123]..."

# Complete new work
Step 3: Save decision
  → uni-mem save "Updated feature with X approach"
```

### Manual Query (user runs directly)

```bash
$ uni-mem search "authentication"

Found 3 memories:
🔵 🤖 2025-10-15: Implemented OAuth with JWT [mem:abc123]
🔵 ✍️ 2025-10-10: Decided on auth strategy [mem:def456]
🔵 🤖 2025-10-08: Set up user database [mem:ghi789]
```

---

## 📈 Current Stats

```
Total Memories: 164
  🔵 Claude: 140
  🟢 Codex:  10
  ⚪ Manual: 14

Date Range: 2025-10-09 to 2025-10-29 (20 days)
Topics Indexed: 560+
Average per day: ~8 memories
```

---

## 🎯 Benefits

### For Users
- ✅ Never lose context between sessions
- ✅ See work from all AI systems in one place
- ✅ LLM references past work automatically
- ✅ Faster development (build on previous solutions)

### For LLMs
- ✅ Extended context beyond session limits
- ✅ Semantic understanding of project history
- ✅ Can reference specific past decisions
- ✅ Continuous learning across sessions

### For Teams
- ✅ Share memory across different AI tools
- ✅ Maintain consistency in architectural decisions
- ✅ Track project evolution over time
- ✅ Onboard new team members with history

---

## 🔮 Roadmap

### Phase 1: Fix Dedupe ✅ COMPLETED
- [x] Session-based tracking instead of time-based
- [x] Guaranteed infusion once per session
- [x] Automatic cleanup of old locks

### Phase 2: LLM Instructions ✅ COMPLETED
- [x] LLM-MEMORY-INSTRUCTIONS.md created
- [x] STM/LTM distinction in display
- [x] Memory IDs shown for reference
- [x] Tips on querying LTM

### Phase 3: Semantic Associations (Next)
- [ ] Generate embeddings for all memories
- [ ] Build similarity index
- [ ] Association graph (memory → related memories)
- [ ] Semantic search (not just keywords)

### Phase 4: Enhanced Retrieval (Future)
- [ ] Relevance scoring algorithm
- [ ] Context-aware suggestions
- [ ] File/Git integration
- [ ] "You worked on this file before" notifications

### Phase 5: Production Polish (Future)
- [ ] Separate STM/LTM storage
- [ ] Automatic STM refresh
- [ ] LTM archival policies
- [ ] Performance optimization for 1000+ memories

---

## 🏗️ How It Works (Step by Step)

### 1. Work Happens

User works in Claude Code or Codex CLI. Conversations are saved locally.

### 2. Hourly Extraction

LaunchAgents run every hour:
- `com.universal.memory.claude` → Extract Claude conversations
- `com.universal.memory.codex` → Extract Codex sessions

### 3. Unified Storage

Analyzers append to `~/.universal-memory/memories.jsonl`:
```json
{
  "id": "abc123...",
  "source": "claude",
  "type": "auto",
  "summary": "Working on RAG architecture",
  "details": {"topics": ["rag", "memory"], ...}
}
```

### 4. Session Start

User starts new Claude session → Hook triggers:
```bash
python3 ~/.universal-memory/hooks/load-memory.py \
  --source all \
  --limit 20 \
  --session-key claude
```

### 5. Session Check

```python
pid = os.getpid()  # e.g., 12345
session_file = f"session-claude-12345.lock"

if session_file.exists():
    # Already shown this session
    skip
else:
    # New session - show memory!
    display_memory()
    create_lock_file()
```

### 6. Memory Displayed

```
════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (STM) - Recent Context
   20 entries across all AI systems
════════════════════════════════════════════════════════════════
[20 most recent memories with IDs, icons, tips]
```

### 7. LLM Receives Context

LLM sees:
- 20 recent memories (STM)
- Instructions on how to query more
- Memory IDs for referencing
- Cross-system work visibility

### 8. Active Retrieval

During conversation, LLM can:
```bash
uni-mem search "topic"      # Search LTM
uni-mem topics "pharmacy"   # Topic history
uni-mem show --claude       # Filter by source
```

### 9. Continuous Loop

- User works → Saved locally
- Hourly → Extracted to unified storage
- Next session → Memory infused again
- LLM → Builds on previous work

---

## 🔒 Privacy & Security

- ✅ **100% local** - No cloud sync
- ✅ **Your data only** - Never leaves your machine
- ✅ **File locking** - Safe concurrent writes
- ✅ **Append-only** - No data loss
- ✅ **Backed up** - Automatic backups created

---

## 📚 Further Reading

- **RAG-ARCHITECTURE.md** - Deep dive into technical design
- **LLM-MEMORY-INSTRUCTIONS.md** - How LLMs should use memory
- **README.md** - User guide and command reference
- **UNIFIED-ARCHITECTURE.md** - Original unified storage design

---

## 🎉 Success Criteria

You know the system is working when:

- ✅ Memory appears at every session start (not suppressed)
- ✅ LLM references past work with memory IDs
- ✅ Cross-system work is acknowledged (Claude ↔ Codex)
- ✅ Users say "wow, it remembered that!"
- ✅ Duplicate work is avoided
- ✅ Context continues across sessions

---

## 🤝 Contributing

This is a personal productivity system, but improvements welcome:

1. **Add new AI systems** - Create analyzer for new tool
2. **Improve extraction** - Better topic extraction
3. **Semantic search** - Implement embeddings
4. **Better UI** - Enhance memory display

---

## 📝 Version History

- **v1.0** - Basic memory storage per AI system
- **v2.0** - Unified storage (one JSONL for all AIs)
- **v3.0** - RAG-enabled (STM/LTM, LLM instructions, session tracking)

---

**You now have a RAG system where LLMs actively participate in memory management, providing true cross-session continuity.**

---

*Version: 3.0.0 RAG-Enabled*
*Created: 2025-10-29*
*Last Updated: 2025-10-29*
