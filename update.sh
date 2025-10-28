#!/bin/bash
# Universal AI Memory - Update Script
# Updates to the latest version while preserving user data

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

INSTALL_DIR="$HOME/.universal-memory"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "=================================================================="
echo "🧠 Universal AI Memory - Update"
echo "=================================================================="
echo ""

# Check if installed
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${RED}✗ Universal Memory is not installed.${NC}"
    echo ""
    echo "Please run: ./install.sh"
    echo ""
    exit 1
fi

echo "This will update Universal AI Memory to the latest version."
echo ""
echo "Your memories and configuration will be preserved."
echo ""

# Show current stats
if [ -f "$INSTALL_DIR/uni-mem" ]; then
    echo "Current installation:"
    "$INSTALL_DIR/uni-mem" stats 2>/dev/null || echo "  (stats unavailable)"
    echo ""
fi

read -p "Proceed with update? [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Update cancelled."
    exit 0
fi

echo ""
echo "📦 Updating Universal AI Memory..."

# Backup user data
echo "   Creating backup..."
BACKUP_DIR="$INSTALL_DIR/.backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
[ -f "$INSTALL_DIR/memories.jsonl" ] && cp "$INSTALL_DIR/memories.jsonl" "$BACKUP_DIR/"
[ -d "$INSTALL_DIR/logs" ] && cp -r "$INSTALL_DIR/logs" "$BACKUP_DIR/"
[ -d "$INSTALL_DIR/index" ] && cp -r "$INSTALL_DIR/index" "$BACKUP_DIR/"
[ -d "$INSTALL_DIR/sessions" ] && cp -r "$INSTALL_DIR/sessions" "$BACKUP_DIR/"
echo -e "   ${GREEN}✓${NC} Backup created at: $BACKUP_DIR"

# Update application files
echo "   Updating application files..."
cp -r "$REPO_DIR/src/analyzers/"* "$INSTALL_DIR/analyzers/"
cp -r "$REPO_DIR/src/hooks/"* "$INSTALL_DIR/hooks/"
cp "$REPO_DIR/src/cli/uni-mem" "$INSTALL_DIR/"
cp "$REPO_DIR/scripts/codex-with-memory" "$INSTALL_DIR/"
cp "$REPO_DIR/scripts/migrate-old-memories.py" "$INSTALL_DIR/"

# Update documentation
cp -r "$REPO_DIR/docs/"* "$INSTALL_DIR/" 2>/dev/null || true

echo -e "   ${GREEN}✓${NC} Application files updated"

# Set permissions
echo "   Setting permissions..."
chmod +x "$INSTALL_DIR/uni-mem"
chmod +x "$INSTALL_DIR/codex-with-memory"
chmod +x "$INSTALL_DIR/analyzers/"*.py
chmod +x "$INSTALL_DIR/hooks/"*.sh
chmod +x "$INSTALL_DIR/hooks/"*.py
chmod +x "$INSTALL_DIR/migrate-old-memories.py"
echo -e "   ${GREEN}✓${NC} Permissions set"

# Detect OS for LaunchAgent updates
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

# Update LaunchAgents if needed (macOS)
if [[ "$OS" == "macos" ]]; then
    echo "   Updating LaunchAgents..."

    # Recreate LaunchAgent plists with correct paths
    cat > "$HOME/Library/LaunchAgents/com.universal.memory.claude.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.universal.memory.claude</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$INSTALL_DIR/analyzers/claude-analyzer.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/launchd-claude-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/launchd-claude-stderr.log</string>
</dict>
</plist>
EOF

    cat > "$HOME/Library/LaunchAgents/com.universal.memory.codex.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.universal.memory.codex</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$INSTALL_DIR/analyzers/codex-analyzer.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/launchd-codex-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/launchd-codex-stderr.log</string>
</dict>
</plist>
EOF

    # Reload LaunchAgents
    launchctl bootout gui/$(id -u)/com.universal.memory.claude 2>/dev/null || true
    launchctl bootout gui/$(id -u)/com.universal.memory.codex 2>/dev/null || true
    launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.universal.memory.claude.plist"
    launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.universal.memory.codex.plist"

    echo -e "   ${GREEN}✓${NC} LaunchAgents updated and reloaded"
fi

# Verify update
echo ""
echo "✅ Verifying update..."

ERRORS=0

# Check if cli works
if "$INSTALL_DIR/uni-mem" stats >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} CLI working"
else
    echo -e "${RED}✗${NC} CLI not working"
    ERRORS=$((ERRORS + 1))
fi

# Check if data preserved
if [ -f "$INSTALL_DIR/memories.jsonl" ]; then
    echo -e "${GREEN}✓${NC} Memories preserved"
else
    echo -e "${RED}✗${NC} Memories missing"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "=================================================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Update Complete!${NC}"
else
    echo -e "${RED}⚠️  Update completed with $ERRORS error(s)${NC}"
    echo ""
    echo "Your data is backed up at: $BACKUP_DIR"
fi
echo "=================================================================="
echo ""

# Show updated stats
if [ -f "$INSTALL_DIR/uni-mem" ]; then
    echo "Updated installation:"
    "$INSTALL_DIR/uni-mem" stats 2>/dev/null || true
    echo ""
fi

echo "🎉 Universal AI Memory is now up to date!"
echo ""
echo "Backup available at: $BACKUP_DIR"
echo ""
