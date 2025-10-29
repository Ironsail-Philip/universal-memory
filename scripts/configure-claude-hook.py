#!/usr/bin/env python3
"""
Configure Claude Code session start hook for Universal Memory.

Updates Claude's settings to ensure our SessionStart hook is present.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import shutil


def ensure_session_start_hook(data, command_path):
    """Ensure the SessionStart hook includes the Universal Memory command."""
    hooks = data.setdefault("hooks", {})
    session_start = hooks.setdefault("SessionStart", [])
    if not isinstance(session_start, list):
        session_start = hooks["SessionStart"] = []

    for block in session_start:
        if not isinstance(block, dict):
            continue
        for hook in block.get("hooks", []):
            if (
                isinstance(hook, dict)
                and hook.get("type") == "command"
                and hook.get("command") == command_path
            ):
                return False

    session_start.append(
        {
            "matchers": ["startup", "resume"],
            "hooks": [
                {
                    "type": "command",
                    "command": command_path,
                }
            ],
        }
    )
    return True


def create_backup(settings_path: Path) -> Path:
    """Create a timestamped backup of the settings file."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = settings_path.with_suffix(
        settings_path.suffix + f".unimem-backup-{timestamp}"
    )
    shutil.copy2(settings_path, backup_path)
    return backup_path


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: configure-claude-hook.py <settings-path> <command-path>",
            file=sys.stderr,
        )
        return 1

    settings_path = Path(sys.argv[1]).expanduser()
    command_path = sys.argv[2]

    if not settings_path.exists():
        return 0

    try:
        data = json.loads(settings_path.read_text())
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Unable to parse {settings_path}: {exc}", file=sys.stderr)
        return 1

    changed = ensure_session_start_hook(data, command_path)
    if not changed:
        return 0

    try:
        backup_path = create_backup(settings_path)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Failed to create backup for {settings_path}: {exc}", file=sys.stderr)
        return 1

    try:
        settings_path.write_text(json.dumps(data, indent=2) + "\n")
    except Exception as exc:  # pylint: disable=broad-except
        print(
            f"Failed to write updated settings to {settings_path}: {exc}",
            file=sys.stderr,
        )
        print(f"Backup preserved at: {backup_path}", file=sys.stderr)
        return 1

    print(f"Claude settings updated. Backup created at: {backup_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
