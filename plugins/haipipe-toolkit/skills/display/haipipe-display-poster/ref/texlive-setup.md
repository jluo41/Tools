# TeX Live Setup (LaTeX not installed)

If `pdflatex` / `latexmk` are missing, try in order:

```bash
# Option 1: brew cask (requires sudo — may fail in non-interactive shells)
brew install --cask mactex-no-gui

# Option 2: BasicTeX (smaller, may still need sudo)
brew install --cask basictex

# Option 3: User-directory install (NO sudo needed — always works)
curl -L https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz | tar xz
cd install-tl-*
cat > texlive.profile << 'PROF'
selected_scheme scheme-basic
TEXDIR ~/texlive/YYYY
TEXMFLOCAL ~/texlive/texmf-local
TEXMFSYSCONFIG ~/texlive/YYYY/texmf-config
TEXMFSYSVAR ~/texlive/YYYY/texmf-var
TEXMFHOME ~/texmf
binary_x86_64-darwin 1
instopt_adjustpath 0
instopt_adjustrepo 1
instopt_write18_restricted 1
tlpdbopt_autobackup 1
tlpdbopt_install_docfiles 0
tlpdbopt_install_srcfiles 0
PROF
./install-tl --profile=texlive.profile
export PATH="$HOME/texlive/YYYY/bin/universal-darwin:$PATH"
```

After installation, install required packages:

```bash
tlmgr install tcolorbox pgf etoolbox environ trimspaces \
  type1cm pdfcol tikzfill latexmk lm enumitem geometry
```

> ⚠️ **Lesson learned**: `brew install --cask mactex-no-gui` often fails in non-interactive shells because the macOS installer requires sudo password. The user-directory TeX Live install (Option 3) always works without sudo.

> ⚠️ **Do NOT install or use `beamerposter`**. The article class approach does not need it.
