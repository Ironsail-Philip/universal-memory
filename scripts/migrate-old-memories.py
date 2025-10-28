#!/usr/bin/env python3
"""
Migrate Old Memories to Unified Storage
Imports memories from old separate Claude and Codex systems
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add analyzers to path
sys.path.insert(0, str(Path.home() / ".universal-memory" / "analyzers"))
import common

# Old system paths
OLD_CLAUDE_MEMORY = Path.home() / ".claude-memory" / "conversation-summaries.jsonl"
OLD_CODEX_MEMORY = Path.home() / ".codex-memory" / "conversation-summaries.jsonl"


def migrate_from_old_system(old_file, source_system):
    """
    Migrate memories from old system to unified storage

    Args:
        old_file: Path to old memory file
        source_system: 'claude' or 'codex'

    Returns:
        Number of entries migrated
    """
    if not old_file.exists():
        print(f"⚠️  Old {source_system} memory file not found: {old_file}")
        return 0

    print(f"\n📦 Migrating {source_system} memories from old system...")
    print(f"   Source: {old_file}")

    migrated = 0
    skipped = 0

    with open(old_file, 'r') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                old_entry = json.loads(line)
            except json.JSONDecodeError:
                print(f"   ⚠️  Skipping invalid JSON line")
                skipped += 1
                continue

            # Convert old format to new unified format
            new_entry = {
                'source': source_system,
                'type': old_entry.get('type', 'auto'),
                'summary': old_entry.get('summary', 'Migrated memory'),
                'timestamp': old_entry.get('timestamp'),
                'date': old_entry.get('date'),
                'details': old_entry.get('details', {}),
                'metadata': {
                    'migrated_from': f'{source_system}-memory',
                    'original_timestamp': old_entry.get('timestamp')
                }
            }

            # Ensure details has proper structure
            if 'details' not in new_entry or not isinstance(new_entry['details'], dict):
                new_entry['details'] = {}

            # Save to unified storage
            try:
                entry_id = common.append_to_unified_storage(new_entry)
                migrated += 1

                # Show progress
                if migrated % 5 == 0:
                    print(f"   ✓ Migrated {migrated} entries...")

            except Exception as e:
                print(f"   ⚠️  Error migrating entry: {e}")
                skipped += 1
                continue

    print(f"   ✅ Complete: {migrated} migrated, {skipped} skipped")
    return migrated


def main():
    """Main migration entry point"""
    print("=" * 70)
    print("🔄 Universal Memory Migration Tool")
    print("=" * 70)
    print("\nThis will migrate memories from old separate systems to unified storage.")
    print("Old systems: ~/.claude-memory/ and ~/.codex-memory/")
    print("New unified: ~/.universal-memory/")

    # Check if old systems exist
    claude_exists = OLD_CLAUDE_MEMORY.exists()
    codex_exists = OLD_CODEX_MEMORY.exists()

    if not claude_exists and not codex_exists:
        print("\n⚠️  No old memory systems found. Nothing to migrate.")
        return

    print("\nFound old systems:")
    if claude_exists:
        with open(OLD_CLAUDE_MEMORY, 'r') as f:
            claude_count = sum(1 for line in f if line.strip())
        print(f"  🔵 Claude: {claude_count} entries")

    if codex_exists:
        with open(OLD_CODEX_MEMORY, 'r') as f:
            codex_count = sum(1 for line in f if line.strip())
        print(f"  🟢 Codex: {codex_count} entries")

    # Ask for confirmation
    print("\n⚠️  Warning: This will add these memories to unified storage.")
    print("   They will be tagged as migrated from old systems.")

    response = input("\nProceed with migration? [y/N]: ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return

    # Migrate
    total_migrated = 0

    if claude_exists:
        total_migrated += migrate_from_old_system(OLD_CLAUDE_MEMORY, 'claude')

    if codex_exists:
        total_migrated += migrate_from_old_system(OLD_CODEX_MEMORY, 'codex')

    # Show results
    print("\n" + "=" * 70)
    print(f"✅ Migration Complete!")
    print(f"   Total migrated: {total_migrated}")
    print("=" * 70)

    # Show new stats
    print("\n📊 New Unified Memory Stats:")
    memories = common.read_memories()

    by_source = {}
    for entry in memories:
        source = entry.get('source', 'unknown')
        by_source[source] = by_source.get(source, 0) + 1

    print(f"   Total entries: {len(memories)}")
    for source, count in sorted(by_source.items()):
        icon = {'claude': '🔵', 'codex': '🟢', 'unified': '⚪'}.get(source, '⚪')
        print(f"   {icon} {source}: {count}")

    print("\n💡 Tip: You can now archive the old systems:")
    if claude_exists:
        print(f"   mv ~/.claude-memory ~/.claude-memory.backup")
    if codex_exists:
        print(f"   mv ~/.codex-memory ~/.codex-memory.backup")

    print("\n✨ Use 'uni-mem show' to see all your unified memories!")


if __name__ == "__main__":
    main()
