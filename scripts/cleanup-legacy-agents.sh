#!/bin/bash
# Universal AI Memory - Legacy LaunchAgent Cleanup Script
# Removes old LaunchAgents from previous memory systems

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "========================================================================"
echo "🧹 Universal AI Memory - Legacy LaunchAgent Cleanup"
echo "========================================================================"
echo ""

# Legacy agents to remove
LEGACY_AGENTS=(
    "com.claude.memory"
    "com.claude.memory.analyzer"
    "com.codex.memory"
    "com.codex.memory.analyzer"
)

REMOVED=0
NOT_FOUND=0

for agent in "${LEGACY_AGENTS[@]}"; do
    PLIST_FILE="$HOME/Library/LaunchAgents/${agent}.plist"

    if [ -f "$PLIST_FILE" ]; then
        echo "🔍 Found legacy agent: $agent"

        # Try to unload it first
        echo "   Unloading..."
        launchctl bootout gui/$(id -u)/$agent 2>/dev/null || true

        # Remove the plist file
        echo "   Removing plist file..."
        rm -f "$PLIST_FILE"

        echo -e "   ${GREEN}✓${NC} Removed $agent"
        REMOVED=$((REMOVED + 1))
    else
        NOT_FOUND=$((NOT_FOUND + 1))
    fi
done

echo ""
echo "========================================================================"
echo "Summary:"
echo "  Removed: $REMOVED legacy agent(s)"
echo "  Not found: $NOT_FOUND"
echo "========================================================================"
echo ""

if [ $REMOVED -gt 0 ]; then
    echo -e "${GREEN}✅ Cleanup complete!${NC}"
    echo ""
    echo "Current Universal Memory agents:"
    launchctl list | grep "universal.memory" || echo "  (None loaded - run setup-launchagents.sh)"
else
    echo -e "${GREEN}✅ No legacy agents found.${NC}"
    echo "Your system is clean!"
fi

echo ""
