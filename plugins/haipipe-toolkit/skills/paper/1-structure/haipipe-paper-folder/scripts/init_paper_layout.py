#!/usr/bin/env python3
"""Scaffold a paper folder matching the proven Paper-<Name>-<Venue><Year> layout.

Usage:
    python init_paper_layout.py <root> --name MapPhyTrait --venue npjDM2025 --format IRDM
    python init_paper_layout.py <root> --name Personality2Opioid --venue MISQ2026 --format IS
    python init_paper_layout.py <root> --name MapPhyTrait --venue npjDM2025 --format IRDM --dry-run
"""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path


# ---------------------------------------------------------------------------
# Section templates per venue format
# ---------------------------------------------------------------------------

SECTIONS_IRDM = [
    ("00_abstract.tex", ""),
    ("01_introduction.tex", ""),
    ("02_results.tex", "% Results meta-file: add \\input{{0-sections/02-NN_slug}} per subsection\n"),
    ("03_discussion.tex", ""),
    ("04_methods.tex", "% Methods meta-file: add \\input{{0-sections/04-NN_slug}} per subsection\n"),
    ("05_back-matter.tex", textwrap.dedent("""\
        % Data Availability, Code Availability, Acknowledgements,
        % Author Contributions, Competing Interests
    """)),
]

SECTIONS_IMRD = [
    ("00_abstract.tex", ""),
    ("01_introduction.tex", ""),
    ("02_methods.tex", "% Methods meta-file: add \\input{{0-sections/02-NN_slug}} per subsection\n"),
    ("03_results.tex", "% Results meta-file: add \\input{{0-sections/03-NN_slug}} per subsection\n"),
    ("04_discussion.tex", ""),
    ("05_back-matter.tex", textwrap.dedent("""\
        % Data Availability, Code Availability, Acknowledgements,
        % Author Contributions, Competing Interests
    """)),
]

SECTIONS_IS = [
    ("0-abstract.tex", ""),
    ("01_introduction.tex", ""),
    ("02_literature_review.tex", ""),
    ("03_theoretical_framework.tex", ""),
    ("04_personality_extraction.tex", "% Data/method meta-file: add \\input{{0-sections/04-N_slug}} per subsection\n"),
    ("05_data_variables.tex", "% Data meta-file: add \\input{{0-sections/05-N_slug}} per subsection\n"),
    ("06_empirical_analysis.tex", "% Analysis meta-file: add \\input{{0-sections/06-N_slug}} per subsection\n"),
    ("08_discussion.tex", ""),
    ("09_conclusion.tex", ""),
    ("A_llm_prompts.tex", "% Appendix A\n"),
    ("B_robustness_tables.tex", "% Appendix B\n"),
]

FORMAT_MAP = {
    "IRDM": SECTIONS_IRDM,
    "IMRD": SECTIONS_IMRD,
    "IS": SECTIONS_IS,
}


# ---------------------------------------------------------------------------
# Directory skeleton
# ---------------------------------------------------------------------------

DEFAULT_DIRS = [
    "0-lifecycle/0-seed",
    "0-lifecycle/1-pitch",
    "0-lifecycle/2-claims",
    "0-lifecycle/3-narrative",
    "0-lifecycle/4-figures-tables",
    "0-lifecycle/5-minimap",
    "0-sections",
    "0-displays/display01-placeholder/assets",
    "0-displays/display01-placeholder/source",
    "0-displays/display01-placeholder/versions",
    "1-rounds",
]


# ---------------------------------------------------------------------------
# Template generators
# ---------------------------------------------------------------------------

def sections_readme(name: str, venue: str, fmt: str, sections: list) -> str:
    lines = [
        f"# Paper Sections Directory",
        "",
        f"Paper: {name} ({venue}, {fmt} format)",
        "",
        "Section files contain ONLY content -- the main .tex handles \\section{{}} headers.",
        "Meta-files (e.g. 02_results.tex) list subsections via \\input{{}}.",
        "Subsections use NN-MM_slug.tex naming (e.g. 02-01_dataset-characteristics.tex).",
        "SI sections use letter prefix (A_, B_, C_, ...).",
        "",
        "## Sections",
    ]
    for filename, _ in sections:
        lines.append(f"- `{filename}`")
    return "\n".join(lines) + "\n"


def main_tex(name: str, venue: str, fmt: str, sections: list) -> str:
    header = textwrap.dedent(f"""\
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %% {name} -- {venue}
        %% Master LaTeX file with modular sections
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        % !TEX root = 0-{name}-{venue}.tex
        \\documentclass{{article}}
        % \\usepackage{{arxiv}}  % uncomment or replace with venue style

        % Core packages
        \\usepackage[utf8]{{inputenc}}
        \\usepackage{{amsmath}}
        \\usepackage{{amsfonts}}
        \\usepackage{{amssymb}}
        \\usepackage{{graphicx}}
        \\usepackage{{booktabs}}
        \\usepackage{{multirow}}
        \\usepackage{{xcolor}}
        \\usepackage{{subcaption}}
        \\usepackage{{hyperref}}
        \\usepackage{{geometry}}
        \\usepackage{{float}}
        \\usepackage{{array}}
        \\usepackage{{enumitem}}

        \\geometry{{margin=1in}}

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %% Title and author information
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        \\title{{\\textbf{{{name}}}}}
        \\author{{Author Name}}
        \\date{{}}

        \\begin{{document}}
        \\maketitle

    """)

    body_lines = []
    for filename, _ in sections:
        sec_name = filename.replace(".tex", "")
        if sec_name.startswith("A_") or sec_name.startswith("B_") or sec_name.startswith("C_"):
            continue
        if sec_name == "00_abstract":
            body_lines.append("\\begin{abstract}")
            body_lines.append(f"\\input{{0-sections/{sec_name}}}")
            body_lines.append("\\end{abstract}")
            body_lines.append("")
        elif sec_name == "0-abstract":
            body_lines.append("\\begin{abstract}")
            body_lines.append(f"\\input{{0-sections/{sec_name}}}")
            body_lines.append("\\end{abstract}")
            body_lines.append("")
        else:
            label = sec_name.split("_", 1)[-1].replace("_", " ").title()
            if sec_name.startswith("05_back"):
                body_lines.append(f"% Back-matter (no \\section header)")
                body_lines.append(f"\\input{{0-sections/{sec_name}}}")
            else:
                body_lines.append(f"\\section{{{label}}}")
                body_lines.append(f"\\input{{0-sections/{sec_name}}}")
            body_lines.append("")

    bib_name = f"0-{name}-{venue}"
    footer = textwrap.dedent(f"""\
        \\bibliographystyle{{plain}}
        \\bibliography{{{bib_name}}}

        \\end{{document}}
    """)

    return header + "\n".join(body_lines) + "\n\n" + footer


def bib_file(name: str, venue: str) -> str:
    return f"% Bibliography for {name} ({venue})\n% Add entries below\n"


def compile_sh() -> str:
    return textwrap.dedent("""\
        #!/bin/bash
        # LaTeX Compilation Script with Auto-cleanup and Auto-discovery
        # Usage: ./1-compile.sh [options]
        #   -c, --clean-only    Only clean auxiliary files, don't compile
        #   -k, --keep         Keep auxiliary files after compilation
        #   -h, --help         Show this help message

        set -e

        # If not in the paper directory, search upward
        find_compile_script() {
            local dir="$(pwd)"
            while [ "$dir" != "/" ]; do
                if [ -f "$dir/1-compile.sh" ]; then echo "$dir"; return 0; fi
                dir=$(dirname "$dir")
            done
            return 1
        }
        if [ ! -f "$(pwd)/1-compile.sh" ]; then
            PAPER_DIR=$(find_compile_script)
            if [ -z "$PAPER_DIR" ]; then echo "Error: Could not find 1-compile.sh"; exit 1; fi
            cd "$PAPER_DIR"
            exec bash "$PAPER_DIR/1-compile.sh" "$@"
        fi

        RED='\\033[0;31m'; GREEN='\\033[0;32m'; YELLOW='\\033[1;33m'; NC='\\033[0m'

        # Auto-detect master tex files (every 0-*.tex, excluding -DIFF)
        MAIN_TEXS=()
        while IFS= read -r _tex; do MAIN_TEXS+=("$_tex"); done < <(ls 0-*.tex 2>/dev/null | grep -v -- '-DIFF')
        if [ ${#MAIN_TEXS[@]} -eq 0 ]; then echo -e "${RED}No 0-*.tex file found!${NC}"; exit 1; fi

        CLEAN_ONLY=false; KEEP_AUX=false
        while [[ $# -gt 0 ]]; do
            case $1 in
                -c|--clean-only) CLEAN_ONLY=true; shift;;
                -k|--keep) KEEP_AUX=true; shift;;
                -h|--help) echo "Usage: ./1-compile.sh [-c|--clean-only] [-k|--keep]"; exit 0;;
                *) echo "Unknown option: $1"; exit 1;;
            esac
        done

        clean_aux_files() {
            echo -e "${YELLOW}Cleaning auxiliary files...${NC}"
            rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk \\
                  *.synctex.gz *.blg *.bbl *.bcf *.run.xml *.xdv \\
                  *.nav *.snm *.vrb *.thm
            rm -f 0-sections/*.aux
            echo -e "${GREEN}Auxiliary files cleaned${NC}"
        }

        cleanup_on_exit() { if [ "$KEEP_AUX" = false ]; then clean_aux_files; fi; }
        trap cleanup_on_exit EXIT

        if [ "$CLEAN_ONLY" = true ]; then exit 0; fi

        compile_one() {
            local MAIN_TEX="$1"
            local PDF_NAME="${MAIN_TEX%.tex}.pdf"
            echo -e "${GREEN}Compiling ${MAIN_TEX} ...${NC}"
            echo -e "${YELLOW}[1/4] First pdflatex pass...${NC}"
            pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1 || true
            echo -e "${YELLOW}[2/4] Running bibtex...${NC}"
            bibtex "${MAIN_TEX%.tex}" > /dev/null 2>&1 || true
            echo -e "${YELLOW}[3/4] Second pdflatex pass...${NC}"
            pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1 || true
            echo -e "${YELLOW}[4/4] Final pdflatex pass...${NC}"
            pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1 || true
            if [ -f "$PDF_NAME" ]; then
                local PDF_SIZE; PDF_SIZE=$(ls -lh "$PDF_NAME" | awk '{print $5}')
                echo -e "${GREEN}Done: ${PDF_NAME} (${PDF_SIZE})${NC}"
            else
                echo -e "${RED}Failed: ${PDF_NAME} was not generated${NC}"
                COMPILE_FAILED=1
            fi
        }

        COMPILE_FAILED=0
        for _tex in "${MAIN_TEXS[@]}"; do compile_one "$_tex"; echo ""; done
        if [ "$COMPILE_FAILED" != 0 ]; then exit 1; fi
    """)


def compile_ps1() -> str:
    return textwrap.dedent("""\
        <#
        .SYNOPSIS
            LaTeX compilation script (PowerShell) with auto-cleanup and auto-discovery.
        .PARAMETER CleanOnly
            Only clean auxiliary files, don't compile.
        .PARAMETER Keep
            Keep auxiliary files after compilation.
        #>
        [CmdletBinding()]
        param(
            [Alias('c')][switch]$CleanOnly,
            [Alias('k')][switch]$Keep
        )

        $ErrorActionPreference = 'Stop'
        $PaperDir = $PSScriptRoot
        if (-not $PaperDir) { $PaperDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
        Set-Location $PaperDir

        $MainTexs = @(Get-ChildItem -File -Filter '0-*.tex' | Where-Object { $_.Name -notmatch '-DIFF' })
        if ($MainTexs.Count -eq 0) { Write-Host 'No 0-*.tex file found!' -ForegroundColor Red; exit 1 }

        function Clear-AuxFiles {
            Write-Host 'Cleaning auxiliary files...' -ForegroundColor Yellow
            $exts = '*.aux','*.log','*.out','*.toc','*.lof','*.lot','*.fls','*.fdb_latexmk',
                    '*.synctex.gz','*.blg','*.bbl','*.bcf','*.run.xml','*.xdv',
                    '*.nav','*.snm','*.vrb','*.thm'
            foreach ($e in $exts) {
                Get-ChildItem -File -Filter $e -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
            }
            if (Test-Path '0-sections') {
                Get-ChildItem -Path '0-sections' -File -Filter '*.aux' -ErrorAction SilentlyContinue |
                    Remove-Item -Force -ErrorAction SilentlyContinue
            }
            Write-Host 'Auxiliary files cleaned' -ForegroundColor Green
        }

        if ($CleanOnly) { Clear-AuxFiles; exit 0 }

        if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
            Write-Host 'pdflatex not found on PATH.' -ForegroundColor Red
            Write-Host '  winget install MiKTeX.MiKTeX' -ForegroundColor Yellow
            exit 1
        }

        function Invoke-Quiet([string]$exe, [string[]]$exeArgs) { & $exe @exeArgs *> $null }

        function Invoke-CompileOne([string]$MainTexName) {
            $base = [System.IO.Path]::GetFileNameWithoutExtension($MainTexName)
            $pdfName = "$base.pdf"
            Write-Host "Compiling $MainTexName ..." -ForegroundColor Green
            Write-Host '[1/4] First pdflatex pass...'  -ForegroundColor Yellow
            Invoke-Quiet pdflatex @('-interaction=nonstopmode', $MainTexName)
            Write-Host '[2/4] Running bibtex...'        -ForegroundColor Yellow
            Invoke-Quiet bibtex @($base)
            Write-Host '[3/4] Second pdflatex pass...'  -ForegroundColor Yellow
            Invoke-Quiet pdflatex @('-interaction=nonstopmode', $MainTexName)
            Write-Host '[4/4] Final pdflatex pass...'   -ForegroundColor Yellow
            Invoke-Quiet pdflatex @('-interaction=nonstopmode', $MainTexName)
            if (Test-Path $pdfName) {
                $size = '{0:N0} KB' -f ([math]::Ceiling((Get-Item $pdfName).Length / 1KB))
                Write-Host "Done: $pdfName ($size)" -ForegroundColor Green
                return $true
            } else {
                Write-Host "Failed: $pdfName was not generated" -ForegroundColor Red
                return $false
            }
        }

        Write-Host 'Starting LaTeX compilation...' -ForegroundColor Green
        $AllOk = $true
        foreach ($tex in $MainTexs) {
            if (-not (Invoke-CompileOne $tex.Name)) { $AllOk = $false }
            Write-Host ''
        }
        if (-not $AllOk) {
            if (-not $Keep) { Clear-AuxFiles }
            exit 1
        }
        if (-not $Keep) { Write-Host ''; Clear-AuxFiles }
        Write-Host 'Done!' -ForegroundColor Green
    """)


def gitignore_content() -> str:
    return textwrap.dedent("""\
        # macOS
        .DS_Store

        # LaTeX build artifacts
        *.aux
        *.log
        *.out
        *.pdf
        # but keep figure / table PDFs under 0-displays/
        !0-displays/**/*.pdf
        # and keep submission-bundle PDFs for any revision round
        !1-rounds/*/submission/**/*.pdf
        # and keep the rebuttal-report PDF for any revision round
        !1-rounds/*/rebuttal-report/**/*.pdf
        # and keep the diff PDFs for any revision round
        !1-rounds/*/diff/**/*.pdf
        *.synctex.gz
        *.fdb_latexmk
        *.fls
        *.toc
        *.bbl
        *.blg
        *.bcf
        *.run.xml

        # Editor directories
        .vscode/

        # Old files
        _old/
    """)


def config_yaml(name: str, venue: str) -> str:
    return textwrap.dedent(f"""\
        ##############################################
        # Paper config: {name} ({venue})
        ##############################################

        DisplayPath: '0-displays'
        ActiveRound: 'v000000'
    """)


def status_md(name: str, venue: str) -> str:
    return textwrap.dedent(f"""\
        # Paper Status

        Paper: {name} ({venue})

        | Field | Value |
        |---|---|
        | current_layer | 0-seed |
        | maturity | scaffold |
        | active_round | none |
        | next_gate | fill 0-lifecycle/0-seed and 1-pitch |

        ## Open Gates

        - Seed, pitch, claims, display map, and minimap need author content.
    """)


def lifecycle_readme(name: str, venue: str) -> str:
    return textwrap.dedent(f"""\
        # Paper Lifecycle

        Paper: {name} ({venue})

        This folder is the TeX-first paper maturation spine.

        ```text
        0-seed -> 1-pitch -> 2-claims -> 3-narrative -> 4-figures-tables -> 5-minimap
        ```

        Each stage owns one reviewable `.tex` file and may compile to its own
        PDF when useful.
    """)


def lifecycle_stage_tex(stage: str, title: str, body: str) -> str:
    return textwrap.dedent(f"""\
        \\documentclass{{article}}
        \\usepackage[margin=1in]{{geometry}}
        \\usepackage{{booktabs}}
        \\usepackage{{hyperref}}

        \\title{{{title}}}
        \\date{{}}

        \\begin{{document}}
        \\maketitle

        {body}

        \\end{{document}}
    """)


def seed_tex(name: str, venue: str) -> str:
    return lifecycle_stage_tex(
        "0-seed",
        f"0-seed: {name} ({venue})",
        textwrap.dedent("""\
            \\section*{Seed}

            Why might this paper exist?

            \\section*{Current Evidence}

            List task, probe, discovery, and insight paths that make this
            possibility plausible.

            \\section*{Kill Criteria}

            What evidence would make this paper not worth pursuing?
        """),
    )


def pitch_tex(name: str, venue: str) -> str:
    return lifecycle_stage_tex(
        "1-pitch",
        f"1-pitch: {name} ({venue})",
        textwrap.dedent("""\
            \\section*{One-Minute Pitch}

            One sentence that a non-specialist can repeat after one minute.

            \\section*{Hook}

            Why should a reader care?

            \\section*{Surprise}

            What is non-obvious?

            \\section*{Why Believe}

            What evidence makes the pitch credible?

            \\section*{Still Fragile}

            What is the weakest point?
        """),
    )


def claims_tex(name: str, venue: str) -> str:
    return lifecycle_stage_tex(
        "2-claims",
        f"2-claims: {name} ({venue})",
        textwrap.dedent("""\
            \\section*{Claim Ledger}

            \\begin{tabular}{p{0.12\\linewidth}p{0.34\\linewidth}p{0.18\\linewidth}p{0.25\\linewidth}}
            \\toprule
            ID & Claim & Status & Need / Evidence \\\\
            \\midrule
            C1 & TODO & GAP & TODO: probe/discover/task route \\\\
            \\bottomrule
            \\end{tabular}
        """),
    )


def narrative_tex(name: str, venue: str) -> str:
    return lifecycle_stage_tex(
        "3-narrative",
        f"3-narrative: {name} ({venue})",
        "\\section*{Narrative Arc}\n\nHow do the claims become this paper's story?",
    )


def figures_tables_tex(name: str, venue: str) -> str:
    return lifecycle_stage_tex(
        "4-figures-tables",
        f"4-figures-tables: {name} ({venue})",
        textwrap.dedent("""\
            \\section*{Display Map}

            \\begin{tabular}{p{0.12\\linewidth}p{0.2\\linewidth}p{0.28\\linewidth}p{0.24\\linewidth}}
            \\toprule
            Display & Type & Claim & Source / Status \\\\
            \\midrule
            display01 & TODO & TODO & planned \\\\
            \\bottomrule
            \\end{tabular}
        """),
    )


def minimap_tex(name: str, venue: str) -> str:
    return lifecycle_stage_tex(
        "5-minimap",
        f"5-minimap: {name} ({venue})",
        textwrap.dedent("""\
            \\section*{Paragraph Minimap}

            \\begin{tabular}{p{0.12\\linewidth}p{0.25\\linewidth}p{0.25\\linewidth}p{0.22\\linewidth}}
            \\toprule
            Section & Paragraph job & Evidence anchor & Display \\\\
            \\midrule
            Intro P1 & TODO & TODO & none \\\\
            \\bottomrule
            \\end{tabular}
        """),
    )


def round_latest() -> str:
    return textwrap.dedent("""\
        # Latest Round

        active_round: none

        Start a dated round as `1-rounds/vYYMMDD/` when discussion, review,
        decisions, or applied edits need to be tracked.
    """)


def display_readme(name: str, venue: str) -> str:
    return textwrap.dedent(f"""\
        # Displays

        Paper: {name} ({venue})

        | ID | Type | Claim | Evidence Source | Section | Status | Canonical PDF |
        |---|---|---|---|---|---|---|
        | display01 | TODO | TODO | TODO | TODO | planned | TODO |
    """)


def display_unit_readme(name: str, venue: str) -> str:
    return textwrap.dedent(f"""\
        # display01-placeholder

        Paper: {name} ({venue})

        ## Purpose
        TODO

        ## Claim
        TODO

        ## Evidence Source
        TODO

        ## Exports
        - `preview.pdf`: TODO

        ## Status
        planned
    """)


def display_index(name: str, venue: str) -> str:
    return textwrap.dedent(f"""\
        # Display Index

        Paper: {name} ({venue})

        This file is the display contract for every figure and table the paper
        uses. A display item is not just an asset; it is a story/evidence object.

        ## Display Table

        | ID | Type | Role | Claim | Evidence Source | Section | Status |
        |----|------|------|-------|-----------------|---------|--------|
        | Fig 1 | hero figure | one-minute story | core contribution | `0-lifecycle/1-pitch/1-pitch.tex` | Introduction | planned |
        | Table 1 | result table | benchmark comparison | [claim] | [task/probe/result path] | Results | planned |

        ## Status Vocabulary

        - `planned`: the paper needs this display, but evidence or rendering is not ready.
        - `data-ready`: source data or evidence exists.
        - `rendered`: visual asset or table body exists.
        - `input-ready`: `float.tex` exists and can be `\\input` by a section.
        - `inserted`: a section file inputs the display.
        - `reviewed`: claim, caption, label, numbers, and placement passed review.

        ## Display Item Contract

        Each major display may have its own folder:

        ```text
        0-displays/display01-hero/
          README.md
          assets/figure.pdf
          float.tex
          preview.tex
          preview.pdf
          source/
          versions/

        0-displays/display02-main-results/
          README.md
          assets/table-body.tex
          float.tex
          preview.tex
          preview.pdf
          source/
          versions/
        ```

        The main paper should input `float.tex`, not copy/paste display code.
        The preview PDF is for human review; the clean visual asset should not
        bake in the caption.
    """)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a paper folder matching the Paper-<Name>-<Venue><Year> layout."
    )
    parser.add_argument("root", help="Paper project root directory")
    parser.add_argument("--name", required=True, help="Paper short name (e.g. MapPhyTrait)")
    parser.add_argument("--venue", required=True, help="Venue+year tag (e.g. npjDM2025, MISQ2026)")
    parser.add_argument("--format", dest="fmt", default="IRDM",
                        choices=["IRDM", "IMRD", "IS"],
                        help="Section format (default: IRDM)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report planned changes without writing")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    sections = FORMAT_MAP[args.fmt]
    created = []
    reused = []

    def track_dir(rel: str) -> None:
        target = root / rel
        if target.exists():
            reused.append(rel)
        else:
            created.append(rel)
            if not args.dry_run:
                target.mkdir(parents=True, exist_ok=True)

    def track_file(rel: str, content: str) -> None:
        target = root / rel
        if target.exists():
            reused.append(rel)
        else:
            created.append(rel)
            if not args.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")

    # 1. Directories
    for d in DEFAULT_DIRS:
        track_dir(d)

    # 1a. Paper status, lifecycle, rounds, and display index
    track_file("STATUS.md", status_md(args.name, args.venue))
    track_file("0-lifecycle/README.md", lifecycle_readme(args.name, args.venue))
    track_file("0-lifecycle/0-seed/0-seed.tex", seed_tex(args.name, args.venue))
    track_file("0-lifecycle/1-pitch/1-pitch.tex", pitch_tex(args.name, args.venue))
    track_file("0-lifecycle/2-claims/2-claims.tex", claims_tex(args.name, args.venue))
    track_file("0-lifecycle/3-narrative/3-narrative.tex", narrative_tex(args.name, args.venue))
    track_file("0-lifecycle/4-figures-tables/4-figures-tables.tex", figures_tables_tex(args.name, args.venue))
    track_file("0-lifecycle/5-minimap/5-minimap.tex", minimap_tex(args.name, args.venue))
    track_file("1-rounds/latest.md", round_latest())
    track_file("0-displays/README.md", display_readme(args.name, args.venue))
    track_file("0-displays/display01-placeholder/README.md", display_unit_readme(args.name, args.venue))

    # 2. Section stubs
    for filename, stub in sections:
        track_file(f"0-sections/{filename}", stub)
    track_file(
        "0-sections/README.md",
        sections_readme(args.name, args.venue, args.fmt, sections),
    )

    # 3. Root source files
    track_file(
        f"0-{args.name}-{args.venue}.tex",
        main_tex(args.name, args.venue, args.fmt, sections),
    )
    track_file(
        f"0-{args.name}-{args.venue}.bib",
        bib_file(args.name, args.venue),
    )

    # 4. Process files
    track_file("1-compile.sh", compile_sh())
    track_file("1-compile.ps1", compile_ps1())
    track_file(".gitignore", gitignore_content())
    track_file("1-config.yaml", config_yaml(args.name, args.venue))

    # 5. Report
    print(f"root: {root}")
    print(f"venue: {args.venue}  format: {args.fmt}")
    print(f"main tex: 0-{args.name}-{args.venue}.tex")
    if args.dry_run:
        print("(dry run -- no files written)")
    print(f"\ncreated ({len(created)}):")
    for p in sorted(created):
        print(f"  {p}")
    print(f"\nreused ({len(reused)}):")
    for p in sorted(reused):
        print(f"  {p}")


if __name__ == "__main__":
    main()
