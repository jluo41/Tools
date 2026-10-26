# install.ps1 - Windows installer for jluo41-tools (PowerShell port of install.sh)
#
# Usage (from the Tools/ directory):
#   .\install.ps1                       # marketplace + auto-detected project skills
#   .\install.ps1 -Project C:\path\repo # link skills into <repo>\.claude\skills,
#                                      # <repo>\.codex\skills and <repo>\.agents\skills
#                                      # when present
#   .\install.ps1 -Global               # also link skills into ~\.claude\skills
#   .\install.ps1 -Hooks                # configure sound hooks in settings.json
#   .\install.ps1 -All                  # marketplace + global + hooks
#   .\install.ps1 -Symlink              # use symlinks instead of junctions (needs admin / Developer Mode)
#   .\install.ps1 -NoMarketplace        # skip marketplace registration
#   .\install.ps1 -Verify               # audit a workspace's links and write nothing
#                                       # (exit 1 if anything is stale, missing, or
#                                       # pointing at a folder Tools no longer uses)
#
# Sound hooks read the same per-OS table as install.sh (install-hooks.json), so
# the two installers cannot drift. Each keeps its own writer, which is why this
# one needs no Python.
#
# Why junctions: on Windows, native symbolic links require Administrator or
# Developer Mode. Directory junctions do not - and every skill is a directory -
# so junctions are the default. Junctions need ABSOLUTE targets, so links built
# this way do not move with the repo (re-run the installer if you relocate it).
#
# The mac/Linux equivalent is install.sh (relative symlinks).

[CmdletBinding()]
param(
    [string]$Project = "",
    [switch]$Global,
    [switch]$Hooks,
    [switch]$All,
    [switch]$Symlink,
    [switch]$NoMarketplace,
    [switch]$Verify
)

$ErrorActionPreference = "Stop"
$ScriptDir   = $PSScriptRoot
$PluginsRoot = Join-Path $ScriptDir "plugins"
# USERPROFILE is the Windows home. The fallback lets the script run under
# pwsh on macOS/Linux for testing; on Windows it never fires.
$userHome    = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$ClaudeDir   = Join-Path $userHome ".claude"

if ($All) { $Global = $true; $Hooks = $true }

# Write JSON without a BOM. Windows PowerShell 5.1's `Out-File -Encoding utf8`
# emits one, and a BOM in known_marketplaces.json or settings.json breaks strict
# JSON readers. PS7's utf8NoBOM is not available on 5.1, so do it by hand.
function Write-JsonFile {
    param([string]$Path, [object]$Object)
    $json = $Object | ConvertTo-Json -Depth 20
    [IO.File]::WriteAllText($Path, $json, (New-Object Text.UTF8Encoding $false))
}

# ─── Skill enumeration ───────────────────────────────────────────────────────
# Recursively find every <plugin>/skills/<...>/SKILL.md, then dedupe by skill
# name. Mirrors install.sh exactly, including its prune: any folder whose name
# starts with "_" (_old, _archive, _todo, _legacy, ...) and node_modules/ are
# excluded BEFORE matching, not merely demoted. Until 2026-07-26 this function only
# demoted them, so Windows installed two retired skills (haipipe-project-organize,
# haipipe-project-inspect) that macOS never saw. haipipe-toolkit nests skills in
# layers (skills/0_utils, skills/1_base/<family>, skills/2_theme/<theme>); the
# rule names no layer, so a layer move cannot leave it pointing nowhere.
#
# Duplicate names are resolved by priority (lowest wins), ties by plugin/path.
# No promotion rule is live today: install.sh's two rules named a plugin that no
# longer exists and a directory that is pruned here anyway, so both were dropped
# from both scripts. Add one in the same place in each if a collision appears.
function Get-Skills {
    param([string]$Root)

    $rootFull = (Resolve-Path $Root).Path
    $rows = foreach ($f in Get-ChildItem -Path $rootFull -Recurse -Filter "SKILL.md" -File) {
        $skillDir = $f.Directory.FullName
        $rel      = $skillDir.Substring($rootFull.Length).TrimStart('\', '/')
        $parts    = $rel -split '[\\/]'
        # Only accept <plugin>/skills/<...>; skip anything not under a skills/ tree.
        if ($parts.Length -lt 3 -or $parts[1] -ne 'skills') { continue }
        # install.sh's -prune, as an exclusion rather than a demotion.
        if (@($parts | Where-Object { $_.StartsWith('_') -or $_ -eq 'node_modules' }).Count -gt 0) {
            continue
        }

        $plugin  = $parts[0]
        $relPath = ($parts[2..($parts.Length - 1)] -join '/')
        $name    = $parts[-1]

        [pscustomobject]@{
            Name     = $name
            Priority = 50
            SkillDir = $skillDir
            Plugin   = $plugin
            RelPath  = $relPath
        }
    }

    # Keep one row per skill name: lowest priority, then stable by plugin/path.
    # install.sh reports what it dropped, so this does too.
    $rows |
        Sort-Object Name, Priority, Plugin, RelPath |
        Group-Object Name |
        ForEach-Object {
            foreach ($dup in ($_.Group | Select-Object -Skip 1)) {
                Write-Host "  . $($dup.Name) (duplicate skipped: $($dup.Plugin)/skills/$($dup.RelPath))"
            }
            $_.Group[0]
        }
}

# Short names, as install.sh makes them: `aliases: [wb]` under `metadata:` in a
# SKILL.md is one more link per alias to the same folder (/wb is /workbench). An
# alias that is already a skill's own name is skipped. Shared by Install-Skills
# and the -Verify audit, so the two can never disagree about what should exist.
function Get-SkillAliases {
    param([array]$Skills)

    $names = @{}
    foreach ($s in $Skills) { $names[$s.Name] = $true }

    foreach ($s in $Skills) {
        $text = Get-Content -LiteralPath (Join-Path $s.SkillDir "SKILL.md") -Raw -ErrorAction SilentlyContinue
        if (-not $text -or -not $text.StartsWith('---')) { continue }
        $head = ($text -split "`n---", 2)[0]
        $m = [regex]::Match($head, '(?m)^\s+aliases:\s*\[?([^\]\r\n#]*)\]?')
        if (-not $m.Success) { continue }
        foreach ($alias in ($m.Groups[1].Value -split ',' | ForEach-Object { $_.Trim().Trim('"', "'") })) {
            if ($alias -notmatch '^[a-z0-9][a-z0-9-]*$') { continue }
            if ($names.ContainsKey($alias)) {
                Write-Host "  . $alias (alias of $($s.Name) skipped: a skill has that name)"
                continue
            }
            [pscustomobject]@{ Name = $alias; Skill = $s }
        }
    }
}

# ─── Agent enumeration ───────────────────────────────────────────────────────
# Recursively find every *-agent.md under agents/ directories, excluding any
# folder whose name starts with "_" and node_modules/ (as install.sh does).
# Dedup by agent name: agents under skills/
# (priority 10) win over flat copies at plugin-root agents/ (priority 50).
function Get-Agents {
    param([string]$Root)

    $rootFull = (Resolve-Path $Root).Path
    $rows = foreach ($f in Get-ChildItem -Path $rootFull -Recurse -Filter "*-agent.md" -File) {
        $fullPath = $f.FullName
        $rel = $fullPath.Substring($rootFull.Length).TrimStart('\', '/')
        $parts   = $rel -split '[\\/]'

        # install.sh's prunes, as exclusions.
        if (@($parts | Where-Object { $_.StartsWith('_') -or $_ -eq 'node_modules' }).Count -gt 0) { continue }
        # install.sh matches */agents/*-agent.md, so the file must sit DIRECTLY in
        # an agents/ dir. Matching 'agents' anywhere in the path would also pull in
        # agents/<subdir>/x-agent.md, which the .sh installer never sees.
        if ($parts.Length -lt 2 -or $parts[-2] -ne 'agents') { continue }

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

    # install.sh reports the agents it dropped, so this does too.
    $rows |
        Sort-Object Name, Priority, Plugin, RelPath |
        Group-Object Name |
        ForEach-Object {
            foreach ($dup in ($_.Group | Select-Object -Skip 1)) {
                Write-Host "  . $($dup.Name) (duplicate skipped: $($dup.Plugin)/$($dup.RelPath))"
            }
            $_.Group[0]
        }
}

# Agent files are single .md files: junctions do not work for files and symlinks
# need admin, so without -Symlink they are COPIED. A copy is indistinguishable
# from a file the user wrote, which broke the installer until 2026-07-26: the
# "kept, not a link" guard saw its own copy on the second run and skipped it, so
# agents were written once and then never updated again. install.sh's header
# warns about exactly this drift; on Windows it was the default path.
#
# The manifest is what makes the guard honest. A name in it is ours, so it gets
# overwritten and, once the agent disappears upstream, deleted. A name not in it
# is the user's own file and is never touched.
$AgentManifestName = ".jluo41-tools-agents.json"

function Get-AgentManifest {
    param([string]$AgentsDir)
    $p = Join-Path $AgentsDir $AgentManifestName
    if (-not (Test-Path -LiteralPath $p)) { return @() }
    try { return @((Get-Content -Raw -LiteralPath $p | ConvertFrom-Json).files) }
    catch { return @() }
}

function Install-Agents {
    param([string]$AgentsDir, [string]$Label)

    Write-Host ""
    Write-Host "Installing agents to $Label : $AgentsDir ..."
    New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null

    $previous = Get-AgentManifest $AgentsDir
    $written  = New-Object System.Collections.Generic.List[string]

    $installed = 0; $kept = 0
    foreach ($a in Get-Agents $PluginsRoot) {
        $fileName = "$($a.Name).md"
        $linkPath = Join-Path $AgentsDir $fileName
        $target   = $a.AgentFile

        if (Test-Path -LiteralPath $linkPath) {
            $item = Get-Item -LiteralPath $linkPath -Force
            $isReparse = ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
            if ($isReparse) {
                $item.Delete()
            } elseif ($previous -notcontains $fileName) {
                # A real file we did not write: the user owns it.
                $kept++; Write-Host "  . $($a.Name) (kept, not ours)"; continue
            }
            # else: our own copy from a previous run, refresh it below.
        }

        if ($Symlink) {
            New-Item -ItemType SymbolicLink -Path $linkPath -Target $target -Force | Out-Null
        } else {
            Copy-Item -LiteralPath $target -Destination $linkPath -Force
        }
        $written.Add($fileName)
        $installed++
    }

    # Remove what we wrote before and no longer produce: retired agents, plus any
    # dangling symlink from a -Symlink run.
    $cleaned = 0
    foreach ($old in $previous) {
        if ($written.Contains($old)) { continue }
        $p = Join-Path $AgentsDir $old
        if (Test-Path -LiteralPath $p) {
            Remove-Item -LiteralPath $p -Force
            Write-Host "  - $old (retired, removed)"
            $cleaned++
        }
    }
    foreach ($entry in Get-ChildItem -LiteralPath $AgentsDir -Filter "*.md" -Force) {
        $isReparse = ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse -and -not (Test-Path -LiteralPath $entry.Target)) {
            $entry.Delete(); $cleaned++
            Write-Host "  - $($entry.Name) (stale symlink, removed)"
        }
    }

    Write-JsonFile -Path (Join-Path $AgentsDir $AgentManifestName) `
                   -Object ([pscustomobject]@{
                       _comment = "Written by install.ps1. Lists the agent files this installer owns, so a re-run can refresh them and a retired agent can be removed. Delete a name here to make the installer treat that file as yours."
                       files    = [string[]]@($written)
                   })

    $verb = if ($Symlink) { "symlinked" } else { "copied" }
    Write-Host "  $installed agents $verb, $kept kept, $cleaned removed."
}

# ─── Link helpers ────────────────────────────────────────────────────────────
# A link's target as an absolute path. Junctions store absolute targets; a
# symlink made by install.sh (or by hand) may store a relative one, which
# Test-Path would resolve against the current directory instead of the link's
# own folder - turning a perfectly good link into a "dangling" one.
function Resolve-LinkTarget {
    param([string]$LinkPath, [string]$Target)
    if (-not $Target) { return $null }
    if (-not [IO.Path]::IsPathRooted($Target)) {
        # A link at the filesystem root (/tmp on macOS is a symlink to
        # /private/tmp) has no parent to join against.
        $parent = Split-Path -Parent $LinkPath
        if (-not $parent) { $parent = [IO.Path]::DirectorySeparatorChar }
        $Target = Join-Path $parent $Target
    }
    try { (Resolve-Path -LiteralPath $Target).Path } catch { $null }
}

# The directory a path really is, following symlink/junction hops. install.sh's
# audit gets this for free from Path.resolve(); PowerShell's Resolve-Path does
# not follow a symlink, and only the last component can be one: a skill folder
# under Knowledge-SPACE/Tools (a symlink to ../Tools-SPACE) is a plain directory.
# Without this, every link looks like drift when the installer runs through the
# symlink - the expected path runs through Tools, the link's target through the
# real folder, and the two strings never match.
function Get-RealPath {
    param([string]$Path)

    $sep = [IO.Path]::DirectorySeparatorChar
    $real = @()
    foreach ($part in ((Resolve-Path -LiteralPath $Path).Path -split '[\\/]')) {
        # An absolute path splits with a leading empty part; keep it so the
        # joined candidate still starts with the separator.
        if (-not $part) { if ($real.Count -eq 0) { $real = @('') }; continue }

        $candidate = ($real + $part) -join $sep
        try { $item = Get-Item -LiteralPath $candidate -Force } catch { return $candidate }

        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) {
            $real += $part
            continue
        }

        $next = Resolve-LinkTarget -LinkPath $candidate -Target $item.Target
        if (-not $next) { return $candidate }
        $real = @((Resolve-Path -LiteralPath $next).Path -split '[\\/]')
    }

    return ($real -join $sep)
}

function New-SkillLink {
    param([string]$LinkPath, [string]$Target)

    # Replace an existing reparse point (junction/symlink); never clobber a real
    # file or directory the user owns.
    if (Test-Path -LiteralPath $LinkPath) {
        $item = Get-Item -LiteralPath $LinkPath -Force
        $isReparse = ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse) { $item.Delete() }
        else { return "kept" }   # real file/dir - leave it alone
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
    $skills = @(Get-Skills $PluginsRoot)
    foreach ($s in $skills) {
        $linkPath = Join-Path $SkillsDir $s.Name
        $target   = Join-Path $PluginsRoot ($s.Plugin + "\skills\" + ($s.RelPath -replace '/', '\'))
        $result   = New-SkillLink -LinkPath $linkPath -Target $target
        if ($result -eq "linked") { $installed++ }
        else { $kept++; Write-Host "  . $($s.Name) (kept, not a link)" }
    }

    # Short names: one more link per alias, to the same skill folder. The alias
    # rule lives in Get-SkillAliases so the -Verify audit reads the same list.
    foreach ($a in Get-SkillAliases $skills) {
        $s = $a.Skill
        $target = Join-Path $PluginsRoot ($s.Plugin + "\skills\" + ($s.RelPath -replace '/', '\'))
        $result = New-SkillLink -LinkPath (Join-Path $SkillsDir $a.Name) -Target $target
        if ($result -eq "linked") { $installed++ }
        else { $kept++; Write-Host "  . $($a.Name) (kept, not a link)" }
    }

    # Remove stale links: reparse points whose target no longer resolves.
    $cleaned = 0
    foreach ($entry in Get-ChildItem -LiteralPath $SkillsDir -Force) {
        $isReparse = ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
        if ($isReparse -and -not (Resolve-LinkTarget -LinkPath $entry.FullName -Target $entry.Target)) {
            $entry.Delete(); $cleaned++
            Write-Host "  - $($entry.Name) (stale, removed)"
        }
    }

    $kind = if ($Symlink) { "symlinks" } else { "junctions" }
    Write-Host "  $installed $kind created, $kept kept, $cleaned stale removed."
}

# ─── Audit mode (-Verify) ──────────────────────────────────────────────────────
# Read-only mirror of install.sh --verify: report what a workspace's links
# actually point to, without touching anything. Exit 1 when anything is out of
# date, so a setup step can gate on it. Junctions make Windows drift in a way
# macOS rarely sees: an absolute junction survives a Tools move as long as the
# old folder still exists somewhere, so "resolves" is not the same as "current".
function Test-WorkspaceLinks {
    param([string]$Project)

    Write-Host "Verifying links for: $Project"
    try {
        $commit = (& git -C $ScriptDir rev-parse --short HEAD)
        if ($commit) {
            Write-Host "  Tools commit: $commit"
            Write-Host "  Uncommitted files in Tools: $((@(& git -C $ScriptDir status --porcelain)).Count)"
        }
    } catch { }

    $skills = @(Get-Skills $PluginsRoot)
    $expectedSkills = @{}
    foreach ($s in $skills) { $expectedSkills[$s.Name] = Get-RealPath $s.SkillDir }
    foreach ($a in Get-SkillAliases $skills) {
        $expectedSkills[$a.Name] = Get-RealPath $a.Skill.SkillDir
    }

    $expectedAgents = @{}
    foreach ($a in Get-Agents $PluginsRoot) { $expectedAgents["$($a.Name).md"] = Get-RealPath $a.AgentFile }

    $problems = 0
    foreach ($check in @(
        [pscustomobject]@{ Label = "Claude skills"; Dir = Join-Path $Project ".claude\skills"; Expected = $expectedSkills },
        [pscustomobject]@{ Label = "Codex skills";  Dir = Join-Path $Project ".codex\skills";  Expected = $expectedSkills },
        [pscustomobject]@{ Label = "Shared agents skills"; Dir = Join-Path $Project ".agents\skills"; Expected = $expectedSkills },
        [pscustomobject]@{ Label = "Claude agents"; Dir = Join-Path $Project ".claude\agents"; Expected = $expectedAgents }
    )) {
        Write-Host "  $($check.Label): $($check.Dir)"
        if (-not (Test-Path -LiteralPath $check.Dir)) {
            Write-Host "    not installed - run the installer"
            $problems++
            continue
        }

        # The agent manifest is the installer's own bookkeeping, not a link.
        $entries = @(Get-ChildItem -LiteralPath $check.Dir -Force |
                     Where-Object { $_.Name -ne $AgentManifestName })
        $dangling = @(); $drift = @(); $owned = @()
        foreach ($entry in $entries) {
            $isReparse = ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
            if (-not $isReparse) { $owned += $entry.Name; continue }
            $target = Resolve-LinkTarget -LinkPath $entry.FullName -Target $entry.Target
            if (-not $target) { $dangling += $entry.Name; continue }
            if ($check.Expected.ContainsKey($entry.Name)) {
                $have = (Get-RealPath $target).TrimEnd('\')
                $want = $check.Expected[$entry.Name].TrimEnd('\')
                if ($have -ne $want) { $drift += [pscustomobject]@{ Name = $entry.Name; Target = $have } }
            }
        }

        $present = @($entries | ForEach-Object { $_.Name })
        $missing = @($check.Expected.Keys | Where-Object { $present -notcontains $_ })
        # A real directory you made is reported as yours, not as an unexplained link.
        $unknown = @($present | Where-Object {
            -not $check.Expected.ContainsKey($_) -and
            $dangling -notcontains $_ -and
            $owned -notcontains $_
        })

        Write-Host "    $($entries.Count) entries, $($check.Expected.Count) expected"
        if ($dangling) { Write-Host "    $($dangling.Count) dangling: $($dangling -join ', ')" }
        if ($drift) {
            Write-Host "    $($drift.Count) resolve but point where Tools no longer keeps them:"
            foreach ($d in $drift) { Write-Host "      $($d.Name) -> $($d.Target)" }
        }
        if ($missing) { Write-Host "    $($missing.Count) not linked: $($missing -join ', ')" }
        if ($unknown) { Write-Host "    $($unknown.Count) links with no matching skill or agent on disk: $($unknown -join ', ')" }
        if ($owned) { Write-Host "    $($owned.Count) real directories you own (the installer leaves these alone): $($owned -join ', ')" }

        $problems += $dangling.Count + $drift.Count + $missing.Count
    }

    # A skill that shells out to a server is only real if that server is registered.
    $mcpFile = Join-Path $Project ".mcp.json"
    $registered = @()
    if (Test-Path -LiteralPath $mcpFile) {
        try {
            $parsed = Get-Content -Raw -LiteralPath $mcpFile | ConvertFrom-Json
            if ($parsed.mcpServers) { $registered = @($parsed.mcpServers.PSObject.Properties.Name) }
        } catch { Write-Host "  .mcp.json exists but is not valid JSON" }
    }

    $servers = @()
    foreach ($package in Get-ChildItem -LiteralPath $PluginsRoot -Directory |
                         Where-Object { -not $_.Name.StartsWith('_') }) {
        $root = Join-Path $package.FullName "mcp-servers"
        if (Test-Path -LiteralPath $root) {
            foreach ($child in Get-ChildItem -LiteralPath $root -Directory) {
                $servers += [pscustomobject]@{ Plugin = $package.Name; Name = $child.Name }
            }
        }
    }

    if ($servers) {
        Write-Host "  MCP servers in the repo:"
        foreach ($s in $servers) {
            $state = if ($registered -contains $s.Name) { "registered" } else { "not registered in .mcp.json" }
            Write-Host "    $($s.Plugin)/$($s.Name): $state"
        }
    }

    return $problems
}

if ($Verify) {
    if (-not $Project) {
        $parent = Split-Path -Parent $ScriptDir
        if ((Test-Path -LiteralPath (Join-Path $parent ".claude")) -or
            (Test-Path -LiteralPath (Join-Path $parent ".codex"))) {
            $Project = $parent
            Write-Host "  Auto-detected workspace: $Project"
        }
    }
    if (-not $Project) {
        Write-Host "-Verify needs a workspace: .\install.ps1 -Verify -Project C:\path\repo"
        exit 2
    }
    if (-not (Test-Path -LiteralPath $Project)) {
        Write-Host "Project path does not exist: $Project"
        exit 2
    }

    $problems = Test-WorkspaceLinks -Project $Project
    if ($problems -gt 0) {
        Write-Host "  Links are out of date: re-run .\install.ps1 -Project <path>"
        exit 1
    }
    Write-Host "  Links are current."
    exit 0
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
            lastUpdated     = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.000Z")
        }
        $known | Add-Member -NotePropertyName "jluo41-tools" -NotePropertyValue $entry -Force
        Write-JsonFile -Path $knownFile -Object $known
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
    # .agents\skills is the tool-neutral root that DeepSeek Harness (dsh) scans.
    if (Test-Path -LiteralPath (Join-Path $Project ".agents")) {
        Install-Skills -SkillsDir (Join-Path $Project ".agents\skills") -Label "Shared agents project"
    }
}

# ─── 3. Global skills (-Global) ──────────────────────────────────────────────
if ($Global) {
    Install-Skills -SkillsDir (Join-Path $ClaudeDir "skills") -Label "global"
    Install-Agents -AgentsDir (Join-Path $ClaudeDir "agents") -Label "global"
}

# ─── 4. Sound hooks (-Hooks) ─────────────────────────────────────────────────
# Same table as install.sh --hooks, read from install-hooks.json.
if ($Hooks) {
    Write-Host ""
    Write-Host "Configuring sound hooks in settings.json..."

    $tablePath = Join-Path $ScriptDir "install-hooks.json"
    if (-not (Test-Path -LiteralPath $tablePath)) {
        Write-Host "  Warning: $tablePath not found. Skipping sound hooks."
    } else {
        $spec = (Get-Content -Raw -LiteralPath $tablePath | ConvertFrom-Json).windows
        $settingsFile = Join-Path $ClaudeDir "settings.json"

        $settings = [pscustomobject]@{}
        if (Test-Path -LiteralPath $settingsFile) {
            $settings = Get-Content -Raw -LiteralPath $settingsFile | ConvertFrom-Json
        } else {
            New-Item -ItemType Directory -Force -Path $ClaudeDir | Out-Null
        }

        $hooksObj = [pscustomobject]@{}
        $missing = 0
        # $ev, not $event: $event is a PowerShell automatic variable.
        foreach ($ev in $spec.sounds.PSObject.Properties) {
            $sound = $ev.Value
            if (-not (Test-Path -LiteralPath $sound)) { $missing++ }
            $cmd = $spec.command.Replace("{sound}", $sound)
            # [object[]] casts are deliberate: a one-element array can be unrolled
            # on its way through Add-Member, and settings.json needs arrays here.
            $inner = [object[]]@([pscustomobject]@{ type = "command"; command = $cmd; async = $true })
            $hooksObj | Add-Member -NotePropertyName $ev.Name -NotePropertyValue ([object[]]@(
                [pscustomobject]@{ matcher = "*"; hooks = $inner }
            )) -Force
        }

        # Overwrite the hooks section, preserve everything else.
        $settings | Add-Member -NotePropertyName "hooks" -NotePropertyValue $hooksObj -Force
        Write-JsonFile -Path $settingsFile -Object $settings

        Write-Host "  OS: $($spec.label)"
        Write-Host "  Configured $(@($spec.sounds.PSObject.Properties).Count) sound hooks:"
        foreach ($ev in $spec.sounds.PSObject.Properties) {
            Write-Host ("    {0,-22} -> {1}" -f $ev.Name, (Split-Path -Leaf $ev.Value))
        }
        if ($missing -gt 0) {
            Write-Host "  Note: $missing sound file(s) not found on this machine; those hooks stay silent."
        }
        Write-Host "  Sound hooks installed."
    }
}

# ─── Summary ─────────────────────────────────────────────────────────────────
# Plugin names are READ from plugins/*/.claude-plugin/plugin.json, not typed
# here: the hand-written line named 4 plugins when there were 7, and install.sh's
# named a `diagram-skill` that no longer exists.
Write-Host ""
Write-Host "Done. Available plugins:"
foreach ($d in (Get-ChildItem -LiteralPath $PluginsRoot -Directory | Sort-Object Name)) {
    if ($d.Name.StartsWith("_") -or $d.Name.StartsWith(".")) { continue }
    $man = Join-Path $d.FullName ".claude-plugin\plugin.json"
    $name = $d.Name; $desc = "(no plugin.json; not installable as a plugin)"
    if (Test-Path -LiteralPath $man) {
        try {
            $m = Get-Content -Raw -LiteralPath $man | ConvertFrom-Json
            if ($m.name) { $name = $m.name }
            $desc = ($m.description -replace '\s+', ' ')
            if ($desc.Length -gt 96) { $desc = $desc.Substring(0, 96) }
        } catch { $desc = "(unreadable plugin.json)" }
    }
    Write-Host ("  {0,-18}- {1}" -f $name, $desc)
}
Write-Host ""
Write-Host "Install in Claude Code with e.g.: /plugin install haipipe@jluo41-tools"
Write-Host ""
Write-Host "Run with flags for more:"
Write-Host "  .\install.ps1 -Global           Link skills into ~\.claude\skills"
Write-Host "  .\install.ps1 -Project <path>   Link skills into <path>\.claude, .codex and .agents\skills"
Write-Host "  .\install.ps1 -Hooks            Configure sound hooks in settings.json"
Write-Host "  .\install.ps1 -Verify -Project <path>  Audit a workspace's links (writes nothing)"
Write-Host "  .\install.ps1 -All              Do everything (marketplace + global + hooks)"
Write-Host "  .\install.ps1 -NoMarketplace    Skip marketplace registration"
