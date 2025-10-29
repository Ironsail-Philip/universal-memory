#!/usr/bin/env python3
"""
Universal Memory - Shared Analyzer Logic
Shared utilities for all AI system analyzers
"""

import json
import fcntl
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import uuid

# Paths
MEMORY_FILE = Path.home() / ".universal-memory" / "memories.jsonl"
INDEX_DIR = Path.home() / ".universal-memory" / "index"

# Stop words for topic extraction (expanded list)
STOP_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
    'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
    'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
    'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
    'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
    'is', 'was', 'are', 'been', 'has', 'had', 'were', 'did', 'done', 'does',
    'am', 'being', 'having', 'doing', 'makes', 'made', 'making',
    # Claude Code specific common words
    'claude', 'code', 'using', 'use', 'used', 'create', 'update', 'need', 'should',
    'please', 'thanks', 'sure', 'okay', 'yes', 'no', 'ive', 'im', 'youre', 'lets',
    # Sentence-starting words
    'discussed', 'created', 'updated', 'configured', 'analyzed', 'built', 'fixed',
    'improved', 'added', 'removed', 'changed', 'modified', 'implemented', 'installed'
}


def extract_topics(text: str, max_topics: int = 10) -> List[str]:
    """
    Extract important topics from text

    Args:
        text: Text to analyze
        max_topics: Maximum number of topics to return

    Returns:
        List of topic strings
    """
    if not text:
        return []

    # Clean text
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)

    # Extract potential topics (words 3+ chars)
    words = re.findall(r'\b[a-z0-9_-]{3,}\b', text)

    # Count word frequency
    word_counts = {}
    for word in words:
        if word not in STOP_WORDS:
            word_counts[word] = word_counts.get(word, 0) + 1

    # Sort by frequency
    topics = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Return top N unique topics
    return [topic for topic, count in topics[:max_topics]]


def generate_summary(messages: List[Dict], max_length: int = 100) -> str:
    """
    Generate a one-sentence summary from messages

    Args:
        messages: List of message dictionaries
        max_length: Maximum summary length

    Returns:
        One-sentence summary
    """
    if not messages:
        return "Empty conversation"

    # Combine all text
    text_parts = []
    for msg in messages:
        if isinstance(msg.get('content'), str):
            text_parts.append(msg['content'])
        elif isinstance(msg.get('content'), list):
            for item in msg['content']:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])

    full_text = ' '.join(text_parts)[:1000]  # Limit to first 1000 chars

    # Extract topics for summary
    topics = extract_topics(full_text, max_topics=5)

    # Detect action verbs
    actions = []
    action_patterns = [
        r'\b(creat\w+)\b', r'\b(updat\w+)\b', r'\b(fix\w+)\b',
        r'\b(build\w+)\b', r'\b(implement\w+)\b', r'\b(add\w+)\b',
        r'\b(remov\w+)\b', r'\b(refactor\w+)\b', r'\b(test\w+)\b',
        r'\b(deploy\w+)\b', r'\b(configur\w+)\b', r'\b(install\w+)\b'
    ]

    for pattern in action_patterns:
        matches = re.findall(pattern, full_text.lower())
        if matches:
            actions.append(matches[0])
            break

    # Generate summary
    if actions and topics:
        action = actions[0].capitalize()
        topic_str = ', '.join(topics[:3])
        summary = f"{action} {topic_str}"
    elif topics:
        topic_str = ', '.join(topics[:3])
        summary = f"Discussion about {topic_str}"
    else:
        summary = "Conversation session"

    # Limit length
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."

    return summary


def append_to_unified_storage(entry: Dict[str, Any]) -> str:
    """
    Thread-safe append to unified memory storage

    Args:
        entry: Memory entry dictionary

    Returns:
        UUID of created entry
    """
    # Ensure required fields
    if 'id' not in entry:
        entry['id'] = str(uuid.uuid4())

    if 'timestamp' not in entry:
        entry['timestamp'] = datetime.now().isoformat()

    if 'date' not in entry:
        entry['date'] = datetime.now().strftime('%Y-%m-%d')

    # Validate required fields
    required = ['source', 'type', 'summary']
    for field in required:
        if field not in entry:
            raise ValueError(f"Missing required field: {field}")

    # Ensure directories exist
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Thread-safe append with file locking
    with open(MEMORY_FILE, 'a') as f:
        # Acquire exclusive lock
        fcntl.flock(f, fcntl.LOCK_EX)

        try:
            # Write entry
            f.write(json.dumps(entry) + '\n')
        finally:
            # Release lock (automatic on close, but explicit is better)
            fcntl.flock(f, fcntl.LOCK_UN)

    # Update indexes
    update_indexes(entry)

    return entry['id']


def update_indexes(entry: Dict[str, Any]):
    """
    Update all indexes with new entry

    Args:
        entry: Memory entry to index
    """
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    entry_id = entry.get('id')
    if not entry_id:
        return

    # Update source index
    update_source_index(entry_id, entry.get('source'))

    # Update topic index
    if 'details' in entry and 'topics' in entry['details']:
        for topic in entry['details']['topics']:
            update_topic_index(entry_id, topic)

    # Update date index
    update_date_index(entry_id, entry.get('date'))


def update_source_index(entry_id: str, source: str):
    """Update by-source index"""
    index_file = INDEX_DIR / "by-source.json"

    # Load existing index
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)
    else:
        index = {}

    # Add entry
    if source not in index:
        index[source] = []
    if entry_id not in index[source]:
        index[source].append(entry_id)

    # Save index
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)


def update_topic_index(entry_id: str, topic: str):
    """Update by-topic index"""
    index_file = INDEX_DIR / "by-topic.json"

    # Load existing index
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)
    else:
        index = {}

    # Add entry
    if topic not in index:
        index[topic] = []
    if entry_id not in index[topic]:
        index[topic].append(entry_id)

    # Save index
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)


def update_date_index(entry_id: str, date: str):
    """Update by-date index"""
    index_file = INDEX_DIR / "by-date.json"

    # Load existing index
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)
    else:
        index = {}

    # Add entry
    if date not in index:
        index[date] = []
    if entry_id not in index[date]:
        index[date].append(entry_id)

    # Save index
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)


def read_memories(limit: int = None, source: str = None, date: str = None) -> List[Dict]:
    """
    Read memories from unified storage

    Args:
        limit: Maximum number of entries to return (most recent first)
        source: Filter by source (claude, codex, etc.)
        date: Filter by date (YYYY-MM-DD)

    Returns:
        List of memory entries
    """
    if not MEMORY_FILE.exists():
        return []

    memories = []

    with open(MEMORY_FILE, 'r') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)

                # Apply filters
                if source and entry.get('source') != source:
                    continue
                if date and entry.get('date') != date:
                    continue

                memories.append(entry)

    # Sort by timestamp (most recent first)
    memories.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    # Apply limit
    if limit:
        memories = memories[:limit]

    return memories


def search_memories(query: str, source: str = None) -> List[Dict]:
    """
    Search memories by keyword

    Args:
        query: Search query
        source: Filter by source

    Returns:
        List of matching memory entries
    """
    if not MEMORY_FILE.exists():
        return []

    query_lower = query.lower()
    matches = []

    with open(MEMORY_FILE, 'r') as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)

                # Apply source filter
                if source and entry.get('source') != source:
                    continue

                # Search in summary, topics, and details
                searchable = json.dumps(entry).lower()
                if query_lower in searchable:
                    matches.append(entry)

    # Sort by timestamp (most recent first)
    matches.sort(key=lambda x: x.get('timestamp', ''), reverse=True)

    return matches


if __name__ == "__main__":
    # Test functions
    print("Testing unified memory common utilities...")

    # Test topic extraction
    test_text = "We implemented OAuth authentication using JWT tokens for the API"
    topics = extract_topics(test_text)
    print(f"Topics: {topics}")

    # Test summary generation
    test_messages = [
        {"role": "user", "content": "Help me add authentication"},
        {"role": "assistant", "content": "I'll help you implement OAuth authentication"}
    ]
    summary = generate_summary(test_messages)
    print(f"Summary: {summary}")

    print("✓ Tests passed!")
