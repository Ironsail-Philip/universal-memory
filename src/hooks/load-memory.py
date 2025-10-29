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
    """Format memories for display"""
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
    lines.append(f"📚 Universal AI Memory - Recent Context ({len(entries)} entries)")
    lines.append("=" * 70 + "\n")

    for i, entry in enumerate(entries, 1):
        source = entry.get('source', 'unknown')
        type_ = entry.get('type', 'unknown')
        date = entry.get('date', 'Unknown')
        summary = entry.get('summary', 'No summary')

        source_icon = source_icons.get(source, '⚪')
        type_icon = type_icons.get(type_, '🤖')

        # Basic display
        line = f"{source_icon} {type_icon} {date}: {summary}"
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
    lines.append("Use 'uni-mem show' for more | 'uni-mem search <keyword>' to search")
    lines.append("=" * 70 + "\n")

    return "\n".join(lines)


def should_display(dedupe_seconds=0, dedupe_key="global"):
    """Determine if we should display memory output (prevents rapid duplicates)."""
    if dedupe_seconds <= 0:
        return True

    sentinel_dir = Path.home() / ".universal-memory" / "runtime"
    sentinel_file = sentinel_dir / f"memory-display-{dedupe_key}.ts"
    now = time.time()

    try:
        if sentinel_file.exists():
            ts = float(sentinel_file.read_text().strip() or "0")
            if now - ts < dedupe_seconds:
                return False
    except (ValueError, OSError):
        # Ignore malformed sentinel and continue.
        pass

    try:
        sentinel_dir.mkdir(parents=True, exist_ok=True)
        sentinel_file.write_text(str(now))
    except OSError:
        # If we cannot write the sentinel, proceed without deduping.
        pass

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
    parser = argparse.ArgumentParser(description='Load Universal AI Memory')
    parser.add_argument('--source', default='all',
                        choices=['all', 'claude', 'codex'],
                        help='Filter by source')
    parser.add_argument('--limit', type=int, default=15,
                        help='Number of entries to show')
    parser.add_argument('--details', action='store_true',
                        help='Show additional details')
    parser.add_argument('--dedupe-seconds', type=int, default=0,
                        help='Skip display if recently shown within this window')
    parser.add_argument('--dedupe-key', default='global',
                        help='Unique key for dedupe tracking')

    args = parser.parse_args()

    if should_display(args.dedupe_seconds, args.dedupe_key):
        load_memory(source=args.source, limit=args.limit, show_details=args.details)


if __name__ == "__main__":
    main()
