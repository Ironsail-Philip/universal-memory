#!/usr/bin/env python3
"""
Claude Code Analyzer
Reads Claude Code conversations and writes to unified memory
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import hashlib

# Import shared utilities
import common

# Paths
CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"
PROCESSED_LOG = Path.home() / ".universal-memory" / "sessions" / "claude-processed.log"
ANALYZER_LOG = Path.home() / ".universal-memory" / "logs" / "claude-analyzer.log"


def log(message):
    """Log to analyzer log file"""
    ANALYZER_LOG.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    with open(ANALYZER_LOG, 'a') as f:
        f.write(log_entry)

    print(log_entry.strip())


def get_processed_conversations():
    """Load list of already processed conversation IDs"""
    if not PROCESSED_LOG.exists():
        return set()

    with open(PROCESSED_LOG, 'r') as f:
        return set(line.strip() for line in f if line.strip())


def mark_processed(conv_id):
    """Mark conversation as processed"""
    PROCESSED_LOG.parent.mkdir(parents=True, exist_ok=True)

    with open(PROCESSED_LOG, 'a') as f:
        f.write(f"{conv_id}\n")


def find_claude_conversations():
    """Find all Claude Code conversation files"""
    if not CLAUDE_PROJECTS_DIR.exists():
        log(f"Claude projects directory not found: {CLAUDE_PROJECTS_DIR}")
        return []

    conversations = []

    # Find all conversation JSONL files (stored directly in project folders)
    # Pattern: ~/.claude/projects/*/UUID.jsonl
    for conv_file in CLAUDE_PROJECTS_DIR.rglob("*.jsonl"):
        conversations.append(conv_file)

    return sorted(conversations, key=lambda p: p.stat().st_mtime)


def parse_claude_conversation(conv_path):
    """Parse Claude Code conversation file"""
    messages = []

    try:
        with open(conv_path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        msg = json.loads(line)
                        messages.append(msg)
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        log(f"Error reading {conv_path}: {e}")
        return None

    return messages


def extract_claude_metadata(messages, conv_path):
    """Extract metadata from Claude conversation"""
    metadata = {
        'topics': [],
        'message_count': len(messages),
        'conversation_id': conv_path.stem,
        'files_modified': [],
        'project': conv_path.parent.parent.name
    }

    # Extract topics from all messages
    # Claude format: {type: 'user'/'assistant', message: {role, content}}
    all_text = []
    for msg in messages:
        msg_type = msg.get('type', '')
        if msg_type not in ['user', 'assistant']:
            continue

        # Get nested message object
        nested_msg = msg.get('message', {})
        content = nested_msg.get('content', '')

        # Handle user messages (simple string)
        if msg_type == 'user':
            if isinstance(content, str):
                all_text.append(content)

        # Handle assistant messages (array of content blocks)
        elif msg_type == 'assistant':
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        # Text blocks
                        if item.get('type') == 'text' and 'text' in item:
                            all_text.append(item['text'])

                        # Tool use blocks - extract file paths
                        elif item.get('type') == 'tool_use':
                            input_params = item.get('input', {})
                            if 'file_path' in input_params:
                                file_path = input_params['file_path']
                                if file_path and file_path not in metadata['files_modified']:
                                    metadata['files_modified'].append(Path(file_path).name)

    # Generate topics from combined text
    combined_text = ' '.join(all_text[:5000])  # Limit to first 5000 chars
    metadata['topics'] = common.extract_topics(combined_text)

    return metadata


def should_skip_conversation(messages):
    """Determine if conversation should be skipped"""
    # Skip very short conversations
    if len(messages) < 5:
        return True

    # Skip if no user messages
    # Claude format: {type: 'user', message: {role: 'user', content: '...'}}
    user_messages = [m for m in messages if m.get('type') == 'user']
    if not user_messages:
        return True

    # Skip if no assistant messages
    assistant_messages = [m for m in messages if m.get('type') == 'assistant']
    if not assistant_messages:
        return True

    return False


def process_claude_conversations():
    """Process all new Claude conversations"""
    log("Starting Claude conversation analysis...")

    # Get processed conversations
    processed = get_processed_conversations()
    log(f"Already processed: {len(processed)} conversations")

    # Find all conversations
    conversations = find_claude_conversations()
    log(f"Found {len(conversations)} total conversations")

    # Process new ones
    new_count = 0
    skipped_count = 0

    for conv_path in conversations:
        # Generate conversation ID
        conv_id = f"claude:{conv_path.stem}"

        if conv_id in processed:
            continue

        # Parse conversation
        messages = parse_claude_conversation(conv_path)

        if messages is None:
            log(f"Skipping {conv_path.name}: parse error")
            mark_processed(conv_id)
            skipped_count += 1
            continue

        # Skip if too short or not meaningful
        if should_skip_conversation(messages):
            log(f"Skipping {conv_path.name}: too short or no user messages")
            mark_processed(conv_id)
            skipped_count += 1
            continue

        # Extract metadata
        metadata = extract_claude_metadata(messages, conv_path)

        # Generate summary
        summary = common.generate_summary(messages)

        # Create entry
        entry = {
            'source': 'claude',
            'type': 'auto',
            'summary': summary,
            'details': metadata
        }

        # Save to unified storage
        try:
            entry_id = common.append_to_unified_storage(entry)
            log(f"Saved: {summary[:50]}... (ID: {entry_id})")
            new_count += 1
        except Exception as e:
            log(f"Error saving entry: {e}")
            continue

        # Mark as processed
        mark_processed(conv_id)

    log(f"Analysis complete: {new_count} new entries, {skipped_count} skipped")
    return new_count


def main():
    """Main entry point"""
    try:
        count = process_claude_conversations()
        sys.exit(0 if count >= 0 else 1)
    except Exception as e:
        log(f"Fatal error: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
