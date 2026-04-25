#!/bin/bash
# Install jluo41-tools as a Claude Code marketplace
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
echo "  ccskill           - Anthropic-bundled skills (skill-creator, docx, pptx, pdf, ...)"
echo "  chronicle         - Email indexing from MS365 Outlook"
echo "  diagram-skill     - Visual artifacts: diagram-ascii, diagram-ascii-canvas, diagram-drawio, diagram-excalidraw, progress-log"
echo "  dikw              - DIKW session orchestrator (data/info/knowledge/wisdom + plan/gate/report)"
echo "  haipipe           - haipipe umbrella commands (data, nn, end, project, subject)"
echo "  haipipe-toolkit   - haipipe specialists grouped by stage (1_data, 2_nn, 3_end, 4_project, 5_subject)"
echo "  health            - Health logging (meal-cam-logger, whoop-connect)"
echo "  logseq            - LogSeq markdown, queries, templates, whiteboards"
echo "  research-toolkit  - Research workflow stages (00_meta ... 13_venue + _workflows)"
echo "  subjective-label  - Subjective-label iterator (init, iterate, scale, status, validate)"
echo ""
echo "Install in Claude Code with e.g.:"
echo "  /plugin install dikw@jluo41-tools"
echo "  /plugin install haipipe@jluo41-tools"
echo "  /plugin install haipipe-toolkit@jluo41-tools"
echo "  /plugin install diagram-skill@jluo41-tools"

# ─── 2. Global skill installation (--global) ─────────────────────────────────

# Enumerate every skill dir (containing SKILL.md) under a plugin's skills/ tree,
# at most two levels deep so nested layouts (skills/<category>/<skill>) work.
# Prints one line per skill: "<absolute_skill_dir>\t<plugin_name>\t<rel_path_from_plugin_skills>"
enumerate_skills() {
    local plugins_root="$1"
    for plugin_dir in "$plugins_root"/*/; do
        local plugin_name skills_root
        plugin_name=$(basename "$plugin_dir")
        skills_root="$plugin_dir/skills"
        [ -d "$skills_root" ] || continue
        for entry in "$skills_root"/*/; do
            [ -d "$entry" ] || continue
            local entry_name
            entry_name=$(basename "$entry")
            if [ -f "$entry/SKILL.md" ]; then
                printf '%s\t%s\t%s\n' "${entry%/}" "$plugin_name" "$entry_name"
            else
                # Treat as category dir; descend one more level
                for nested in "$entry"*/; do
                    [ -d "$nested" ] || continue
                    if [ -f "$nested/SKILL.md" ]; then
                        local nested_name
                        nested_name=$(basename "$nested")
                        printf '%s\t%s\t%s/%s\n' "${nested%/}" "$plugin_name" "$entry_name" "$nested_name"
                    fi
                done
            fi
        done
    done
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

    # Clean up stale symlinks (point to removed skills)
    cleaned=0
    for link in "$PROJECT_SKILLS"/*/; do
        link="${link%/}"
        if [ -L "$link" ] && [ ! -e "$link" ]; then
            echo "  - $(basename "$link") (stale, removed)"
            rm "$link"
            cleaned=$((cleaned + 1))
        fi
    done

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
