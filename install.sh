#!/bin/bash
# Universal AI Memory - Installation Script
# Automatically configures the unified memory system for Claude Code and Codex CLI

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.universal-memory"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "=================================================================="
echo "🧠 Universal AI Memory - Installer"
echo "=================================================================="
echo ""
echo "This will install a unified memory system for:"
echo "  🔵 Claude Code"
echo "  🟢 Codex CLI"
echo ""
echo "Installation directory: ${INSTALL_DIR}"
echo ""

# Check if already installed
if [ -d "$INSTALL_DIR" ] && [ -f "$INSTALL_DIR/uni-mem" ]; then
    echo -e "${YELLOW}⚠️  Universal Memory is already installed.${NC}"
    echo ""
    read -p "Reinstall and overwrite existing installation? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    echo ""
    echo "Backing up existing memories..."
    if [ -f "$INSTALL_DIR/memories.jsonl" ]; then
        cp "$INSTALL_DIR/memories.jsonl" "$INSTALL_DIR/memories.jsonl.backup-$(date +%Y%m%d-%H%M%S)"
        echo -e "${GREEN}✓${NC} Memories backed up"
    fi
fi

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    echo -e "${RED}✗ Unsupported OS: $OSTYPE${NC}"
    echo "Universal Memory currently supports macOS and Linux only."
    exit 1
fi

echo -e "${BLUE}Detected OS:${NC} $OS"

# Detect shell
SHELL_TYPE="unknown"
SHELL_RC=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_TYPE="zsh"
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_TYPE="bash"
    if [[ "$OS" == "macos" ]]; then
        SHELL_RC="$HOME/.bash_profile"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
fi

echo -e "${BLUE}Detected shell:${NC} $SHELL_TYPE"
echo ""

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$INSTALL_DIR"/{analyzers,hooks,cli,config/launchagents,logs,sessions,index}

# Copy application files
echo "📦 Installing application files..."
cp -r "$REPO_DIR/src/analyzers/"* "$INSTALL_DIR/analyzers/"
cp -r "$REPO_DIR/src/hooks/"* "$INSTALL_DIR/hooks/"
cp "$REPO_DIR/src/cli/uni-mem" "$INSTALL_DIR/"
cp -r "$REPO_DIR/src/config/launchagents/"* "$INSTALL_DIR/config/launchagents/" 2>/dev/null || true
cp "$REPO_DIR/scripts/codex-with-memory" "$INSTALL_DIR/"
cp "$REPO_DIR/scripts/migrate-old-memories.py" "$INSTALL_DIR/"
cp "$REPO_DIR/scripts/setup-launchagents.sh" "$INSTALL_DIR/"
cp "$REPO_DIR/scripts/cleanup-legacy-agents.sh" "$INSTALL_DIR/"

# Copy documentation
cp -r "$REPO_DIR/docs/"* "$INSTALL_DIR/" 2>/dev/null || true

# Set permissions
echo "🔐 Setting permissions..."
chmod +x "$INSTALL_DIR/uni-mem"
chmod +x "$INSTALL_DIR/codex-with-memory"
chmod +x "$INSTALL_DIR/analyzers/"*.py
chmod +x "$INSTALL_DIR/hooks/"*.sh
chmod +x "$INSTALL_DIR/hooks/"*.py
chmod +x "$INSTALL_DIR/migrate-old-memories.py"
chmod +x "$INSTALL_DIR/setup-launchagents.sh"
chmod +x "$INSTALL_DIR/cleanup-legacy-agents.sh"

# Initialize storage if it doesn't exist
if [ ! -f "$INSTALL_DIR/memories.jsonl" ]; then
    echo "💾 Initializing empty memory storage..."
    touch "$INSTALL_DIR/memories.jsonl"
fi

# Initialize indexes
echo "📊 Initializing indexes..."
mkdir -p "$INSTALL_DIR/index"
echo '{"claude": [], "codex": [], "unified": []}' > "$INSTALL_DIR/index/by-source.json"
echo '{}' > "$INSTALL_DIR/index/by-topic.json"
echo '{}' > "$INSTALL_DIR/index/by-date.json"

# Initialize session tracking
touch "$INSTALL_DIR/sessions/claude-processed.log"
touch "$INSTALL_DIR/sessions/codex-processed.log"

# Configure Claude Code hooks
echo "🔵 Configuring Claude Code integration..."

# Check for settings.local.json first (takes precedence), then settings.json
if [ -f "$HOME/.claude/settings.local.json" ]; then
    CLAUDE_SETTINGS="$HOME/.claude/settings.local.json"
elif [ -f "$HOME/.claude/settings.json" ]; then
    CLAUDE_SETTINGS="$HOME/.claude/settings.json"
else
    CLAUDE_SETTINGS=""
fi

if [ -n "$CLAUDE_SETTINGS" ]; then
    echo "   Configuring SessionStart hook in $(basename "$CLAUDE_SETTINGS")..."
    if python3 "$REPO_DIR/scripts/configure-claude-hook.py" \
        "$CLAUDE_SETTINGS" "$INSTALL_DIR/hooks/claude-session-start.sh"; then
        echo -e "   ${GREEN}✓${NC} Claude Code hook configured"
    else
        echo -e "   ${YELLOW}⚠️  Unable to configure Claude Code hook automatically.${NC}"
        echo ""
        echo -e "${YELLOW}Please add the following to $CLAUDE_SETTINGS:${NC}"
        echo '  "hooks": {'
        echo '    "SessionStart": [{'
        echo '      "matchers": ["startup", "resume"],'
        echo '      "hooks": [{'
        echo '        "type": "command",'
        echo "        \"command\": \"$INSTALL_DIR/hooks/claude-session-start.sh\""
        echo '      }]'
        echo '    }]'
        echo '  }'
        echo ""
        echo -e "${BLUE}💡 Tip:${NC} Claude uses settings.local.json if present, otherwise settings.json"
    fi
else
    echo -e "${YELLOW}⚠️  Claude Code not found. Hook will be configured when you install Claude Code.${NC}"
fi

# Configure LaunchAgents (macOS) or cron (Linux)
if [[ "$OS" == "macos" ]]; then
    echo "⏰ Setting up automatic extraction (LaunchAgents)..."

    # Create LaunchAgent plists with correct paths
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

    # Load LaunchAgents
    launchctl bootout gui/$(id -u)/com.universal.memory.claude 2>/dev/null || true
    launchctl bootout gui/$(id -u)/com.universal.memory.codex 2>/dev/null || true

    # Try to bootstrap - may fail in sandboxed environments
    if launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.universal.memory.claude.plist" 2>/dev/null && \
       launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.universal.memory.codex.plist" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} LaunchAgents configured and loaded"
    else
        echo -e "${YELLOW}⚠️${NC}  LaunchAgent bootstrap failed (expected in sandboxed environments)"
        echo ""
        echo "   To enable hourly automatic extraction, run this command in Terminal:"
        echo "   ~/.universal-memory/setup-launchagents.sh"
        echo ""
        echo "   Until then, analyzers will run manually when you execute them."
    fi

elif [[ "$OS" == "linux" ]]; then
    echo "⏰ Setting up automatic extraction (cron)..."

    # Add cron jobs
    (crontab -l 2>/dev/null | grep -v "universal-memory"; echo "0 * * * * /usr/bin/python3 $INSTALL_DIR/analyzers/claude-analyzer.py >> $INSTALL_DIR/logs/cron-claude.log 2>&1") | crontab -
    (crontab -l 2>/dev/null | grep -v "universal-memory"; echo "0 * * * * /usr/bin/python3 $INSTALL_DIR/analyzers/codex-analyzer.py >> $INSTALL_DIR/logs/cron-codex.log 2>&1") | crontab -

    echo -e "${GREEN}✓${NC} Cron jobs configured"
fi

# Add shell aliases
echo "🐚 Adding shell aliases..."

if [ -f "$SHELL_RC" ]; then
    # Check if aliases already exist
    if grep -q "universal-memory/uni-mem" "$SHELL_RC" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Shell aliases already configured"
    else
        echo "" >> "$SHELL_RC"
        echo "# Universal AI Memory aliases" >> "$SHELL_RC"
        echo "alias uni-mem=\"$INSTALL_DIR/uni-mem\"" >> "$SHELL_RC"
        echo "alias codex-mem=\"$INSTALL_DIR/codex-with-memory\"" >> "$SHELL_RC"
        echo -e "${GREEN}✓${NC} Shell aliases added to $SHELL_RC"
    fi
else
    echo -e "${YELLOW}⚠️  Could not find shell RC file. Add these aliases manually:${NC}"
    echo "    alias uni-mem=\"$INSTALL_DIR/uni-mem\""
    echo "    alias codex-mem=\"$INSTALL_DIR/codex-with-memory\""
fi

# Run initial extraction
echo ""
echo "🔍 Running initial extraction..."
python3 "$INSTALL_DIR/analyzers/claude-analyzer.py" 2>&1 | head -5 || true
echo -e "${GREEN}✓${NC} Initial extraction complete"

# Verify installation
echo ""
echo "✅ Verifying installation..."

ERRORS=0

# Check if cli works
if "$INSTALL_DIR/uni-mem" stats >/dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} CLI working"
else
    echo -e "${RED}✗${NC} CLI not working"
    ERRORS=$((ERRORS + 1))
fi

# Check if files exist
if [ -f "$INSTALL_DIR/memories.jsonl" ]; then
    echo -e "${GREEN}✓${NC} Storage initialized"
else
    echo -e "${RED}✗${NC} Storage not initialized"
    ERRORS=$((ERRORS + 1))
fi

# Check if LaunchAgents are loaded (macOS)
if [[ "$OS" == "macos" ]]; then
    if launchctl list | grep -q "com.universal.memory.claude"; then
        echo -e "${GREEN}✓${NC} Claude analyzer scheduled"
    else
        echo -e "${YELLOW}⚠️${NC} Claude analyzer not scheduled"
    fi

    if launchctl list | grep -q "com.universal.memory.codex"; then
        echo -e "${GREEN}✓${NC} Codex analyzer scheduled"
    else
        echo -e "${YELLOW}⚠️${NC} Codex analyzer not scheduled"
    fi
fi

echo ""
echo "=================================================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Installation Complete!${NC}"
else
    echo -e "${YELLOW}⚠️  Installation completed with $ERRORS warning(s)${NC}"
fi
echo "=================================================================="
echo ""
echo "📚 Getting Started:"
echo ""
echo "  1. Reload your shell:"
echo "     source $SHELL_RC"
echo ""
echo "  2. Try the CLI:"
echo "     uni-mem stats"
echo "     uni-mem show"
echo ""
echo "  3. Start using Claude Code or Codex CLI normally!"
echo "     - Claude: Memories auto-load at startup"
echo "     - Codex: Use 'codex-mem' command"
echo ""
echo "  4. Search your work:"
echo "     uni-mem search \"keyword\""
echo ""
echo "📖 Documentation:"
echo "   $INSTALL_DIR/README.md"
echo ""
echo "🆘 Need help?"
echo "   uni-mem status"
echo ""
echo "🎉 Happy coding with perfect memory!"
echo ""
