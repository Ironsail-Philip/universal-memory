# Universal AI Memory - Unified Architecture

**Version:** 2.0.0 (Unified)
**Created:** 2025-10-27
**Architecture Type:** Single Unified Storage

---

## Core Principle

> **One Storage, Multiple Sources**
> All AI systems write to ONE unified memory location. Each entry is tagged with its source.

---

## Directory Structure

```
~/.universal-memory/
├── memories.jsonl              # ALL memories (Claude + Codex + future)
├── uni-mem                     # Universal CLI (works everywhere)
├── analyzers/
│   ├── claude-analyzer.py     # Reads ~/.claude/projects/ → writes unified
│   ├── codex-analyzer.py      # Reads ~/.codex/sessions/ → writes unified
│   └── common.py              # Shared logic
├── hooks/
│   ├── claude-session-start.sh   # Claude Code startup hook
│   ├── codex-session-start.sh    # Codex startup hook
│   └── load-memory.py            # Memory loader (shared)
├── index/
│   ├── by-source.json         # Index by AI system
│   ├── by-topic.json          # Index by topic
│   ├── by-date.json           # Index by date
│   └── by-project.json        # Index by project
├── logs/
│   ├── claude-analyzer.log    # Claude analyzer logs
│   ├── codex-analyzer.log     # Codex analyzer logs
│   └── cli.log                # CLI operation logs
├── sessions/
│   ├── claude-processed.log   # Track processed Claude conversations
│   └── codex-processed.log    # Track processed Codex sessions
├── config/
│   ├── config.toml            # User configuration
│   └── launchagents/
│       ├── com.universal.memory.claude.plist
│       └── com.universal.memory.codex.plist
└── docs/
    ├── README.md
    ├── ARCHITECTURE.md (this file)
    ├── USER-MANUAL.md
    ├── MIGRATION-GUIDE.md
    └── API.md
```

---

## Unified Data Schema

### Memory Entry Format

Every entry in `memories.jsonl` follows this schema:

```json
{
  "id": "uuid-v4",
  "timestamp": "2025-10-27T16:00:00.123456",
  "date": "2025-10-27",
  "source": "claude|codex|future-ai",
  "type": "manual|auto",
  "summary": "One sentence description",
  "details": {
    "topics": ["topic1", "topic2"],
    "files_modified": ["file1.ts", "file2.py"],
    "git_commit": "abc123",
    "conversation_id": "43085bae",
    "session_id": "rollout-xyz",
    "message_count": 25,
    "project": "project-name"
  },
  "metadata": {
    "importance": 0.75,
    "category": "feature|bugfix|discussion|research",
    "tags": ["urgent", "review-needed"],
    "related_ids": ["uuid1", "uuid2"]
  }
}
```

### Key Fields

**`source`** - Which AI system created this memory
- `"claude"` - Created by Claude Code
- `"codex"` - Created by Codex CLI
- `"unified"` - Created via unified CLI (could be from either context)

**`type`** - How memory was created
- `"manual"` - User explicitly saved it
- `"auto"` - Automatically extracted by analyzer

**`id`** - UUID for unique identification across all systems

---

## System Integration

### Claude Code Integration

**1. Analyzer (`analyzers/claude-analyzer.py`)**
- **Reads:** `~/.claude/projects/*/conversations/*.jsonl`
- **Writes:** `~/.universal-memory/memories.jsonl`
- **Tracks:** `~/.universal-memory/sessions/claude-processed.log`
- **Frequency:** Hourly (via LaunchAgent)

**2. Session Hook (`hooks/claude-session-start.sh`)**
- **Trigger:** When Claude Code session starts
- **Action:** Load recent memories from unified storage
- **Display:** Last 10-15 entries (all sources)

**3. LaunchAgent**
- **Label:** `com.universal.memory.claude`
- **Schedule:** Hourly
- **Runs:** Claude analyzer

### Codex CLI Integration

**1. Analyzer (`analyzers/codex-analyzer.py`)**
- **Reads:** `~/.codex/sessions/YYYY/MM/DD/*.jsonl`
- **Writes:** `~/.universal-memory/memories.jsonl`
- **Tracks:** `~/.universal-memory/sessions/codex-processed.log`
- **Frequency:** Hourly (via LaunchAgent)

**2. Session Hook (`hooks/codex-session-start.sh`)**
- **Trigger:** When Codex session starts (if hooks supported)
- **Action:** Load recent memories from unified storage
- **Display:** Last 10-15 entries (all sources)

**3. LaunchAgent**
- **Label:** `com.universal.memory.codex`
- **Schedule:** Hourly
- **Runs:** Codex analyzer

---

## Universal CLI (`uni-mem`)

### Commands

```bash
# Show memories
uni-mem show [n]                    # Show last N entries (default 10)
uni-mem show --all                  # Show all memories
uni-mem show --claude               # Only Claude memories
uni-mem show --codex                # Only Codex memories
uni-mem show --manual               # Only manual saves
uni-mem show --auto                 # Only auto-extracted

# Save memory
uni-mem save "Summary" [details]    # Save from current context
uni-mem save "Summary" --source claude  # Explicit source
uni-mem save "Summary" --tags "urgent,review"

# Search
uni-mem search "keyword"            # Search all fields
uni-mem search "pharmacy" --claude  # Search Claude only
uni-mem search "auth" --manual      # Search manual entries only

# Statistics
uni-mem stats                       # Overall statistics
uni-mem stats --claude              # Claude statistics
uni-mem stats --codex               # Codex statistics
uni-mem stats --breakdown           # By source breakdown

# Topics
uni-mem topics                      # List all topics
uni-mem topics --claude             # Claude topics only
uni-mem topics "pharmacy"           # Entries for topic

# Timeline
uni-mem timeline                    # Chronological view
uni-mem timeline --date 2025-10-27  # Specific date
uni-mem timeline --week             # This week

# System
uni-mem status                      # System health check
uni-mem reindex                     # Rebuild indexes
uni-mem migrate                     # Migration tools
uni-mem export [format]             # Export data
```

### Source Detection

When you run `uni-mem save` without `--source`:
- If run from Claude Code context → `source: "claude"`
- If run from Codex context → `source: "codex"`
- Auto-detect by checking environment variables

---

## Data Flow

### Claude Code → Unified Memory

```
User works in Claude Code
    ↓
Conversation saved: ~/.claude/projects/PROJECT/conversations/CONV.jsonl
    ↓
[Hourly LaunchAgent triggers]
    ↓
claude-analyzer.py runs
    ↓
Reads new conversations
    ↓
Extracts topics, summary
    ↓
Creates entry with source="claude"
    ↓
Appends to ~/.universal-memory/memories.jsonl
    ↓
Updates indexes
    ↓
Logs to claude-processed.log
```

### Codex CLI → Unified Memory

```
User works in Codex
    ↓
Session saved: ~/.codex/sessions/YYYY/MM/DD/SESSION.jsonl
    ↓
[Hourly LaunchAgent triggers]
    ↓
codex-analyzer.py runs
    ↓
Reads new sessions
    ↓
Extracts topics, summary
    ↓
Creates entry with source="codex"
    ↓
Appends to ~/.universal-memory/memories.jsonl
    ↓
Updates indexes
    ↓
Logs to codex-processed.log
```

### Manual Save from Either System

```bash
# From Claude Code or Codex
uni-mem save "Completed feature X"

# Detects context (Claude or Codex)
# Creates entry with appropriate source
# Appends to unified storage
# Updates indexes immediately
```

---

## Searching Across Systems

### Example Queries

**"Show me everything about pharmacy"**
```bash
uni-mem search "pharmacy"
# Returns entries from BOTH Claude and Codex
```

**"What did I do in Claude yesterday?"**
```bash
uni-mem show --claude --date 2025-10-26
```

**"Show me all manual saves about authentication"**
```bash
uni-mem search "authentication" --manual
```

**"Timeline of ironflow project across both AIs"**
```bash
uni-mem timeline --project ironflow
# Shows Claude and Codex work chronologically
```

---

## Migration Strategy

### Existing Memories

**Claude Memory:** 31 entries in `~/.claude-memory/conversation-summaries.jsonl`
**Codex Memory:** 5 entries in `~/.codex-memory/conversation-summaries.jsonl`
**Total:** 36 entries

### Migration Process

```bash
# 1. Create unified storage
uni-mem migrate --init

# 2. Import Claude memories
uni-mem migrate --from ~/.claude-memory/conversation-summaries.jsonl \
                --source claude

# 3. Import Codex memories
uni-mem migrate --from ~/.codex-memory/conversation-summaries.jsonl \
                --source codex

# 4. Verify import
uni-mem stats --breakdown

# 5. Archive old systems (optional)
mv ~/.claude-memory ~/.claude-memory.backup
mv ~/.codex-memory ~/.codex-memory.backup
```

---

## Analyzer Design

### Shared Logic (`analyzers/common.py`)

```python
"""Shared logic for all analyzers"""

def extract_topics(text):
    """Common topic extraction"""
    pass

def generate_summary(messages):
    """Common summary generation"""
    pass

def append_to_unified_storage(entry):
    """Append entry to memories.jsonl with file locking"""
    pass

def update_indexes(entry):
    """Update all indexes"""
    pass
```

### Claude Analyzer (`analyzers/claude-analyzer.py`)

```python
"""
Claude-specific analyzer
Reads: ~/.claude/projects/*/conversations/*.jsonl
Format: Claude conversation format
"""

import common

def parse_claude_conversation(path):
    """Parse Claude format"""
    pass

def extract_claude_metadata(conv):
    """Get Claude-specific metadata"""
    pass

def process_claude_conversations():
    for conv in find_new_conversations():
        entry = {
            "source": "claude",
            "type": "auto",
            "summary": common.generate_summary(conv),
            "details": extract_claude_metadata(conv)
        }
        common.append_to_unified_storage(entry)
```

### Codex Analyzer (`analyzers/codex-analyzer.py`)

```python
"""
Codex-specific analyzer
Reads: ~/.codex/sessions/YYYY/MM/DD/*.jsonl
Format: Codex session format
"""

import common

def parse_codex_session(path):
    """Parse Codex format"""
    pass

def extract_codex_metadata(session):
    """Get Codex-specific metadata"""
    pass

def process_codex_sessions():
    for session in find_new_sessions():
        entry = {
            "source": "codex",
            "type": "auto",
            "summary": common.generate_summary(session),
            "details": extract_codex_metadata(session)
        }
        common.append_to_unified_storage(entry)
```

---

## Concurrency & File Locking

### Challenge

Both analyzers write to same file (`memories.jsonl`)

### Solution

```python
import fcntl

def append_to_unified_storage(entry):
    """Thread-safe append with file locking"""

    path = "~/.universal-memory/memories.jsonl"

    with open(path, 'a') as f:
        # Acquire exclusive lock
        fcntl.flock(f, fcntl.LOCK_EX)

        # Write entry
        f.write(json.dumps(entry) + '\n')

        # Lock automatically released on close
```

---

## Session Startup Integration

### Claude Code Hook

**Location:** `~/.claude/hooks/on-session-start.sh` (if supported) or equivalent

```bash
#!/bin/bash
# Load unified memory at Claude Code startup

echo "Loading Universal AI Memory..."
python3 ~/.universal-memory/hooks/load-memory.py --source all --limit 15
```

### Codex Hook

**Location:** Codex config or startup script

```bash
#!/bin/bash
# Load unified memory at Codex startup

echo "Loading Universal AI Memory..."
python3 ~/.universal-memory/hooks/load-memory.py --source all --limit 15
```

### Memory Loader (`hooks/load-memory.py`)

```python
"""Load and display recent memories at session start"""

def load_memory(source='all', limit=15):
    """
    Load recent memories
    source: 'all', 'claude', or 'codex'
    limit: number of entries
    """

    entries = read_recent_entries(limit)

    if source != 'all':
        entries = [e for e in entries if e['source'] == source]

    display_memory_summary(entries)
```

---

## Indexing System

### Purpose

Fast searching without reading entire JSONL file

### Indexes

**1. By Source (`index/by-source.json`)**
```json
{
  "claude": ["uuid1", "uuid2", ...],
  "codex": ["uuid3", "uuid4", ...]
}
```

**2. By Topic (`index/by-topic.json`)**
```json
{
  "pharmacy": ["uuid1", "uuid3", ...],
  "authentication": ["uuid2", "uuid4", ...]
}
```

**3. By Date (`index/by-date.json`)**
```json
{
  "2025-10-27": ["uuid1", "uuid2", ...],
  "2025-10-26": ["uuid3", "uuid4", ...]
}
```

### Index Updates

- Updated on every write (analyzer or manual save)
- Rebuilt on `uni-mem reindex` if corrupted
- Loaded into memory for fast queries

---

## Configuration

### User Config (`config/config.toml`)

```toml
[general]
timezone = "America/New_York"
default_limit = 10

[analyzers]
claude_enabled = true
codex_enabled = true
frequency_minutes = 60

[display]
show_source_icon = true
show_date_relative = true
colorize = true

[search]
default_fields = ["summary", "topics", "details"]
case_sensitive = false

[cli]
default_source = "all"  # "all", "claude", or "codex"
```

---

## Benefits of Unified Approach

### 1. Single Source of Truth
- All memories in one place
- No syncing needed
- No conflicts or duplicates

### 2. Cross-System Context
- See what you did in Codex when working in Claude
- See what you did in Claude when working in Codex
- Complete picture of all work

### 3. Simplified Architecture
- One storage file
- One CLI
- Simpler to understand and maintain

### 4. Easier Search
- Search everything at once
- Filter by source if needed
- See relationships across systems

### 5. Future-Proof
- Easy to add new AI systems
- Just add new analyzer
- Same unified storage

---

## Future Enhancements

### Phase 2+
- Knowledge graph across all sources
- Semantic search across everything
- AI-to-AI memory references
- Memory consolidation agents
- Importance scoring
- Automatic categorization

---

## Implementation Priority

### P0 (Must Have - Week 1)
1. Create directory structure
2. Design unified data schema
3. Build universal CLI (basic commands)
4. Build Claude analyzer
5. Build Codex analyzer
6. Migration tool

### P1 (Should Have - Week 2)
7. Session hooks for both systems
8. LaunchAgents setup
9. Basic indexing
10. Testing & verification

### P2 (Nice to Have - Week 3+)
11. Advanced search
12. Enhanced statistics
13. Timeline view
14. Topic tracking
15. Configuration system

---

## Success Criteria

- [ ] All memories in one unified location
- [ ] Both analyzers writing successfully
- [ ] CLI works from both Claude and Codex contexts
- [ ] Manual saves work with auto-detection
- [ ] Search returns results from both sources
- [ ] Session hooks load memories at startup
- [ ] LaunchAgents running hourly for both
- [ ] Existing 36 memories migrated
- [ ] Zero data loss
- [ ] Performance: <100ms for common operations

---

*Created: 2025-10-27*
*Architecture: Unified Single Storage*
*Version: 2.0.0*
