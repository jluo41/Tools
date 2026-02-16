#!/bin/bash
# Install jluo41-tools as a Claude Code marketplace
#
# Usage:
#   git clone --recursive git@github.com:jluo41/Tools.git
#   cd Tools && ./install.sh
#
# Options:
#   --global    Also symlink all skills to ~/.claude/skills/
#   --hooks     Also configure sound hooks in settings.json
#   --all       Do everything (marketplace + global + hooks)
#
# Works on macOS (afplay) and Linux (paplay/aplay).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_DIR/plugins/marketplaces/jluo41-tools"
KNOWN_FILE="$CLAUDE_DIR/plugins/known_marketplaces.json"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

# Parse flags
DO_GLOBAL=false
DO_HOOKS=false
for arg in "$@"; do
    case "$arg" in
        --global) DO_GLOBAL=true ;;
        --hooks)  DO_HOOKS=true ;;
        --all)    DO_GLOBAL=true; DO_HOOKS=true ;;
    esac
done

# ─── 1. Marketplace registration ─────────────────────────────────────────────

echo "Installing jluo41-tools marketplace..."

mkdir -p "$CLAUDE_DIR/plugins/marketplaces"

if [ -L "$MARKETPLACE_DIR" ]; then
    rm "$MARKETPLACE_DIR"
elif [ -d "$MARKETPLACE_DIR" ]; then
    echo "  Warning: $MARKETPLACE_DIR already exists as a directory. Removing..."
    rm -rf "$MARKETPLACE_DIR"
fi

ln -s "$SCRIPT_DIR" "$MARKETPLACE_DIR"
echo "  Symlinked $SCRIPT_DIR -> $MARKETPLACE_DIR"

if [ -f "$KNOWN_FILE" ]; then
    python3 -c "
import json
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

# ─── 2. Global skill installation (--global) ─────────────────────────────────

if [ "$DO_GLOBAL" = true ]; then
    echo ""
    echo "Installing skills globally to $CLAUDE_DIR/skills/..."
    mkdir -p "$CLAUDE_DIR/skills"

    for plugin_dir in "$SCRIPT_DIR"/plugins/*/; do
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

    echo "  All skills installed globally."
fi

# ─── 3. Sound hooks (--hooks) ────────────────────────────────────────────────

if [ "$DO_HOOKS" = true ]; then
    echo ""
    echo "Configuring sound hooks in settings.json..."

    python3 << 'PYEOF'
import json, platform, shutil, os

settings_file = os.path.expanduser("~/.claude/settings.json")

# Detect OS and pick sound player + sound files
system = platform.system()

if system == "Darwin":
    # macOS
    player = "afplay"
    sounds = {
        "SessionStart":       "/System/Library/Sounds/Hero.aiff",
        "Stop":               "/System/Library/Sounds/Glass.aiff",
        "TaskCompleted":      "/System/Library/Sounds/Purr.aiff",
        "PermissionRequest":  "/System/Library/Sounds/Blow.aiff",
        "Notification":       "/System/Library/Sounds/Ping.aiff",
        "SubagentStart":      "/System/Library/Sounds/Submarine.aiff",
        "SubagentStop":       "/System/Library/Sounds/Pop.aiff",
        "PostToolUseFailure": "/System/Library/Sounds/Basso.aiff",
    }
elif system == "Linux":
    # Linux — try paplay (PulseAudio) first, fall back to aplay (ALSA)
    player = "paplay" if shutil.which("paplay") else "aplay"
    # freedesktop sound theme paths (Ubuntu/Debian/Fedora)
    sound_dirs = [
        "/usr/share/sounds/freedesktop/stereo",
        "/usr/share/sounds/gnome/default/alerts",
        "/usr/share/sounds/ubuntu/stereo",
    ]
    # Find first existing sound directory
    sound_dir = next((d for d in sound_dirs if os.path.isdir(d)), sound_dirs[0])
    sounds = {
        "SessionStart":       f"{sound_dir}/service-login.oga",
        "Stop":               f"{sound_dir}/complete.oga",
        "TaskCompleted":      f"{sound_dir}/complete.oga",
        "PermissionRequest":  f"{sound_dir}/dialog-warning.oga",
        "Notification":       f"{sound_dir}/message.oga",
        "SubagentStart":      f"{sound_dir}/service-login.oga",
        "SubagentStop":       f"{sound_dir}/service-logout.oga",
        "PostToolUseFailure": f"{sound_dir}/dialog-error.oga",
    }
else:
    print(f"  Unsupported OS: {system}. Skipping sound hooks.")
    exit(0)

# Load existing settings
if os.path.exists(settings_file):
    with open(settings_file, "r") as f:
        settings = json.load(f)
else:
    settings = {}

# Build hooks config
hooks = {}
for event, sound_file in sounds.items():
    hooks[event] = [
        {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": f"{player} {sound_file}",
                    "async": True
                }
            ]
        }
    ]

# Merge — overwrite hooks section, preserve everything else
settings["hooks"] = hooks

with open(settings_file, "w") as f:
    json.dump(settings, f, indent=2)

print(f"  OS: {system}, player: {player}")
print(f"  Configured {len(sounds)} sound hooks:")
for event, sound in sounds.items():
    print(f"    {event:22s} -> {os.path.basename(sound)}")
PYEOF

    echo "  Sound hooks installed."
fi

# ─── Summary ─────────────────────────────────────────────────────────────────

echo ""
echo "Run with flags for more:"
echo "  ./install.sh --global   Symlink skills to ~/.claude/skills/"
echo "  ./install.sh --hooks    Configure sound hooks in settings.json"
echo "  ./install.sh --all      Do everything"
