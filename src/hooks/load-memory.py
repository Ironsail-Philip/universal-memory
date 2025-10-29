#!/usr/bin/env python3
"""
Universal Memory Loader
Loads and displays recent memories at session startup
Works for both Claude Code and Codex
"""

import sys
import argparse
import time
from pathlib import Path

# Add analyzers to path for imports
sys.path.insert(0, str(Path.home() / ".universal-memory" / "analyzers"))
import common


def format_memory_display(entries, show_details=False):
    """Format memories for display with RAG-aware context"""
    if not entries:
        return "No recent memories found."

    # Icons
    source_icons = {
        'claude': '🔵',
        'codex': '🟢',
        'unified': '⚪'
    }
    type_icons = {
        'manual': '✍️',
        'auto': '🤖'
    }

    lines = []
    lines.append("\n" + "=" * 70)
    lines.append(f"📚 SHORT-TERM MEMORY (STM) - Recent Context")
    lines.append(f"   {len(entries)} entries across all AI systems")
    lines.append("=" * 70 + "\n")

    for i, entry in enumerate(entries, 1):
        source = entry.get('source', 'unknown')
        type_ = entry.get('type', 'unknown')
        date = entry.get('date', 'Unknown')
        summary = entry.get('summary', 'No summary')
        memory_id = entry.get('id', 'unknown')[:8]  # Show first 8 chars of UUID

        source_icon = source_icons.get(source, '⚪')
        type_icon = type_icons.get(type_, '🤖')

        # Basic display with memory ID for reference
        line = f"{source_icon} {type_icon} {date}: {summary} [mem:{memory_id}]"
        lines.append(line)

        # Show details if requested
        if show_details:
            details = entry.get('details', {})
            topics = details.get('topics', [])
            if topics:
                lines.append(f"   Topics: {', '.join(topics[:5])}")
            files = details.get('files_modified', [])
            if files:
                lines.append(f"   Files: {', '.join(files[:3])}")
            lines.append("")

    lines.append("\n" + "=" * 70)
    lines.append("💡 I can search LONG-TERM MEMORY (164+ entries) with:")
    lines.append("   • uni-mem search \"<keyword>\"  - Find related work")
    lines.append("   • uni-mem topics \"<topic>\"    - Show topic history")
    lines.append("   • uni-mem show --claude       - See only Claude work")
    lines.append("\n   Ask me to check my memory before starting new work!")
    lines.append("=" * 70 + "\n")

    return "\n".join(lines)


def cleanup_old_session_locks(max_age_hours=24):
    """
    Clean up old session lock files to prevent runtime directory bloat.

    Args:
        max_age_hours: Remove lock files older than this many hours
    """
    sentinel_dir = Path.home() / ".universal-memory" / "runtime"
    if not sentinel_dir.exists():
        return

    now = time.time()
    max_age_seconds = max_age_hours * 3600

    for lock_file in sentinel_dir.glob("session-*.lock"):
        try:
            # Check file age
            if lock_file.stat().st_mtime < (now - max_age_seconds):
                lock_file.unlink()
        except OSError:
            # Ignore errors during cleanup
            pass


def should_display(session_based=True, dedupe_key="global"):
    """
    Determine if we should display memory output.

    NEW BEHAVIOR (session_based=True):
    - Track by actual session (PID + conversation ID)
    - Display once per session, not time-suppressed
    - Guaranteed infusion for every new session

    Args:
        session_based: Use session tracking (recommended)
        dedupe_key: Unique key for this AI system

    Returns:
        True if memory should be displayed
    """
    if not session_based:
        # Legacy time-based behavior (not recommended)
        return True

    sentinel_dir = Path.home() / ".universal-memory" / "runtime"
    sentinel_dir.mkdir(parents=True, exist_ok=True)

    # Clean up old locks (runs once per invocation, negligible overhead)
    cleanup_old_session_locks(max_age_hours=24)

    # Create session identifier from PID + timestamp
    # This ensures each unique session gets memory infused
    import os
    pid = os.getpid()
    session_id = f"{dedupe_key}-{pid}"
    session_file = sentinel_dir / f"session-{session_id}.lock"

    # Check if this session already received memory
    if session_file.exists():
        # Already shown for this session
        return False

    # First time for this session - create lock file
    try:
        session_file.write_text(f"{time.time()}\n{session_id}")
        return True
    except OSError:
        # If we can't write lock, show memory anyway (fail-safe)
        return True


def load_memory(source='all', limit=15, show_details=False):
    """
    Load and display recent memories

    Args:
        source: Filter by source ('all', 'claude', 'codex')
        limit: Number of recent entries to show
        show_details: Show additional details
    """
    try:
        # Read recent memories
        entries = common.read_memories(limit=limit if source == 'all' else None)

        # Filter by source if specified
        if source != 'all':
            entries = [e for e in entries if e.get('source') == source]
            entries = entries[:limit]

        # Format and display
        display = format_memory_display(entries, show_details=show_details)
        print(display)

    except Exception as e:
        print(f"⚠️  Error loading memory: {e}")
        print("   Memory system may not be initialized yet.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Load Universal AI Memory (RAG System)')
    parser.add_argument('--source', default='all',
                        choices=['all', 'claude', 'codex'],
                        help='Filter by source')
    parser.add_argument('--limit', type=int, default=15,
                        help='Number of entries to show (default: 15)')
    parser.add_argument('--details', action='store_true',
                        help='Show additional details')
    parser.add_argument('--session-key', default='global',
                        help='Unique key for session tracking (e.g., "claude", "codex")')
    parser.add_argument('--force', action='store_true',
                        help='Force display even if already shown this session')
    parser.add_argument('--legacy-time-based', action='store_true',
                        help='Use legacy time-based dedupe (not recommended)')

    args = parser.parse_args()

    # Determine if we should display
    if args.force:
        # Always show when forced
        load_memory(source=args.source, limit=args.limit, show_details=args.details)
    elif should_display(session_based=not args.legacy_time_based, dedupe_key=args.session_key):
        load_memory(source=args.source, limit=args.limit, show_details=args.details)


if __name__ == "__main__":
    main()
