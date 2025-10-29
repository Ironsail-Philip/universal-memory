# LLM Memory System Instructions

**For:** AI Coding Assistants (Claude Code, Codex, etc.)
**Version:** 3.0.0 (RAG-Enabled)
**Purpose:** Teach LLMs how to use the Universal AI Memory system

---

## Overview

You have access to a **RAG-based memory system** with two tiers:
- **Short-Term Memory (STM):** Shown at session start
- **Long-Term Memory (LTM):** Available via `uni-mem` commands

This is **your memory**, not just the user's. Use it actively to provide better assistance.

---

## 1. Short-Term Memory (STM)

### What You See at Session Start

At the beginning of each session, you receive a memory infusion like this:

```
════════════════════════════════════════════════════════════════
📚 SHORT-TERM MEMORY (STM) - Recent Context
   20 entries across all AI systems
════════════════════════════════════════════════════════════════

🔵 🤖 2025-10-29: Working on RAG architecture [mem:a8380efc]
🟢 🤖 2025-10-29: Fixed initialization bug [mem:e4c016f0]
🔵 ✍️ 2025-10-28: Decided to use embeddings [mem:6250c57e]
...
```

### What This Means

- **🔵** = Work done in Claude Code
- **🟢** = Work done in Codex CLI
- **⚪** = Manual saves or unified system
- **🤖** = Automatically extracted
- **✍️** = User explicitly saved
- **[mem:abc12345]** = Memory ID for reference

### How to Use STM

1. **Read it carefully** at session start
2. **Reference relevant memories** when appropriate
3. **Build on previous work** instead of starting from scratch
4. **Ask the user** if you need clarification on any memory

### Example STM Usage

```
User: "Let's add authentication to the app"

You: "I see we've worked on authentication before. In memory
     [mem:6250c57e] from 2025-10-15, we implemented OAuth with
     JWT tokens. Should we continue with that approach or start
     fresh?"
```

---

## 2. Long-Term Memory (LTM)

### What's Available

You have access to **164+ historical memories** going back to 2025-10-09. These memories contain:
- All work across Claude Code and Codex CLI
- Topics, files modified, git commits
- User's manual notes and decisions
- Indexed by topic, date, source, and associations

### When to Query LTM

Query long-term memory when:
- User asks "have we done this before?"
- Starting work that might build on past work
- User mentions a topic you want context on
- You need to find related files or approaches
- You want to avoid duplicating work
- User asks about project history

### How to Query LTM

Use the `uni-mem` command via Bash tool:

```bash
# Search for keyword
uni-mem search "authentication"

# Show all memories about a topic
uni-mem topics "pharmacy"

# See only Claude Code work
uni-mem show --claude

# See only Codex work
uni-mem show --codex

# Timeline view of this week
uni-mem timeline --week

# Show recent manual saves
uni-mem show --manual
```

### Example LTM Query

```
User: "How did we handle error logging in the API?"

You: "Let me check our memory..."

[Runs: uni-mem search "error logging API"]

You: "Found it! In memory [mem:abc123] from 2025-10-12, we
     implemented centralized error logging using Winston. The
     setup is in src/utils/logger.ts. Would you like me to review
     that approach or modify it?"
```

---

## 3. Memory-Aware Behavior Guidelines

### DO: Proactively Check Memory

✅ **Good:**
```
User: "Let's add a payment gateway"

You: "Before we start, let me check if we've discussed payment
     systems before..."

[Searches: uni-mem search "payment"]

"I don't see any prior work on payments. Let's discuss which
gateway you prefer - Stripe, PayPal, or something else?"
```

❌ **Bad:**
```
User: "Let's add a payment gateway"

You: "Sure! Let's use Stripe. Here's how to set it up..."
[Starts from scratch without checking memory]
```

### DO: Reference Memory IDs

When building on previous work, reference the memory ID:

✅ **Good:**
```
"Based on the architecture decision in [mem:6250c57e], I'll
continue using the microservices pattern we established."
```

❌ **Bad:**
```
"Based on what we did before, I'll use microservices."
[Vague, no specific reference]
```

### DO: Acknowledge Cross-System Work

You can see work from other AI systems. Acknowledge it:

✅ **Good:**
```
"I see you worked on this feature in Codex yesterday [mem:e4c016f0].
Let me continue from where that left off."
```

### DO: Save Important Decisions

When the user makes a key decision, suggest saving it:

✅ **Good:**
```
User: "Let's use PostgreSQL instead of MongoDB"

You: "Great choice! This is an important architectural decision.
     Would you like me to save it to memory?"

[If yes: uni-mem save "Decided to use PostgreSQL over MongoDB
for ACID compliance and relational data model"
--tags "architecture,database,decision"]
```

### DON'T: Ignore Memory

❌ **Bad:**
```
User: "Can you add authentication?"

You: "Sure! Let me implement OAuth from scratch..."
[Ignores that authentication was already implemented in mem:abc123]
```

### DON'T: Over-Query

❌ **Bad:**
```
[Searches memory before every single response]
[User asks about weather - still searches memory]
```

Use judgment. Query when relevant to the task.

---

## 4. Memory Query Patterns

### Pattern 1: Check Before Building

```bash
# User wants to add feature X
# FIRST: Check if X was discussed before
uni-mem search "feature X"

# If found: Reference and build on it
# If not found: Start fresh with confidence
```

### Pattern 2: Find Related Work

```bash
# User asks about file Y
# Find all work related to that file
uni-mem search "Y.ts"

# Or find all work in same project
uni-mem search "project-name"
```

### Pattern 3: Understand Context

```bash
# User resumes work from days ago
# Check recent timeline
uni-mem timeline --week

# Or check specific topic
uni-mem topics "authentication"
```

### Pattern 4: Cross-System Continuity

```bash
# User switches from Codex to Claude
# STM already shows recent Codex work
# Reference it naturally:
"I see you were working on this in Codex yesterday [mem:xyz]..."
```

---

## 5. Memory Commands Reference

### Search

```bash
# Basic search
uni-mem search "keyword"

# Search with source filter
uni-mem search "auth" --claude    # Only Claude work
uni-mem search "bug" --codex      # Only Codex work
uni-mem search "decision" --manual # Only manual saves
```

### Show

```bash
# Show recent entries
uni-mem show            # Last 10
uni-mem show 20         # Last 20

# Show with filters
uni-mem show --claude   # Claude only
uni-mem show --codex    # Codex only
uni-mem show --manual   # Manual saves only
```

### Topics

```bash
# List all topics
uni-mem topics

# Show entries for specific topic
uni-mem topics "authentication"
uni-mem topics "pharmacy"
```

### Timeline

```bash
# Chronological view
uni-mem timeline              # All time
uni-mem timeline --week       # This week
uni-mem timeline --date 2025-10-27  # Specific date
```

### Stats

```bash
# System statistics
uni-mem stats              # Overall stats
uni-mem stats --breakdown  # Detailed breakdown
```

### Save

```bash
# Save important information
uni-mem save "Summary of decision or work"

# Save with metadata
uni-mem save "Important architectural choice" \
  '{"project": "app", "priority": "high"}' \
  --tags "architecture,decision"
```

---

## 6. Example Conversation Flows

### Example 1: Building on Past Work

```
User: "Let's improve the authentication system"

You: "Let me check what we've built so far..."

[Runs: uni-mem search "authentication"]

You: "I found our auth implementation from 2025-10-15
     [mem:6250c57e]. We're using OAuth with JWT tokens,
     implemented in src/auth/oauth.ts. What specifically
     would you like to improve - security, UX, or performance?"
```

### Example 2: Avoiding Duplicate Work

```
User: "Can you create a database schema for users?"

You: "Let me first check if we've already designed this..."

[Runs: uni-mem search "database schema users"]

You: "Found it! We already created a user schema in [mem:abc123]
     on 2025-10-10. It includes email, password_hash, created_at,
     and role fields. Would you like me to show you that schema
     or modify it?"
```

### Example 3: Cross-System Awareness

```
STM shows:
🟢 🤖 2025-10-28: Set up Express server [mem:def456]

User: "Can you help me add routes to the API?"

You: "I see you set up the Express server in Codex yesterday
     [mem:def456]. I'll add routes that integrate with that
     existing setup. What endpoints do you need?"
```

### Example 4: Saving Decisions

```
User: "After thinking about it, let's go with microservices
      architecture instead of monolith"

You: "That's a significant architectural decision. Let me save
     it to memory so we don't lose this context."

[Runs: uni-mem save "Decided on microservices architecture
instead of monolith for better scalability and team autonomy"
--tags "architecture,decision,microservices"]

You: "Saved! This will help maintain consistency as we build.
     Should we start by defining service boundaries?"
```

---

## 7. Best Practices Summary

### ✅ DO

1. **Check memory before starting new work**
2. **Reference memory IDs when building on past work**
3. **Acknowledge cross-system work (Codex ↔ Claude)**
4. **Suggest saving important decisions**
5. **Use memory to provide context-aware suggestions**
6. **Query LTM when user asks "have we done this?"**

### ❌ DON'T

1. **Start from scratch without checking memory**
2. **Ignore work done in other AI systems**
3. **Make vague references ("we did this before")**
4. **Over-query memory for irrelevant tasks**
5. **Forget to save critical architectural decisions**

---

## 8. Memory System Capabilities

### What Memory Knows

- ✅ All code files you've modified
- ✅ Git commits you've made
- ✅ Topics you've discussed
- ✅ Decisions you've made
- ✅ Features you've implemented
- ✅ Bugs you've fixed
- ✅ Work across all AI systems

### What Memory Doesn't Know

- ❌ Future plans (unless user saved them)
- ❌ External documentation changes
- ❌ User's thoughts not discussed
- ❌ Work done outside AI sessions

---

## 9. Integration with Your Workflow

### At Session Start

1. **Read STM display** (20 recent memories)
2. **Note relevant context** for current work
3. **Be ready to reference** memories when appropriate

### During Conversation

1. **When user asks to build something:**
   - Check: `uni-mem search "<topic>"`
   - Reference past work if found

2. **When user asks "have we done X?":**
   - Query: `uni-mem search "X"`
   - Provide specific memories with IDs

3. **When completing major work:**
   - Suggest: "Should I save this to memory?"
   - Use: `uni-mem save "..."`

### End of Session

- Memory is saved automatically by analyzers
- Manual saves (if any) persist immediately
- Next session will have this work in STM

---

## 10. Your Role in the RAG System

You are **part of the memory system**, not just a user of it.

**Traditional System:**
```
User → Asks Question → You → Answer (from training data)
```

**RAG System (You):**
```
User → Asks Question → You → Check Memory → Answer (from memory + training)
                                    ↓
                              Save Decision → Memory
```

You are responsible for:
- **Retrieving** relevant memories
- **Referencing** past work
- **Suggesting** memory saves
- **Building continuity** across sessions and systems

---

## 11. Success Metrics

You're using memory effectively when:

- ✅ Users say "wow, you remembered that!"
- ✅ You reference specific memory IDs naturally
- ✅ You build on work from previous sessions
- ✅ You acknowledge cross-system work (Claude ↔ Codex)
- ✅ You avoid duplicate implementation
- ✅ You provide context-aware suggestions

---

## 12. Quick Reference Card

```
╔══════════════════════════════════════════════════════════╗
║  LLM Memory Quick Reference                              ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  AT SESSION START:                                       ║
║  • Read STM (20 recent memories shown)                   ║
║  • Note relevant context                                 ║
║                                                          ║
║  WHEN TO QUERY:                                          ║
║  • User asks "have we done this?"                        ║
║  • Starting work that might exist                        ║
║  • Need context on a topic                               ║
║                                                          ║
║  HOW TO QUERY:                                           ║
║  • uni-mem search "keyword"                              ║
║  • uni-mem topics "topic"                                ║
║  • uni-mem show --claude                                 ║
║                                                          ║
║  BEST PRACTICE:                                          ║
║  • Check before building                                 ║
║  • Reference memory IDs                                  ║
║  • Save important decisions                              ║
║  • Build on cross-system work                            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

**Remember: You are memory-aware. Use it to provide better, more continuous assistance across all sessions and AI systems.**

---

*Version: 3.0.0 RAG-Enabled*
*Updated: 2025-10-29*
