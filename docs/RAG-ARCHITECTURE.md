# Universal AI Memory - RAG Architecture

**Version:** 3.0.0 (RAG-Enabled)
**Created:** 2025-10-29
**Purpose:** Retrieval-Augmented Generation for AI Coding Assistants

---

## Core Concept: Memory-Aware LLMs

> **The LLM is part of the memory system, not just a consumer of it.**

This system implements a **true RAG (Retrieval-Augmented Generation)** architecture where:
- Memory retrieval happens **semantically**, not just by keywords
- LLMs receive **instructions** on how to query and use memory
- **Short-term (STM)** and **long-term (LTM)** memory are separated
- **Associations** between memories create a knowledge graph
- Memory is **infused once per session** with context about what's available

---

## 1. Memory Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    RAG MEMORY SYSTEM                           │
└────────────────────────────────────────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐      ┌─────────────────┐
        │  SHORT-TERM     │      │  LONG-TERM      │
        │  MEMORY (STM)   │      │  MEMORY (LTM)   │
        │                 │      │                 │
        │  Current        │      │  Historical     │
        │  session        │      │  knowledge      │
        │  context        │      │  graph          │
        │                 │      │                 │
        │  • Last 20-50   │      │  • All 164+     │
        │    memories     │      │    memories     │
        │  • Active work  │      │  • Indexed      │
        │  • Immediate    │      │  • Searchable   │
        └────────┬────────┘      └────────┬────────┘
                 │                        │
                 └────────────┬───────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  RETRIEVAL       │
                    │  ENGINE          │
                    │                  │
                    │  • Semantic      │
                    │  • Associative   │
                    │  • Contextual    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  LLM CONTEXT     │
                    │  INJECTION       │
                    └──────────────────┘
```

---

## 2. Short-Term Memory (STM)

### Definition
Working memory for the current session - immediate context the LLM needs.

### Characteristics
- **Size:** Last 20-50 memories (configurable)
- **Scope:** Recent work across all AI systems
- **Refresh:** Updated hourly by analyzers
- **Display:** Shown ONCE at session start

### What STM Contains
```json
{
  "stm": {
    "session_start": "2025-10-29T11:18:00",
    "entries": [
      {
        "id": "uuid",
        "date": "2025-10-29",
        "source": "claude",
        "summary": "Working on RAG architecture",
        "relevance": 0.95,
        "recency_score": 1.0
      },
      // ... 19-49 more recent memories
    ],
    "total_count": 20,
    "sources": {
      "claude": 15,
      "codex": 5
    }
  }
}
```

### STM Infusion at Session Start

**Current Problem:** Dedupe suppresses memory display if sessions restart within 5 seconds.

**New Behavior:**
```bash
# Session tracking (not time-based)
~/.universal-memory/runtime/session-{AI}-{PID}.lock

# Memory shown once per actual session
# Not suppressed by rapid restarts
# Cleared when session ends
```

---

## 3. Long-Term Memory (LTM)

### Definition
Persistent knowledge graph of all work - queryable on demand.

### Characteristics
- **Size:** All memories (164+ and growing)
- **Scope:** Complete history across all AI systems
- **Access:** Retrieved via semantic/associative queries
- **Storage:** `memories.jsonl` with semantic indexes

### What LTM Contains
```json
{
  "ltm": {
    "total_entries": 164,
    "indexed_topics": 560,
    "date_range": {
      "earliest": "2025-10-09",
      "latest": "2025-10-29"
    },
    "associations": {
      "memory_id_1": ["memory_id_2", "memory_id_3"],
      // ... semantic relationships
    },
    "embeddings_available": true
  }
}
```

---

## 4. Semantic Indexes & Associations

### Current State (Keyword-Based)
```json
{
  "by-topic.json": {
    "memory": ["uuid1", "uuid2", "uuid3"],
    "pharmacy": ["uuid4", "uuid5"]
  }
}
```

**Problem:** Simple keyword matching, no semantic understanding.

### New State (Semantic Associations)
```json
{
  "semantic-index.json": {
    "memories": [
      {
        "id": "uuid1",
        "embedding": [0.123, -0.456, ...],  // 384-dim vector
        "topics": ["memory", "architecture"],
        "associated_with": [
          {
            "id": "uuid2",
            "similarity": 0.87,
            "reason": "both discuss memory system design"
          },
          {
            "id": "uuid3",
            "similarity": 0.75,
            "reason": "related to RAG implementation"
          }
        ]
      }
    ]
  }
}
```

### Association Types
1. **Semantic Similarity** - Vector embeddings (cosine similarity)
2. **Topic Co-occurrence** - Memories sharing topics
3. **Temporal Proximity** - Related work in same timeframe
4. **File-based** - Memories modifying same files
5. **Project-based** - Memories in same project context
6. **Causal** - Explicit "this builds on that" relationships

---

## 5. LLM Instruction Set

### The Memory Contract

**The LLM must be taught how memory works.** This happens via system prompts injected at session start.

```markdown
## Your Memory System

You have access to a RAG-based memory system with two layers:

### Short-Term Memory (STM)
You have been shown 20 recent memories at session start. These represent:
- Your recent work across Claude Code and Codex CLI
- Context from the last few days
- Cross-system continuity

**How to use STM:**
- Reference these memories directly when relevant
- Mention memory IDs if you're building on previous work
- Ask the user if you need clarification on any memory

### Long-Term Memory (LTM)
You have access to 164+ historical memories via the `uni-mem` command.

**How to query LTM:**
- `uni-mem search "topic"` - Find relevant past work
- `uni-mem topics "pharmacy"` - See all pharmacy-related memories
- `uni-mem show --claude` - See only Claude Code work
- `uni-mem timeline --week` - Chronological view of this week

**When to query LTM:**
- User asks "have we done this before?"
- You need context on a specific topic
- You're starting work that might build on past work
- You want to find related files or approaches

### Memory-Aware Behavior

1. **Check before building** - Search memory to avoid duplicating work
2. **Reference past work** - Mention relevant memory IDs
3. **Build on context** - Use insights from previous sessions
4. **Cross-system awareness** - Remember work done in other AI systems
5. **Save important decisions** - Use `uni-mem save` for key insights

### Example Memory Usage

User: "Let's add authentication to the app"

You: "Let me check if we've worked on authentication before..."
     [Searches: `uni-mem search "authentication"`]

     "I see we discussed OAuth implementation in memory abc123
     (from 2025-10-15). Would you like to continue with that
     approach or start fresh?"
```

---

## 6. Retrieval Mechanisms

### Retrieval Triggers

**Automatic (STM Infusion):**
- Session start → Load 20 most recent memories
- Display once per session (not time-suppressed)
- Includes cross-system context

**On-Demand (LLM-Initiated):**
- `uni-mem search <query>` → Semantic search
- `uni-mem topics <topic>` → Topic-based retrieval
- `uni-mem show --claude` → Source-filtered retrieval

**Context-Aware (Future):**
- File opens → "You worked on this file in memory xyz"
- Git commit → "Related to previous work in memory abc"
- Error occurs → "Similar error solved in memory def"

### Retrieval Ranking

When retrieving from LTM, rank by:
1. **Semantic similarity** (if embeddings available)
2. **Recency** (more recent = higher relevance)
3. **Source match** (same AI system gets boost)
4. **Association strength** (strongly linked memories)
5. **User importance** (manual saves ranked higher)

### Retrieval Format

```json
{
  "query": "authentication",
  "results": [
    {
      "id": "uuid1",
      "summary": "Implemented OAuth with JWT",
      "relevance_score": 0.92,
      "reasoning": "Exact topic match + high semantic similarity",
      "source": "claude",
      "date": "2025-10-15",
      "associations": [
        {"id": "uuid2", "reason": "Uses same JWT library"}
      ]
    }
  ],
  "total_found": 5,
  "showing": 3
}
```

---

## 7. Session Management (Fixing Dedupe)

### Current Problem

**Time-based dedupe:** Suppresses memory if shown within 5 seconds.
```python
# Current (WRONG)
if now - last_display_time < 5:
    suppress_output()
```

**Issue:** If Claude crashes and restarts, user doesn't see memory context.

### New Approach: Session-Based Infusion

**Track actual sessions, not time windows:**

```python
# NEW: Session-based tracking
session_file = f"~/.universal-memory/runtime/session-{AI}-{SESSION_ID}.lock"

if session_file.exists():
    # Already shown for this session
    skip_display()
else:
    # First time this session
    show_memory()
    create_session_lock()
```

**Session ID Sources:**
- Claude Code: Use conversation ID or process ID
- Codex CLI: Use session ID from CLI
- Manual: Generate unique ID per invocation

**Session Lifecycle:**
```
Session Start → Create lock file → Display memory ONCE
     ↓
Work happens (memory not shown again)
     ↓
Session End → Remove lock file
     ↓
New Session Start → Lock doesn't exist → Display memory
```

---

## 8. Implementation Roadmap

### Phase 1: Fix Dedupe (Immediate)
- [ ] Replace time-based dedupe with session-based tracking
- [ ] Ensure memory infuses once per actual session
- [ ] Test with rapid restarts

### Phase 2: LLM Instructions (Week 1)
- [ ] Create memory contract document
- [ ] Inject instructions at session start
- [ ] Add helper commands to system prompt
- [ ] Test LLM's ability to query memory

### Phase 3: Semantic Associations (Week 2)
- [ ] Generate embeddings for all memories
- [ ] Build semantic similarity index
- [ ] Implement association graph
- [ ] Add association-based retrieval

### Phase 4: Enhanced Retrieval (Week 3)
- [ ] Semantic search with embeddings
- [ ] Relevance scoring algorithm
- [ ] Context-aware suggestions
- [ ] File/Git integration

### Phase 5: STM/LTM Separation (Week 4)
- [ ] Separate STM and LTM storage
- [ ] Automatic STM refresh
- [ ] LTM archival policies
- [ ] Performance optimization

---

## 9. Data Structures

### Memory Entry (Enhanced)

```json
{
  "id": "uuid",
  "timestamp": "2025-10-29T11:18:00",
  "date": "2025-10-29",
  "source": "claude|codex|unified",
  "type": "manual|auto",
  "summary": "One-line description",

  "details": {
    "topics": ["memory", "rag", "architecture"],
    "files_modified": ["RAG-ARCHITECTURE.md"],
    "git_commit": "abc123",
    "conversation_id": "43085bae",
    "message_count": 25,
    "project": "universal-memory"
  },

  "metadata": {
    "importance": 0.85,
    "category": "architecture",
    "tags": ["rag", "design", "memory"],
    "user_saved": true
  },

  "rag_data": {
    "embedding": [0.123, -0.456, ...],  // 384-dim vector
    "associations": [
      {
        "memory_id": "uuid2",
        "type": "semantic",
        "score": 0.87
      },
      {
        "memory_id": "uuid3",
        "type": "temporal",
        "score": 0.75
      }
    ],
    "retrieval_count": 5,
    "last_retrieved": "2025-10-29T12:00:00"
  },

  "memory_tier": "stm|ltm",
  "recency_score": 0.95
}
```

### STM State File

```json
{
  "session_id": "claude-12345",
  "started": "2025-10-29T11:18:00",
  "stm_snapshot": {
    "entries": [
      // Last 20 memory entries
    ],
    "displayed_at_start": true,
    "context_summary": "Working on RAG architecture and memory system design"
  }
}
```

---

## 10. Example User Experience

### Session Start (New Behavior)

```
$ claude

Loading Universal AI Memory...

════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (20 recent entries across all AI systems)
════════════════════════════════════════════════════════════════

🔵 🤖 2025-10-29: Working on RAG architecture [memory:uuid1]
🟢 🤖 2025-10-29: Fixed initialization bug [memory:uuid2]
🔵 ✍️ 2025-10-28: Decided to use embeddings for search [memory:uuid3]
...

💡 TIP: I can search my long-term memory with `uni-mem search`
         I have 164 memories available - ask me to check them!

════════════════════════════════════════════════════════════════

Claude Code >
```

### LLM Using Memory

```
User: Let's add authentication

Claude: Before we start, let me check if we've worked on
        authentication before...

        [Internally queries: uni-mem search "authentication"]

        I found 3 related memories:

        1. [2025-10-15] Implemented OAuth with JWT (memory:abc123)
        2. [2025-10-10] Discussed auth strategy (memory:def456)
        3. [2025-10-08] Set up user database (memory:ghi789)

        It looks like you started OAuth implementation in mid-October.
        Would you like to continue that work or start fresh?
```

---

## 11. Benefits of RAG Architecture

### For Users
1. **Never lose context** - Work across sessions seamlessly
2. **Cross-system awareness** - See work from all AI tools
3. **Smart suggestions** - LLM references past work
4. **Faster development** - Build on previous solutions

### For LLMs
1. **Extended context** - Access to full work history
2. **Semantic understanding** - Find related work, not just keywords
3. **Decision support** - Reference past architectural choices
4. **Continuous learning** - Each session builds on previous knowledge

### For System
1. **Scalable** - Works with thousands of memories
2. **Fast retrieval** - <100ms with semantic indexes
3. **Privacy-first** - All local, no cloud dependencies
4. **Extensible** - Add new AI systems easily

---

## 12. Key Differences from Current System

| Aspect | Current (v2.0) | RAG-Enabled (v3.0) |
|--------|----------------|-------------------|
| Retrieval | Keyword matching | Semantic similarity |
| Memory tiers | Single storage | STM + LTM separation |
| LLM awareness | Passive display | Active instruction set |
| Dedupe | Time-based (5 sec) | Session-based |
| Associations | None | Knowledge graph |
| Infusion | May be suppressed | Once per session, guaranteed |
| Search | Text matching | Embedding-based |
| Context | Static display | Dynamic retrieval |

---

## 13. Success Metrics

### Technical
- [ ] Memory displayed at every session start (no suppression)
- [ ] <100ms retrieval time for semantic search
- [ ] 90%+ recall on relevant memory queries
- [ ] Association graph coverage >80%

### User Experience
- [ ] LLM references past work without prompting
- [ ] Users report "it remembers what we did"
- [ ] Cross-system continuity (Claude ↔ Codex)
- [ ] Reduced duplicate work

### System Health
- [ ] All 164+ memories have embeddings
- [ ] Indexes rebuild in <1 second
- [ ] No memory corruption from concurrent writes
- [ ] Session tracking accurate

---

## 14. Next Steps

1. **Immediate:** Fix dedupe mechanism (session-based)
2. **Week 1:** Create and inject LLM instruction set
3. **Week 2:** Generate embeddings for existing memories
4. **Week 3:** Build semantic association graph
5. **Week 4:** Separate STM/LTM with automatic management

---

**This is a RAG system where the LLM is a first-class participant in memory management, not just a consumer.**

---

*Created: 2025-10-29*
*Architecture: RAG-Enabled with STM/LTM*
*Version: 3.0.0*
