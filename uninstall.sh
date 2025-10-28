#!/bin/bash
# Universal AI Memory - Uninstallation Script
# Safely removes the application with optional data backup

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

INSTALL_DIR="$HOME/.universal-memory"

echo ""
echo "=================================================================="
echo "🧠 Universal AI Memory - Uninstaller"
echo "=================================================================="
echo ""

# Check if installed
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Universal Memory is not installed.${NC}"
    echo ""
    exit 0
fi

# Show what will be removed
echo "This will remove Universal AI Memory from your system."
echo ""
echo "Installation directory: ${INSTALL_DIR}"

# Check for user data
MEMORY_COUNT=0
if [ -f "$INSTALL_DIR/memories.jsonl" ]; then
    MEMORY_COUNT=$(wc -l < "$INSTALL_DIR/memories.jsonl" | tr -d ' ')
fi

if [ "$MEMORY_COUNT" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  You have $MEMORY_COUNT memory entries!${NC}"
    echo ""
    read -p "Backup your memories before uninstalling? [Y/n]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        BACKUP_FILE="$HOME/universal-memory-backup-$(date +%Y%m%d-%H%M%S).jsonl"
        cp "$INSTALL_DIR/memories.jsonl" "$BACKUP_FILE"
        echo -e "${GREEN}✓${NC} Memories backed up to: $BACKUP_FILE"
        echo ""
    fi
fi

# Final confirmation
echo ""
read -p "Proceed with uninstallation? [y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "🗑️  Uninstalling Universal AI Memory..."

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

# Remove LaunchAgents (macOS)
if [[ "$OS" == "macos" ]]; then
    echo "   Removing LaunchAgents..."
    launchctl bootout gui/$(id -u)/com.universal.memory.claude 2>/dev/null || true
    launchctl bootout gui/$(id -u)/com.universal.memory.codex 2>/dev/null || true
    rm -f "$HOME/Library/LaunchAgents/com.universal.memory.claude.plist"
    rm -f "$HOME/Library/LaunchAgents/com.universal.memory.codex.plist"
    echo -e "   ${GREEN}✓${NC} LaunchAgents removed"
fi

# Remove cron jobs (Linux)
if [[ "$OS" == "linux" ]]; then
    echo "   Removing cron jobs..."
    (crontab -l 2>/dev/null | grep -v "universal-memory") | crontab - 2>/dev/null || true
    echo -e "   ${GREEN}✓${NC} Cron jobs removed"
fi

# Remove shell aliases
echo "   Removing shell aliases..."

# Check zsh
if [ -f "$HOME/.zshrc" ]; then
    if grep -q "universal-memory" "$HOME/.zshrc"; then
        sed -i.bak '/# Universal AI Memory/d' "$HOME/.zshrc" 2>/dev/null || true
        sed -i.bak '/universal-memory/d' "$HOME/.zshrc" 2>/dev/null || true
        rm -f "$HOME/.zshrc.bak"
    fi
fi

# Check bash
if [ -f "$HOME/.bashrc" ]; then
    if grep -q "universal-memory" "$HOME/.bashrc"; then
        sed -i.bak '/# Universal AI Memory/d' "$HOME/.bashrc" 2>/dev/null || true
        sed -i.bak '/universal-memory/d' "$HOME/.bashrc" 2>/dev/null || true
        rm -f "$HOME/.bashrc.bak"
    fi
fi

if [ -f "$HOME/.bash_profile" ]; then
    if grep -q "universal-memory" "$HOME/.bash_profile"; then
        sed -i.bak '/# Universal AI Memory/d' "$HOME/.bash_profile" 2>/dev/null || true
        sed -i.bak '/universal-memory/d' "$HOME/.bash_profile" 2>/dev/null || true
        rm -f "$HOME/.bash_profile.bak"
    fi
fi

echo -e "   ${GREEN}✓${NC} Shell aliases removed"

# Remove Claude Code hook
echo "   Removing Claude Code hook..."
if [ -f "$HOME/.claude/settings.json" ]; then
    if grep -q "universal-memory" "$HOME/.claude/settings.json"; then
        echo -e "   ${YELLOW}⚠️  Please manually remove the SessionStart hook from:${NC}"
        echo "      ~/.claude/settings.json"
        echo ""
        echo "      Look for: universal-memory/hooks/claude-session-start.sh"
        echo ""
    fi
fi

# Remove installation directory
echo "   Removing installation directory..."
rm -rf "$INSTALL_DIR"
echo -e "   ${GREEN}✓${NC} Installation directory removed"

echo ""
echo "=================================================================="
echo -e "${GREEN}✅ Uninstallation Complete!${NC}"
echo "=================================================================="
echo ""
echo "Universal AI Memory has been removed from your system."
echo ""

if [ -n "$BACKUP_FILE" ]; then
    echo "📦 Your memories are backed up at:"
    echo "   $BACKUP_FILE"
    echo ""
fi

echo "To reinstall, run:"
echo "  ./install.sh"
echo ""
