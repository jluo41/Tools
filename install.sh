#!/bin/bash
# Install jluo41-tools as a Claude Code marketplace
#
# Usage:
#   git clone --recursive git@github.com:jluo41/Tools.git
#   cd Tools && ./install.sh
#
# This registers the Tools repo as a personal marketplace in Claude Code.
# After installation, skills are available via:
#   /plugin install logseq@jluo41-tools
#   /plugin install research@jluo41-tools
#   /plugin install chronicle@jluo41-tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_DIR/plugins/marketplaces/jluo41-tools"
KNOWN_FILE="$CLAUDE_DIR/plugins/known_marketplaces.json"

echo "Installing jluo41-tools marketplace..."

# Ensure directories exist
mkdir -p "$CLAUDE_DIR/plugins/marketplaces"

# Symlink the Tools repo as a marketplace
if [ -L "$MARKETPLACE_DIR" ]; then
    rm "$MARKETPLACE_DIR"
elif [ -d "$MARKETPLACE_DIR" ]; then
    echo "Warning: $MARKETPLACE_DIR already exists as a directory. Removing..."
    rm -rf "$MARKETPLACE_DIR"
fi

ln -s "$SCRIPT_DIR" "$MARKETPLACE_DIR"
echo "  Symlinked $SCRIPT_DIR -> $MARKETPLACE_DIR"

# Register in known_marketplaces.json
if [ -f "$KNOWN_FILE" ]; then
    # Add jluo41-tools entry using python (available on macOS)
    python3 -c "
import json, os
with open('$KNOWN_FILE', 'r') as f:
    data = json.load(f)
data['jluo41-tools'] = {
    'source': {
        'source': 'github',
        'repo': 'jluo41/Tools'
    },
    'installLocation': '$MARKETPLACE_DIR',
    'lastUpdated': '$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'
}
with open('$KNOWN_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
    echo "  Registered in known_marketplaces.json"
else
    echo "  Warning: $KNOWN_FILE not found. Claude Code may not be installed."
fi

echo ""
echo "Done! Available plugins:"
echo "  logseq     - LogSeq markdown, queries, templates, whiteboards"
echo "  research   - Code review, evaluation, notebooks, paper incubation"
echo "  chronicle  - Email indexing from MS365 Outlook"
echo ""
echo "Install in Claude Code with:"
echo "  /plugin install logseq@jluo41-tools"
echo "  /plugin install research@jluo41-tools"
echo "  /plugin install chronicle@jluo41-tools"
echo ""
echo "Or install all skills globally with:"
echo "  ./install.sh --global"

# --global flag: copy all skills directly to ~/.claude/skills/
if [ "$1" = "--global" ]; then
    echo ""
    echo "Installing skills globally to $CLAUDE_DIR/skills/..."
    mkdir -p "$CLAUDE_DIR/skills"

    for plugin_dir in "$SCRIPT_DIR"/plugins/*/; do
        plugin_name=$(basename "$plugin_dir")
        if [ -d "$plugin_dir/skills" ]; then
            for skill_dir in "$plugin_dir"/skills/*/; do
                skill_name=$(basename "$skill_dir")
                target="$CLAUDE_DIR/skills/$skill_name"
                if [ -L "$target" ]; then
                    rm "$target"
                fi
                ln -s "$skill_dir" "$target"
                echo "  $skill_name -> $target"
            done
        fi
    done

    echo ""
    echo "All skills installed globally. They'll be available in every Claude Code session."
fi
