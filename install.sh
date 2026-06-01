#!/bin/bash
# Install jluo41-tools as a Claude Code marketplace (macOS / Linux).
# Windows users: run install.ps1 in PowerShell instead — it creates directory
# junctions (native symlinks need admin/Developer Mode on Windows).
#
# Usage:
#   git clone --recursive git@github.com:jluo41/Tools.git
#   cd Tools && ./install.sh
#
# Options:
#   --global              Also symlink all skills to ~/.claude/skills/
#   --project <path>      Symlink all skills into <path>/.claude/skills/ (relative paths)
#   --hooks               Also configure sound hooks in settings.json
#   --all                 Do everything (marketplace + global + hooks)
#
# Skills are enumerated dynamically from plugins/**/skills/*/SKILL.md, so adding
# or moving a plugin needs no edits here — just re-run. Anything under legacy/ is
# intentionally excluded. The link set is OS/machine-specific; gitignore
# <project>/.claude/skills/ and regenerate per machine rather than committing it.
#
# Sound hooks work on macOS (afplay) and Linux (paplay/aplay).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
MARKETPLACE_DIR="$CLAUDE_DIR/plugins/marketplaces/jluo41-tools"
KNOWN_FILE="$CLAUDE_DIR/plugins/known_marketplaces.json"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

# Parse flags
DO_GLOBAL=false
DO_HOOKS=false
PROJECT_PATH=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --global)  DO_GLOBAL=true ;;
        --hooks)   DO_HOOKS=true ;;
        --all)     DO_GLOBAL=true; DO_HOOKS=true ;;
        --project) PROJECT_PATH="$2"; shift ;;
    esac
    shift
done

# Auto-detect parent workspace if --project was not given
if [ -z "$PROJECT_PATH" ]; then
    PARENT_DIR="$(dirname "$SCRIPT_DIR")"
    if [ -d "$PARENT_DIR/.claude" ]; then
        PROJECT_PATH="$PARENT_DIR"
        echo "  Auto-detected workspace: $PROJECT_PATH"
    fi
fi

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
echo "  chronicle         - Session, daily, email, and Obsidian chronicle workflows"
echo "  diagram-skill     - Visual artifacts: diagram-ascii, diagram-ascii-canvas, diagram-drawio, diagram-excalidraw, progress-log"
echo "  haipipe           - HAI-Pipe research toolkit: data, NN, endpoint, task, experiment, paper, application"
echo "  subjective-label  - Subjective-label iterator (init, iterate, scale, status, validate)"
echo ""
echo "Install in Claude Code with e.g.:"
echo "  /plugin install haipipe@jluo41-tools"
echo "  /plugin install diagram-skill@jluo41-tools"
echo "  /plugin install subjective-label@jluo41-tools"

# ─── 2. Global skill installation (--global) ─────────────────────────────────

# Enumerate every skill dir (containing SKILL.md) under a plugin's skills/ tree.
# Discovery is recursive because haipipe-toolkit intentionally nests skills by
# workflow family, e.g. skills/F_paper/4-write/paper-write.
# Prints one line per skill: "<absolute_skill_dir>\t<plugin_name>\t<rel_path_from_plugin_skills>"
enumerate_skills() {
    local plugins_root="$1"

    find "$plugins_root" -path '*/skills/*/SKILL.md' -type f -print | while IFS= read -r skill_file; do
        local skill_path plugin_rel plugin_name rel_path skill_name priority
        skill_path="${skill_file%/SKILL.md}"
        plugin_rel="${skill_path#"$plugins_root"/}"
        plugin_name="${plugin_rel%%/*}"
        rel_path="${skill_path#"$plugins_root/$plugin_name/skills/"}"
        skill_name="$(basename "$skill_path")"

        # Duplicate skill names cannot both be symlinked into one skills dir.
        # Keep the canonical copy deterministically:
        #   1. standalone diagram-skill wins over haipipe utility mirrors
        #   2. active paper skills win over _paper-writing-backup snapshots
        #   3. otherwise sort by plugin/path for stable installs
        priority=50
        case "$plugin_name/$rel_path" in
            diagram-skill/*) priority=10 ;;
            haipipe-toolkit/0_utils/diagram-*) priority=70 ;;
            haipipe-toolkit/F_paper/_paper-writing-backup/*) priority=80 ;;
        esac

        printf '%03d\t%s\t%s\t%s\t%s\n' "$priority" "$skill_name" "$skill_path" "$plugin_name" "$rel_path"
    done | sort -t $'\t' -k2,2 -k1,1n -k4,4 -k5,5 | awk -F '\t' '
        !seen[$2]++ {
            print $3 "\t" $4 "\t" $5
            next
        }
        {
            print "  . " $2 " (duplicate skipped: " $4 "/skills/" $5 ")" > "/dev/stderr"
        }
    '
}

if [ "$DO_GLOBAL" = true ]; then
    echo ""
    echo "Installing skills globally to $CLAUDE_DIR/skills/..."
    mkdir -p "$CLAUDE_DIR/skills"

    while IFS=$'\t' read -r skill_path plugin_name rel_path; do
        skill_name=$(basename "$skill_path")
        target="$CLAUDE_DIR/skills/$skill_name"
        if [ -L "$target" ]; then
            rm "$target"
        elif [ -e "$target" ]; then
            echo "  . $skill_name (kept, not a symlink)"
            continue
        fi
        ln -s "$skill_path" "$target"
        echo "  $skill_name -> $target"
    done < <(enumerate_skills "$SCRIPT_DIR/plugins")

    echo "  All skills installed globally."
fi

# ─── 3. Project-level skill installation (--project) ────────────────────────

if [ -n "$PROJECT_PATH" ]; then
    PROJECT_SKILLS="$PROJECT_PATH/.claude/skills"
    echo ""
    echo "Installing skills to project: $PROJECT_SKILLS ..."
    mkdir -p "$PROJECT_SKILLS"

    # Compute relative path from .claude/skills/ back to Tools/plugins/
    # e.g., ../../Tools/plugins
    TOOLS_REL="$(python3 -c "import os.path; print(os.path.relpath('$SCRIPT_DIR/plugins', '$PROJECT_SKILLS'))")"

    installed=0
    while IFS=$'\t' read -r skill_path plugin_name rel_path; do
        skill_name=$(basename "$skill_path")
        target="$PROJECT_SKILLS/$skill_name"

        # Skip non-symlink entries (real dirs the user owns)
        if [ -e "$target" ] && [ ! -L "$target" ]; then
            echo "  . $skill_name (kept, not a symlink)"
            continue
        fi

        # Create or update symlink (relative, so the workspace can move)
        [ -L "$target" ] && rm "$target"
        ln -s "$TOOLS_REL/$plugin_name/skills/$rel_path" "$target"
        installed=$((installed + 1))
    done < <(enumerate_skills "$SCRIPT_DIR/plugins")

    # Clean up stale symlinks (point to removed skills).
    # Use plain "*" rather than "*/" so broken symlinks (whose target no
    # longer exists) are still enumerated — "*/" requires the entry to
    # resolve to a directory and silently skips dangling links.
    cleaned=0
    shopt -s nullglob
    for link in "$PROJECT_SKILLS"/*; do
        if [ -L "$link" ] && [ ! -e "$link" ]; then
            echo "  - $(basename "$link") (stale, removed)"
            rm "$link"
            cleaned=$((cleaned + 1))
        fi
    done
    shopt -u nullglob

    echo "  $installed skills symlinked, $cleaned stale links removed."
fi

# ─── 4. Sound hooks (--hooks) ────────────────────────────────────────────────

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
echo "  ./install.sh --global                Symlink skills to ~/.claude/skills/"
echo "  ./install.sh --project /path/to/repo  Symlink skills to repo's .claude/skills/"
echo "  ./install.sh --hooks                 Configure sound hooks in settings.json"
echo "  ./install.sh --all                   Do everything (marketplace + global + hooks)"
