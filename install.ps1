# install.ps1 — Windows installer for jluo41-tools (PowerShell port of install.sh)
#
# Usage (from the Tools/ directory):
#   .\install.ps1                       # marketplace + auto-detected project skills
#   .\install.ps1 -Project C:\path\repo # link skills into <repo>\.claude\skills
#                                      # and <repo>\.codex\skills when present
#   .\install.ps1 -Global               # also link skills into ~\.claude\skills
#   .\install.ps1 -Symlink              # use symlinks instead of junctions (needs admin / Developer Mode)
#   .\install.ps1 -NoMarketplace        # skip marketplace registration
#
# Why junctions: on Windows, native symbolic links require Administrator or
# Developer Mode. Directory junctions do not — and every skill is a directory —
# so junctions are the default. Junctions need ABSOLUTE targets, so links built
# this way do not move with the repo (re-run the installer if you relocate it).
#
# The mac/Linux equivalent is install.sh (relative symlinks).

[CmdletBinding()]
param(
    [string]$Project = "",
    [switch]$Global,
    [switch]$Symlink,
    [switch]$NoMarketplace
)

$ErrorActionPreference = "Stop"
$ScriptDir   = $PSScriptRoot
$PluginsRoot = Join-Path $ScriptDir "plugins"
$ClaudeDir   = Join-Path $env:USERPROFILE ".claude"

# ─── Skill enumeration ───────────────────────────────────────────────────────
# Recursively find every <plugin>/skills/<...>/SKILL.md, then dedupe by skill
# name. Duplicate names are resolved by priority (lowest wins), mirroring
# install.sh: standalone diagram-skill beats the haipipe utility mirrors, and
# active paper skills beat the _paper-writing-backup snapshots.
function Get-Skills {
    param([string]$Root)

    $rootFull = (Resolve-Path $Root).Path
    $rows = foreach ($f in Get-ChildItem -Path $rootFull -Recurse -Filter "SKILL.md" -File) {
        $skillDir = $f.Directory.FullName
        $rel      = $skillDir.Substring($rootFull.Length).TrimStart('\', '/')
        $parts    = $rel -split '[\\/]'
        # Only accept <plugin>/skills/<...>; skip anything not under a skills/ tree.
        if ($parts.Length -lt 3 -or $parts[1] -ne 'skills') { continue }

        $plugin  = $parts[0]
        $relPath = ($parts[2..($parts.Length - 1)] -join '/')
        $name    = $parts[-1]
        $key     = "$plugin/$relPath"

        $priority = 50
        if     ($plugin -eq 'diagram-skill')                                { $priority = 10 }
        elseif ($key -like 'haipipe-toolkit/0_utils/diagram-*')             { $priority = 70 }
        elseif ($key -like 'haipipe-toolkit/F_paper/_paper-writing-backup/*') { $priority = 80 }

        [pscustomobject]@{
            Name     = $name
            Priority = $priority
            SkillDir = $skillDir
            Plugin   = $plugin
            RelPath  = $relPath
        }
    }

    # Keep one row per skill name: lowest priority, then stable by plugin/path.
    $rows |
        Sort-Object Name, Priority, Plugin, RelPath |
        Group-Object Name |
        ForEach-Object { $_.Group[0] }
}

# ─── Agent enumeration ───────────────────────────────────────────────────────
# Recursively find every *-agent.md under agents/ directories, excluding _old/,
# _archive/, _paper-writing-backup/. Dedup by agent name: agents under skills/
# (priority 10) win over flat copies at plugin-root agents/ (priority 50).
function Get-Agents {
    param([string]$Root)

    $rootFull = (Resolve-Path $Root).Path
    $rows = foreach ($f in Get-ChildItem -Path $rootFull -Recurse -Filter "*-agent.md" -File) {
        $fullPath = $f.FullName
        $rel = $fullPath.Substring($rootFull.Length).TrimStart('\', '/')

        # Skip _old, _archive, _paper-writing-backup, README, _TEMPLATE
        if ($rel -match '[\\/]_old[\\/]' -or $rel -match '[\\/]_archive[\\/]' -or
            $rel -match '[\\/]_paper-writing-backup[\\/]') { continue }
        if ($f.Name -eq 'README.md' -or $f.Name -eq '_TEMPLATE.md') { continue }
        # Must be under an agents/ directory
        if ($rel -notmatch '[\\/]agents[\\/]') { continue }

        $parts   = $rel -split '[\\/]'
        $plugin  = $parts[0]
        $relPath = ($parts[1..($parts.Length - 1)] -join '/')
        $name    = $f.BaseName    # e.g. haipipe-task-builder-agent

        $priority = 50
        if ($relPath -match '^skills/') { $priority = 10 }

        [pscustomobject]@{
            Name      = $name
            Priority  = $priority
            AgentFile = $fullPath
            Plugin    = $plugin
            RelPath   = $relPath
        }
    }

    $rows |
        Sort-Object Name, Priority, Plugin, RelPath |
        Group-Object Name |
        ForEach-Object { $_.Group[0] }
}

function Install-Agents {
    param([string]$AgentsDir, [string]$Label)

    Write-Host ""
    Write-Host "Installing agents to $Label : $AgentsDir ..."
    New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null

    $installed = 0; $kept = 0
    foreach ($a in Get-Agents $PluginsRoot) {
        $linkPath = Join-Path $AgentsDir "$($a.Name).md"
        $target   = $a.AgentFile

        # Replace existing reparse point; never clobber a real file.
        if (Test-Path -LiteralPath $linkPath) {
            $item = Get-Item -LiteralPath $linkPath -Force
            $isReparse = ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
            if ($isReparse) { $item.Delete() }
            else { $kept++; Write-Host "  . $($a.Name) (kept, not a link)"; continue }
        }

        if ($Symlink) {
            New-Item -ItemType SymbolicLink -Path $linkPath -Target $target -Force | Out-Null
        } else {
            # Agent files are single .md files — junctions don't work for files,
            # and symlinks need admin. Fall back to Copy-Item (no admin required).
            Copy-Item -LiteralPath $target -Destination $linkPath -Force
        }
        $installed++
    }

    # Remove stale symlinks (only applies when -Symlink was used previously)
    $cleaned = 0
    foreach ($entry in Get-ChildItem -LiteralPath $AgentsDir -Filter "*.md" -Force) {
        $isReparse = ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse -and -not (Test-Path -LiteralPath $entry.Target)) {
            $entry.Delete(); $cleaned++
            Write-Host "  - $($entry.Name) (stale symlink, removed)"
        }
    }

    $verb = if ($Symlink) { "symlinked" } else { "copied" }
    Write-Host "  $installed agents $verb, $kept kept, $cleaned stale removed."
}

# ─── Link helpers ────────────────────────────────────────────────────────────
function New-SkillLink {
    param([string]$LinkPath, [string]$Target)

    # Replace an existing reparse point (junction/symlink); never clobber a real
    # file or directory the user owns.
    if (Test-Path -LiteralPath $LinkPath) {
        $item = Get-Item -LiteralPath $LinkPath -Force
        $isReparse = ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse) { $item.Delete() }
        else { return "kept" }   # real file/dir — leave it alone
    }

    if ($Symlink) {
        New-Item -ItemType SymbolicLink -Path $LinkPath -Target $Target -Force | Out-Null
    } else {
        New-Item -ItemType Junction -Path $LinkPath -Target $Target -Force | Out-Null
    }
    return "linked"
}

function Install-Skills {
    param([string]$SkillsDir, [string]$Label)

    Write-Host ""
    Write-Host "Installing skills to $Label : $SkillsDir ..."
    New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

    $installed = 0; $kept = 0
    foreach ($s in Get-Skills $PluginsRoot) {
        $linkPath = Join-Path $SkillsDir $s.Name
        $target   = Join-Path $PluginsRoot ($s.Plugin + "\skills\" + ($s.RelPath -replace '/', '\'))
        $result   = New-SkillLink -LinkPath $linkPath -Target $target
        if ($result -eq "linked") { $installed++ }
        else { $kept++; Write-Host "  . $($s.Name) (kept, not a link)" }
    }

    # Remove stale links: reparse points whose target no longer resolves.
    $cleaned = 0
    foreach ($entry in Get-ChildItem -LiteralPath $SkillsDir -Force) {
        $isReparse = ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse -and -not (Test-Path -LiteralPath $entry.Target)) {
            $entry.Delete(); $cleaned++
            Write-Host "  - $($entry.Name) (stale, removed)"
        }
    }

    $kind = if ($Symlink) { "symlinks" } else { "junctions" }
    Write-Host "  $installed $kind created, $kept kept, $cleaned stale removed."
}

# ─── 1. Marketplace registration ─────────────────────────────────────────────
if (-not $NoMarketplace) {
    Write-Host "Installing jluo41-tools marketplace..."
    $marketplaces = Join-Path $ClaudeDir "plugins\marketplaces"
    $marketplaceDir = Join-Path $marketplaces "jluo41-tools"
    New-Item -ItemType Directory -Force -Path $marketplaces | Out-Null

    if (Test-Path -LiteralPath $marketplaceDir) {
        (Get-Item -LiteralPath $marketplaceDir -Force).Delete()
    }
    if ($Symlink) {
        New-Item -ItemType SymbolicLink -Path $marketplaceDir -Target $ScriptDir -Force | Out-Null
    } else {
        New-Item -ItemType Junction -Path $marketplaceDir -Target $ScriptDir -Force | Out-Null
    }
    Write-Host "  Linked $ScriptDir -> $marketplaceDir"

    $knownFile = Join-Path $ClaudeDir "plugins\known_marketplaces.json"
    if (Test-Path -LiteralPath $knownFile) {
        $known = Get-Content -Raw -LiteralPath $knownFile | ConvertFrom-Json
        $entry = [pscustomobject]@{
            source          = [pscustomobject]@{ source = "github"; repo = "jluo41/Tools" }
            installLocation = $marketplaceDir
        }
        $known | Add-Member -NotePropertyName "jluo41-tools" -NotePropertyValue $entry -Force
        $known | ConvertTo-Json -Depth 10 | Out-File -LiteralPath $knownFile -Encoding utf8
        Write-Host "  Registered in known_marketplaces.json"
    } else {
        Write-Host "  Warning: $knownFile not found. Claude Code may not be installed."
    }
}

# ─── 2. Project-level skills (auto-detect parent workspace) ──────────────────
if (-not $Project) {
    $parent = Split-Path -Parent $ScriptDir
    if ((Test-Path -LiteralPath (Join-Path $parent ".claude")) -or
        (Test-Path -LiteralPath (Join-Path $parent ".codex"))) {
        $Project = $parent
        Write-Host "  Auto-detected workspace: $Project"
    }
}
if ($Project) {
    if (Test-Path -LiteralPath (Join-Path $Project ".claude")) {
        Install-Skills -SkillsDir (Join-Path $Project ".claude\skills") -Label "Claude project"
        Install-Agents -AgentsDir (Join-Path $Project ".claude\agents") -Label "Claude project"
    }
    if (Test-Path -LiteralPath (Join-Path $Project ".codex")) {
        Install-Skills -SkillsDir (Join-Path $Project ".codex\skills") -Label "Codex project"
    }
}

# ─── 3. Global skills (-Global) ──────────────────────────────────────────────
if ($Global) {
    Install-Skills -SkillsDir (Join-Path $ClaudeDir "skills") -Label "global"
    Install-Agents -AgentsDir (Join-Path $ClaudeDir "agents") -Label "global"
}

Write-Host ""
Write-Host "Done. Plugins: chronicle, diagram-skill, haipipe, subjective-label"
Write-Host "Install in Claude Code with e.g.: /plugin install haipipe@jluo41-tools"
