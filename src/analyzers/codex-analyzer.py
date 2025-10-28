#!/usr/bin/env python3
"""
Codex CLI Analyzer
Reads Codex CLI sessions and writes to unified memory
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Import shared utilities
import common

# Paths
CODEX_SESSIONS_DIR = Path.home() / ".codex" / "sessions"
PROCESSED_LOG = Path.home() / ".universal-memory" / "sessions" / "codex-processed.log"
ANALYZER_LOG = Path.home() / ".universal-memory" / "logs" / "codex-analyzer.log"


def log(message):
    """Log to analyzer log file"""
    ANALYZER_LOG.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    with open(ANALYZER_LOG, 'a') as f:
        f.write(log_entry)

    print(log_entry.strip())


def get_processed_sessions():
    """Load list of already processed session IDs"""
    if not PROCESSED_LOG.exists():
        return set()

    with open(PROCESSED_LOG, 'r') as f:
        return set(line.strip() for line in f if line.strip())


def mark_processed(session_id):
    """Mark session as processed"""
    PROCESSED_LOG.parent.mkdir(parents=True, exist_ok=True)

    with open(PROCESSED_LOG, 'a') as f:
        f.write(f"{session_id}\n")


def find_codex_sessions():
    """Find all Codex session files"""
    if not CODEX_SESSIONS_DIR.exists():
        log(f"Codex sessions directory not found: {CODEX_SESSIONS_DIR}")
        return []

    sessions = []

    # Find all session JSONL files
    # Pattern: ~/.codex/sessions/YYYY/MM/DD/*.jsonl
    for session_file in CODEX_SESSIONS_DIR.rglob("*.jsonl"):
        sessions.append(session_file)

    return sorted(sessions, key=lambda p: p.stat().st_mtime)


def parse_codex_session(session_path):
    """Parse Codex session file"""
    events = []

    try:
        with open(session_path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        log(f"Error reading {session_path}: {e}")
        return None

    return events


def extract_codex_metadata(events, session_path):
    """Extract metadata from Codex session"""
    metadata = {
        'topics': [],
        'message_count': 0,
        'session_id': session_path.stem,
        'files_modified': []
    }

    # Extract text from all messages
    all_text = []

    for event in events:
        event_type = event.get('type', '')

        # Response items contain the actual messages
        if event_type == 'response_item':
            payload = event.get('payload', {})

            if isinstance(payload, dict):
                role = payload.get('role', '')
                content = payload.get('content', [])

                # Count messages
                if role in ['user', 'assistant']:
                    metadata['message_count'] += 1

                # Extract text from content
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            # User input
                            if item.get('type') == 'input_text':
                                text = item.get('text', '')
                                if text:
                                    all_text.append(text)

                            # Assistant output
                            elif item.get('type') == 'output_text':
                                text = item.get('text', '')
                                if text:
                                    all_text.append(text)

        # Event messages may contain additional context
        elif event_type == 'event_msg':
            payload = event.get('payload', {})
            if isinstance(payload, dict):
                text = payload.get('text', '')
                if text:
                    all_text.append(text)

        # Tool use events - extract file paths
        elif event_type == 'tool_use':
            payload = event.get('payload', {})
            if isinstance(payload, dict):
                tool_name = payload.get('name', '')
                params = payload.get('params', {})

                # File operations
                if 'file_path' in params:
                    file_path = params['file_path']
                    if file_path and file_path not in metadata['files_modified']:
                        metadata['files_modified'].append(Path(file_path).name)
                elif 'path' in params:
                    file_path = params['path']
                    if file_path and file_path not in metadata['files_modified']:
                        metadata['files_modified'].append(Path(file_path).name)

    # Generate topics from combined text
    combined_text = ' '.join(all_text[:5000])  # Limit to first 5000 chars
    metadata['topics'] = common.extract_topics(combined_text)

    return metadata


def should_skip_session(events):
    """Determine if session should be skipped"""
    # Skip very short sessions
    if len(events) < 5:
        return True

    # Extract messages
    messages = []
    for event in events:
        if event.get('type') == 'response_item':
            payload = event.get('payload', {})
            if payload.get('role') in ['user', 'assistant']:
                messages.append(payload)

    # Skip if too few messages
    if len(messages) < 3:
        return True

    # Skip if no user messages
    user_messages = [m for m in messages if m.get('role') == 'user']
    if not user_messages:
        return True

    # Skip if no assistant messages
    assistant_messages = [m for m in messages if m.get('role') == 'assistant']
    if not assistant_messages:
        return True

    return False


def generate_codex_summary(events):
    """Generate summary from Codex session events"""
    # Extract message-like structure for summary generation
    messages = []

    for event in events:
        if event.get('type') == 'response_item':
            payload = event.get('payload', {})
            role = payload.get('role', '')

            if role in ['user', 'assistant']:
                # Convert to format expected by common.generate_summary
                content_parts = []
                for item in payload.get('content', []):
                    if isinstance(item, dict):
                        if 'text' in item:
                            content_parts.append(item['text'])

                if content_parts:
                    messages.append({
                        'role': role,
                        'content': ' '.join(content_parts)
                    })

    # Use common summary generator
    if messages:
        return common.generate_summary(messages)
    else:
        return "Codex session"


def process_codex_sessions():
    """Process all new Codex sessions"""
    log("Starting Codex session analysis...")

    # Get processed sessions
    processed = get_processed_sessions()
    log(f"Already processed: {len(processed)} sessions")

    # Find all sessions
    sessions = find_codex_sessions()
    log(f"Found {len(sessions)} total sessions")

    # Process new ones
    new_count = 0
    skipped_count = 0

    for session_path in sessions:
        # Generate session ID
        session_id = f"codex:{session_path.stem}"

        if session_id in processed:
            continue

        # Parse session
        events = parse_codex_session(session_path)

        if events is None:
            log(f"Skipping {session_path.name}: parse error")
            mark_processed(session_id)
            skipped_count += 1
            continue

        # Skip if too short or not meaningful
        if should_skip_session(events):
            log(f"Skipping {session_path.name}: too short or no messages")
            mark_processed(session_id)
            skipped_count += 1
            continue

        # Extract metadata
        metadata = extract_codex_metadata(events, session_path)

        # Generate summary
        summary = generate_codex_summary(events)

        # Create entry
        entry = {
            'source': 'codex',
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
        mark_processed(session_id)

    log(f"Analysis complete: {new_count} new entries, {skipped_count} skipped")
    return new_count


def main():
    """Main entry point"""
    try:
        count = process_codex_sessions()
        sys.exit(0 if count >= 0 else 1)
    except Exception as e:
        log(f"Fatal error: {e}")
        import traceback
        log(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
