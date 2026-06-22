#!/bin/bash
# LaTeX Compilation Script with Auto-cleanup and Auto-discovery
# Usage: ./1-compile.sh [options]
#   -c, --clean-only    Only clean auxiliary files, don't compile
#   -k, --keep          Keep auxiliary files after compilation
#   -h, --help          Show this help message
#
# This script is smart: if called from a subdirectory, it will find itself
# in parent directories and re-run from the correct location automatically.

set -e  # Exit on error

# Function to find this script by searching upward
find_compile_script() {
    local dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/1-compile.sh" ]; then
            echo "$dir"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    return 1
}

# If this script is not in the current directory, find it and re-run from there
if [ ! -f "$(pwd)/1-compile.sh" ]; then
    PAPER_DIR=$(find_compile_script)
    if [ -z "$PAPER_DIR" ]; then
        echo "Error: Could not find 1-compile.sh in any parent directory"
        exit 1
    fi
    echo "📄 Found paper directory: $(basename "$PAPER_DIR")"
    cd "$PAPER_DIR"
    exec bash "$PAPER_DIR/1-compile.sh" "$@"
fi

# Now we're in the correct directory - proceed with compilation
SCRIPT_DIR="$(pwd)"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Auto-detect master tex files (every 0-*.tex, excluding generated -DIFF files).
# The paper may be TWO documents: the main manuscript and the standalone
# Supplementary Information. Both are compiled when present.
MAIN_TEXS=()
while IFS= read -r _tex; do MAIN_TEXS+=("$_tex"); done < <(ls 0-*.tex 2>/dev/null | grep -v -- '-DIFF')
if [ ${#MAIN_TEXS[@]} -eq 0 ]; then
    echo -e "${RED}No 0-*.tex file found!${NC}"
    exit 1
fi

# Parse arguments
CLEAN_ONLY=false
KEEP_AUX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--clean-only)
            CLEAN_ONLY=true
            shift
            ;;
        -k|--keep)
            KEEP_AUX=true
            shift
            ;;
        -h|--help)
            echo "LaTeX Compilation Script with Auto-cleanup"
            echo "Usage: ./1-compile.sh [options]"
            echo ""
            echo "Options:"
            echo "  -c, --clean-only    Only clean auxiliary files, don't compile"
            echo "  -k, --keep          Keep auxiliary files after compilation"
            echo "  -h, --help          Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Function to clean auxiliary files
clean_aux_files() {
    echo -e "${YELLOW}Cleaning auxiliary files...${NC}"

    # Remove common LaTeX auxiliary files
    rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk \
          *.synctex.gz *.blg *.bbl *.bcf *.run.xml *.xdv \
          *.nav *.snm *.vrb *.thm

    # Remove auxiliary files in subdirectories
    rm -f 0-displays/*/*.aux
    rm -f 0-sections/*.aux

    echo -e "${GREEN}✓ Auxiliary files cleaned${NC}"
}

# Clearing aux files is the DEFAULT action: run it on ANY exit (success,
# failure, or Ctrl-C interrupt) unless --keep was passed. The trap guarantees
# the working tree is left clean no matter how the script ends.
cleanup_on_exit() {
    if [ "$KEEP_AUX" = false ]; then
        clean_aux_files
    fi
}
trap cleanup_on_exit EXIT

# Clean-only mode: skip compilation; the EXIT trap performs the cleanup.
if [ "$CLEAN_ONLY" = true ]; then
    exit 0
fi

# Compile one master tex through the standard 4-pass + bibtex pipeline.
compile_one() {
    local MAIN_TEX="$1"
    local PDF_NAME="${MAIN_TEX%.tex}.pdf"
    echo -e "${GREEN}Compiling ${MAIN_TEX} ...${NC}"

    echo -e "${YELLOW}[1/4] First pdflatex pass...${NC}"
    pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1 || true
    echo -e "${YELLOW}[2/4] Running bibtex...${NC}"
    bibtex "${MAIN_TEX%.tex}" > /dev/null 2>&1 || echo -e "${YELLOW}⚠ BibTeX warnings (non-critical)${NC}"
    echo -e "${YELLOW}[3/4] Second pdflatex pass...${NC}"
    pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1 || true
    echo -e "${YELLOW}[4/4] Final pdflatex pass...${NC}"
    pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null 2>&1 || true

    if [ -f "$PDF_NAME" ]; then
        local PDF_SIZE PDF_PAGES
        PDF_SIZE=$(ls -lh "$PDF_NAME" | awk '{print $5}')
        PDF_PAGES=$(pdfinfo "$PDF_NAME" 2>/dev/null | grep "Pages:" | awk '{print $2}')
        echo -e "${GREEN}✓ ${PDF_NAME}${NC} (${PDF_SIZE}, ${PDF_PAGES} pages)"
    else
        echo -e "${RED}✗ ${PDF_NAME} was not generated${NC}"
        COMPILE_FAILED=1
    fi
}

# Compile LaTeX (all detected masters: main + SI)
echo -e "${GREEN}Starting LaTeX compilation...${NC}"
echo ""
COMPILE_FAILED=0
for _tex in "${MAIN_TEXS[@]}"; do
    compile_one "$_tex"
    echo ""
done

# (aux cleanup happens automatically via the EXIT trap)
if [ "$COMPILE_FAILED" = 0 ]; then
    echo -e "${GREEN}Done!${NC}"
else
    echo -e "${RED}Some PDFs failed to generate.${NC}"
    exit 1
fi
