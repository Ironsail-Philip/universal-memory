#!/bin/bash
# Universal AI Memory - LaunchAgent Setup Helper
# Loads LaunchAgents for automatic hourly extraction
# Run this manually if the installer bootstrap failed

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "========================================================================"
echo "⏰ Universal AI Memory - LaunchAgent Setup"
echo "========================================================================"
echo ""

# Check if plist files exist
CLAUDE_PLIST="$HOME/Library/LaunchAgents/com.universal.memory.claude.plist"
CODEX_PLIST="$HOME/Library/LaunchAgents/com.universal.memory.codex.plist"

if [ ! -f "$CLAUDE_PLIST" ] || [ ! -f "$CODEX_PLIST" ]; then
    echo -e "${RED}✗${NC} LaunchAgent plist files not found."
    echo ""
    echo "Expected files:"
    echo "  $CLAUDE_PLIST"
    echo "  $CODEX_PLIST"
    echo ""
    echo "Please run the installer first: ./install.sh"
    exit 1
fi

echo "Found LaunchAgent plist files:"
echo "  ✓ $(basename $CLAUDE_PLIST)"
echo "  ✓ $(basename $CODEX_PLIST)"
echo ""

# Unload existing agents (if any)
echo "Unloading any existing agents..."
launchctl bootout gui/$(id -u)/com.universal.memory.claude 2>/dev/null || true
launchctl bootout gui/$(id -u)/com.universal.memory.codex 2>/dev/null || true
echo ""

# Load LaunchAgents
echo "Loading LaunchAgents..."

if launchctl bootstrap gui/$(id -u) "$CLAUDE_PLIST" 2>&1; then
    echo -e "${GREEN}✓${NC} Claude analyzer loaded"
else
    echo -e "${RED}✗${NC} Claude analyzer failed to load"
    exit 1
fi

if launchctl bootstrap gui/$(id -u) "$CODEX_PLIST" 2>&1; then
    echo -e "${GREEN}✓${NC} Codex analyzer loaded"
else
    echo -e "${RED}✗${NC} Codex analyzer failed to load"
    exit 1
fi

echo ""
echo "========================================================================"
echo -e "${GREEN}✅ LaunchAgents successfully loaded!${NC}"
echo "========================================================================"
echo ""
echo "Automatic extraction is now enabled:"
echo "  • Claude conversations extracted hourly"
echo "  • Codex sessions extracted hourly"
echo ""
echo "Verify with:"
echo "  launchctl list | grep universal.memory"
echo ""
echo "View logs:"
echo "  tail -f ~/.universal-memory/logs/launchd-claude-stdout.log"
echo "  tail -f ~/.universal-memory/logs/launchd-codex-stdout.log"
echo ""
