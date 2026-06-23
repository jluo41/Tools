# 1-diff/.gitignore — drop into your paper's 1-diff/ directory
#
# Snapshots and build artifacts are regenerated on every run. The PDF, .tex,
# silenced-changes.txt, and config.sh are the durable artifacts; everything
# else can be wiped without loss.

# Snapshots — regenerate from git on demand
*/old/
*/new/

# Build intermediates
*/0-display
*/*.aux
*/*.bbl
*/*.blg
*/*.log
*/*.ent
*/*.out
*/*.toc
*/*.lof
*/*.lot
*/*.fls
*/*.fdb_latexmk
*/*.synctex.gz
*/.p*.log
*/.b.log

# Borrowed support files (regenerated each run)
*/*.bib
*/*.cls
*/*.bst
*/*.sty

# Backup files
*.bak

# Pre-flight test artifacts
pre-flight/
