Skill: notebook-cell-python
===========================

Manage the complete pipeline from Python scripts to notebooks to markdown documentation.

---

Overview
========

This skill manages a 4-stage pipeline for evaluation analysis:

```
scripts/1-topic.py  →  notebooks/1-topic.ipynb  →  markdowns/1-topic.md  →  docs/1-topic.md
   (source)              (interactive)              (full content)          (workflow diagram)
      ↓                      ↓                          ↓                       ↓
   Run as .py           Explore in Jupyter      Auto-convert from nb    🤖 LLM generates
                                                                          ASCII workflow
                                                                          & function tree
```

**Stage 1: Python Script** (`evaluation/scripts/`)
- Source of truth
- Runnable standalone: `python evaluation/scripts/1-topic.py`
- Uses `# %%` cell markers for structure
- Works in automated pipelines

**Stage 2: Jupyter Notebook** (`evaluation/notebooks/`)
- Interactive version
- Open in Jupyter/VSCode
- Cell-by-cell execution
- Debugging and exploration

**Stage 3: Full Markdown** (`evaluation/markdowns/`)
- Complete notebook as markdown
- Auto-generated: `jupyter nbconvert --to markdown`
- Includes code, outputs, and visualizations
- Same content as notebook

**Stage 4: Documentation Markdown** (`evaluation/docs/`)
- 🤖 **LLM-generated** ASCII workflow diagrams
- Visualize script structure and function relationships
- LLM reads script and creates code documentation
- For quick code understanding (not data analysis results)

---

When to Use
===========

- User wants to create a new evaluation analysis
- User asks to set up the complete pipeline
- User needs to convert scripts through all stages
- User wants to generate documentation with ASCII graphs
- User asks "how do I structure my analysis workflow?"

**Examples:**
- "Create a new analysis for model comparison"
- "Convert my script to notebook and markdown"
- "Generate ASCII graph documentation"
- "Set up the pipeline for this analysis"

---

The 10 Rules for Pipeline-Ready Scripts
========================================

1. **Cell-Based Structure**
   - Use `# %%` markers to separate logical sections
   - Each cell should be self-contained and runnable
   - Cells execute sequentially (top to bottom)

2. **Runnable as Script**
   - Must work standalone: `python scripts/X-topic.py`
   - No notebook-specific code in the script
   - Use standard Python (no magic commands)

3. **Convertible to Notebook**
   - Cell markers convert to notebook cells
   - Output captured for markdown conversion
   - Plots saved to files for documentation

4. **Clear Output**
   - Print progress markers with `print("="*80)`
   - Show intermediate results
   - Save figures with descriptive names

5. **Reproducible**
   - Load config from `1-config.yaml`
   - Set explicit random seeds
   - Document data dependencies

6. **Self-Documenting**
   - Docstring at top explaining purpose
   - Comments for complex logic
   - Print statements showing progress

7. **Relative Paths**
   - Use `Path.cwd()` for repo root
   - Make paths relative to config
   - No hard-coded absolute paths

8. **Error Handling**
   - Check file existence before loading
   - Graceful handling of missing data
   - Helpful error messages

9. **Visualization-Friendly**
   - Generate ASCII graphs/tables where useful
   - Save plots as files (PNG/PDF)
   - Use matplotlib for figures

10. **Documentation-Ready**
    - Structure output for docs extraction
    - Use consistent formatting for graphs
    - Label all visualizations clearly

---

Standard Pipeline Structure
============================

**File Organization:**

```
evaluation/
├── scripts/
│   ├── 0-convert-Result-to-model-task-instance-score.py
│   ├── 1-describe-model-result-data-quality.py
│   ├── 2-generate-Table1-and-Table2.py
│   └── 5-demo-figure.py
├── notebooks/
│   ├── 0-convert-Result-to-model-task-instance-score.ipynb
│   ├── 1-describe-model-result-data-quality.ipynb
│   └── 5-demo-figure.ipynb
├── markdowns/
│   ├── 1-describe-model-result-data-quality.md
│   └── 5-demo-figure.md
└── docs/
    ├── 1-describe-model-result-data-quality.md (ASCII graphs)
    └── 5-demo-figure.md (ASCII graphs)
```

**Naming Convention:**
- Use consistent numbering: `0-`, `1-`, `2-`, etc.
- Descriptive names: `1-describe-model-result-data-quality`
- Same name across all stages

---

Stage 1: Python Script Structure
=================================

Every script should follow this structure (pseudo-code pattern):

```python
#!/usr/bin/env python3
"""
Title: Brief description of what this analysis does

Input:  path/to/input/data.csv
Output: path/to/output/results/
"""

# %% [markdown]
# # Analysis Title
# Brief overview and description

# %% Setup and Configuration
import [standard imports: sys, pathlib, pandas, numpy, matplotlib, etc]

TOPIC_NAME = 'X-analysis-name'

# 1. Detect working directory (are we in scripts/ or notebooks/?)
#    → Change to repo root if needed
repo_root = detect_and_change_to_repo_root()

# 2. Load configuration from 1-config.yaml
#    → Try YAML parser, fallback to line-based parsing
config = load_config(repo_root / '1-config.yaml')

# 3. Handle paper_project_root if specified
#    → Change working directory to paper root
if config.has('paper_project_root'):
    change_directory_to(config['paper_project_root'])

# 4. Setup output paths from config
results_root = get_from_config('evaluation_results_folder', default='evaluation/results')
output_dir = results_root / TOPIC_NAME
create_directory_if_needed(output_dir)

# 5. Load script-specific config section (e.g., "X-analysis-name:")
script_cfg = load_script_section(config, TOPIC_NAME)

# 6. Apply script-specific overrides
if script_cfg.has('output_dir'):
    output_dir = script_cfg['output_dir']

print("Setup complete")
print(f"Topic: {TOPIC_NAME}")
print(f"Output: {output_dir}")

# %% [markdown]
# ## Load Data

# %% Load Data
print("=" * 80)
print("LOADING DATA")
print("=" * 80)

# Load input data (usually from step 0)
data_path = results_root / '0-convert-.../metrics.csv'

if not data_path.exists():
    print("ERROR: Data not found")
    print("Run step 0 first!")
    raise FileNotFoundError(data_path)

df = load_data(data_path)
print(f"✓ Loaded {len(df)} rows")

# Apply filters from script config
if script_cfg.has('exclude_models'):
    df = filter_models(df, script_cfg['exclude_models'])

# %% [markdown]
# ## Helper Functions

# %% Helper Functions
def your_helper_function():
    """Your helper functions here"""
    pass

# %% [markdown]
# ## Analysis

# %% Analysis
print("=" * 80)
print("ANALYSIS")
print("=" * 80)

# Your analysis logic here
results = perform_analysis(df)

# %% [markdown]
# ## Visualization

# %% Visualization
print("=" * 80)
print("FIGURES")
print("=" * 80)

# Generate figures
fig = create_figure(results)
save_figure(fig, output_dir / "FigureX.pdf")

# %% [markdown]
# ## Save Results

# %% Save Results
print("=" * 80)
print("SAVING")
print("=" * 80)

save_results(results, output_dir / "summary.csv")
print("✓ Saved results")

# %% [markdown]
# ## Auto-convert to Notebook (Optional)

# %% Auto-convert
if config.get('auto_convert_to_notebook'):
    # Find conversion script (check multiple locations)
    converter = find_conversion_script([
        'code/scripts/convert_to_notebooks.py',
        'evaluation/notebooks/convert_to_notebooks.py',
        'notebooks/convert_to_notebooks.py'
    ])

    if converter:
        convert_this_script_to_notebook(converter, output_to='notebooks/')
        print("✓ Notebook created")

# %% [markdown]
# ## Summary

# %% Summary
print("=" * 80)
print("COMPLETE")
print("=" * 80)
print(f"Output: {output_dir}")

if __name__ == '__main__':
    print("Script execution completed!")
```

**Key Patterns:**
- Use `# %%` for code cells
- Use `# %% [markdown]` for documentation cells
- Detect working directory and change to repo root
- Load config with fallback parsing (YAML → line-based)
- Handle `paper_project_root` from config
- Load script-specific config section by name
- Apply script-specific overrides (paths, filters, etc.)
- Check multiple locations for conversion script
- Print progress with `"="*80` markers
- Use `raise` for errors (not `sys.exit()`)

**Note:** The actual implementation can vary - this is just the general pattern to follow. See existing scripts like `0-convert-Result-to-model-task-instance-score.py` for full examples.

---

Stage 2: Notebook Conversion
=============================

**Finding the Conversion Script:**

The conversion script can be in multiple locations. Check in this order:

1. Path from config: `1-config.yaml` → `convert_to_notebooks_script`
2. `code/scripts/convert_to_notebooks.py`
3. `evaluation/notebooks/convert_to_notebooks.py` (current project)
4. `notebooks/convert_to_notebooks.py`

**Automatic Conversion:**

Add to end of script (optional):

```python
# %% Auto-convert to notebook (optional)
if __name__ == '__main__':
    import subprocess
    import sys

    try:
        # Check multiple possible locations for conversion script
        conv_script = config.get('convert_to_notebooks_script')

        # Try locations in order of preference
        possible_locations = []
        if conv_script:
            possible_locations.append(repo_root / conv_script)

        # Common locations to check
        possible_locations.extend([
            repo_root / 'code' / 'scripts' / 'convert_to_notebooks.py',
            repo_root / 'evaluation' / 'notebooks' / 'convert_to_notebooks.py',
            repo_root / 'notebooks' / 'convert_to_notebooks.py',
        ])

        # Find first existing script
        conv_path = None
        for loc in possible_locations:
            if loc.exists():
                conv_path = loc.resolve()
                break

        if conv_path:
            this_script = Path(__file__).resolve()
            nb_dir = conv_path.parent
            ipynb_path = nb_dir / (this_script.stem + '.ipynb')

            subprocess.run([
                sys.executable, str(conv_path),
                str(this_script), '-o', str(ipynb_path)
            ], check=True)

            print(f"\n✓ Notebook created: {ipynb_path}")
            print(f"   Using converter: {conv_path.relative_to(repo_root)}")
        else:
            print(f"\nInfo: No conversion script found, skipping notebook generation")
    except Exception as e:
        print(f"\nWarning: Notebook conversion failed: {e}")
```

**Manual Conversion:**

```bash
# Find conversion script (check multiple locations)
# Location 1: code/scripts/convert_to_notebooks.py
# Location 2: evaluation/notebooks/convert_to_notebooks.py  (this project)
# Location 3: notebooks/convert_to_notebooks.py

# Convert single script to notebook
python evaluation/notebooks/convert_to_notebooks.py evaluation/scripts/1-topic.py

# Or if located elsewhere:
python code/scripts/convert_to_notebooks.py evaluation/scripts/1-topic.py

# Convert all scripts
python evaluation/notebooks/convert_to_notebooks.py evaluation/scripts/

# Specify output location
python evaluation/notebooks/convert_to_notebooks.py \
    evaluation/scripts/1-topic.py \
    -o evaluation/notebooks/1-topic.ipynb
```

**Verify Notebook Works:**

```bash
# Open in Jupyter
jupyter notebook evaluation/notebooks/1-topic.ipynb

# Or run all cells from command line
jupyter nbconvert --to notebook --execute \
    evaluation/notebooks/1-topic.ipynb \
    --output 1-topic.ipynb
```

---

Stage 3: Markdown Conversion
=============================

Convert notebook to full markdown with outputs:

```bash
# Convert single notebook
jupyter nbconvert --to markdown \
    evaluation/notebooks/1-topic.ipynb \
    --output-dir evaluation/markdowns

# Convert all notebooks
for nb in evaluation/notebooks/*.ipynb; do
    jupyter nbconvert --to markdown "$nb" \
        --output-dir evaluation/markdowns
done

# With embedded images (base64)
jupyter nbconvert --to markdown \
    --ExtractOutputPreprocessor.enabled=False \
    evaluation/notebooks/1-topic.ipynb \
    --output-dir evaluation/markdowns
```

**Result:** `evaluation/markdowns/1-topic.md`
- Contains all code cells
- Contains all outputs (text, tables)
- Contains embedded images (or references)
- Same structure as notebook

**Configuration Option:**

Add to `1-config.yaml`:

```yaml
auto_convert_to_markdown: true
markdown_output_dir: evaluation/markdowns
```

---

Stage 4: Documentation Markdown (ASCII Workflow Diagrams)
=========================================================

**🤖 LLM-Based Code Documentation**

This stage uses an LLM (like Claude) to:
1. **Read and understand** the Python script's structure
2. **Visualize the workflow** as ASCII flowcharts
3. **Show function relationships** as ASCII diagrams
4. **Write** `docs/1-topic.md` for quick code understanding

**Purpose:**
- Visualize the script's **workflow and structure** (not data results)
- Show what the code does step-by-step
- Display function relationships and dependencies
- Help developers quickly understand the code

**Focus:** Code structure visualization, NOT analysis results

---

**Example Documentation Structure:**

```markdown
# Script: 1-model-comparison.py

**Purpose:** Compare LLM vs baseline model performance across patient subgroups

**Input:** evaluation/results/0-convert-.../metrics.csv
**Output:** evaluation/results/1-model-comparison/

---

## Workflow

┌──────────────────────┐
│ Setup & Config       │
│ - Load 1-config.yaml │
│ - Detect repo root   │
│ - Setup output paths │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Load Data            │
│ - Read metrics.csv   │
│ - Apply filters      │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Classify Models      │
│ - LLM vs Baseline    │
│ - Context vs NoCtx   │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Aggregate Metrics    │
│ - Group by model     │
│ - Compute mean/std   │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Generate Figures     │
│ - Bar charts         │
│ - Save as PDF        │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Save Results         │
│ - summary.csv        │
│ - Copy to display/   │
└──────────────────────┘

---

## Function Structure

Main Flow:
  ├─ load_config()
  │   ├─ load_script_section()
  │   └─ resolve_paths()
  │
  ├─ load_data()
  │   ├─ read_csv()
  │   └─ filter_models()
  │
  ├─ process_data()
  │   ├─ classify_models()
  │   ├─ group_by_category()
  │   └─ compute_statistics()
  │
  ├─ generate_figures()
  │   ├─ create_bar_chart()
  │   └─ save_figure()
  │
  └─ save_results()
      ├─ save_csv()
      └─ copy_to_display()

---

## Key Functions

### load_config(path)
- Loads YAML configuration
- Fallback to line-based parsing
- Returns: config dict

### classify_models(df)
- Categorizes models by type
- Identifies context usage
- Returns: df with model_class column

### generate_figures(results)
- Creates matplotlib figures
- Saves as PNG/PDF
- Returns: None

---

## Config Dependencies

Required in 1-config.yaml:
- evaluation_results_folder
- model_display_names

Optional script-specific section:
```yaml
1-model-comparison:
  exclude_models: [...]
  figure_size: [10, 6]
```

---

## Output Files

evaluation/results/1-model-comparison/
├── summary.csv              (aggregated metrics)
├── FigureX-comparison.pdf   (visualization)
└── FigureX-comparison.png   (raster version)

Copied to:
├── 0-display/Figure/FigureX-comparison.pdf
```

---

**How LLM Creates This Documentation:**

**Step 1: Analyze Script Structure**
```
LLM reads: evaluation/scripts/1-topic.py
Identifies:
- Cell structure (# %% markers)
- Function definitions
- Data flow
- Dependencies
```

**Step 2: Create ASCII Workflow**
```
LLM generates flowchart showing:
- Sequential steps
- Decision points
- Data transformations
- Output generation
```

**Step 3: Map Function Relationships**
```
LLM creates tree showing:
- Which functions call which
- Helper function hierarchy
- Data flow between functions
```

**Step 4: Document Key Information**
```
LLM extracts:
- Input/output descriptions
- Config dependencies
- File structure
- Usage notes
```

---

**Example LLM Prompt for Generation:**

```
Please read evaluation/scripts/1-model-comparison.py and create workflow documentation
in evaluation/docs/1-model-comparison.md:

1. Analyze the script's structure and flow
2. Create ASCII flowchart showing the main workflow steps
3. Create ASCII diagram showing function relationships
4. Document:
   - Purpose and I/O
   - Key functions and their roles
   - Config dependencies
   - Output file structure

Focus: Code structure and workflow (NOT data analysis results)
Style: ASCII diagrams with minimal text
Goal: Help developers quickly understand what the code does
```

---

**ASCII Characters for Diagrams:**

```
Boxes:     ┌ ┐ └ ┘ │ ─
Arrows:    → ↓ ← ↑
Tree:      ├ └ │ ─
Double:    ═ ║ ╔ ╗ ╚ ╝
Corners:   ╭ ╮ ╯ ╰
```

---

Using Claude to Generate Workflow Docs
=======================================

**Workflow for LLM-Based Code Documentation:**

**Step 1: Prepare Context**
- Ensure script is complete and working
- Script should have clear cell structure (# %% markers)
- Functions should have docstrings

**Step 2: Request LLM Generation**

Ask Claude (or similar LLM):

```
Please create workflow documentation for this script:

Script: evaluation/scripts/1-topic.py

Generate evaluation/docs/1-topic.md showing:
1. Purpose and input/output description
2. ASCII flowchart of the main workflow
3. Function relationship diagram
4. Key functions and their roles
5. Config dependencies from 1-config.yaml
6. Output file structure

Focus: CODE STRUCTURE (not analysis results)
Style: ASCII diagrams with minimal explanatory text
Goal: Help developers quickly understand what the code does
```

**Step 3: LLM Analyzes**
- Reads the Python script structure
- Identifies cell organization (# %% markers)
- Maps function calls and dependencies
- Extracts config references
- Understands data flow

**Step 4: LLM Creates**
- ASCII flowchart showing workflow steps
- Function tree showing relationships
- Config dependency list
- Output file structure
- Brief function descriptions

**Step 5: Review and Iterate**
- Check diagrams render correctly in terminal
- Verify workflow accurately represents code
- Request adjustments if needed

**Example Request Format:**

```
@evaluation/scripts/6-llm-comparison.py

Please create evaluation/docs/6-llm-comparison.md with workflow documentation:

Required sections:
1. Purpose statement (1-2 sentences)
2. Workflow diagram (ASCII flowchart)
3. Function structure (ASCII tree)
4. Key functions (name + brief description)
5. Config dependencies (what it needs from 1-config.yaml)
6. Output files (what it generates)

Focus: How the CODE works, not what the RESULTS show
```

**Benefits of LLM Generation:**
- Visualizes code structure quickly
- Shows function relationships clearly
- Consistent documentation format
- Adapts to different script patterns
- Easier than manual diagram creation

---

Complete Workflow Example
==========================

**Step 1: Create Script**

```bash
# Create new script
touch evaluation/scripts/6-llm-comparison.py

# Edit with cell structure
# ... add code with # %% markers ...

# Run to verify it works
python evaluation/scripts/6-llm-comparison.py
```

**Step 2: Convert to Notebook**

```bash
# Find the conversion script
# Check: code/scripts/convert_to_notebooks.py
# Or: evaluation/notebooks/convert_to_notebooks.py

# Convert (use whichever location exists in your project)
python evaluation/notebooks/convert_to_notebooks.py \
    evaluation/scripts/6-llm-comparison.py

# Or if in code/scripts:
python code/scripts/convert_to_notebooks.py \
    evaluation/scripts/6-llm-comparison.py

# Verify notebook works
jupyter notebook evaluation/notebooks/6-llm-comparison.ipynb
```

**Step 3: Generate Markdown**

```bash
# Convert to markdown
jupyter nbconvert --to markdown \
    evaluation/notebooks/6-llm-comparison.ipynb \
    --output-dir evaluation/markdowns

# Verify
cat evaluation/markdowns/6-llm-comparison.md
```

**Step 4: Create Documentation (LLM-Generated)**

```bash
# Use LLM (Claude) to generate ASCII workflow documentation

# Prompt example:
# "Please read evaluation/scripts/6-llm-comparison.py and create workflow
# documentation in evaluation/docs/6-llm-comparison.md. Show:
# - ASCII flowchart of the main workflow
# - Function relationship diagram
# - Key functions and their purposes
# - Config dependencies
# Focus on CODE STRUCTURE, not data analysis results."

# The LLM will:
# 1. Read and analyze the script structure
# 2. Create ASCII flowchart of workflow steps
# 3. Diagram function relationships
# 4. Write evaluation/docs/6-llm-comparison.md

# Note: This documents the CODE, not the analysis results
```

**Verification:**

```bash
# All stages should exist
ls evaluation/scripts/6-llm-comparison.py
ls evaluation/notebooks/6-llm-comparison.ipynb
ls evaluation/markdowns/6-llm-comparison.md
ls evaluation/docs/6-llm-comparison.md

# All should be consistent
diff <(head -5 evaluation/scripts/6-llm-comparison.py) \
     <(head -5 evaluation/markdowns/6-llm-comparison.md)
```

---

Best Practices
==============

**1. Single Source of Truth**
- Script is the source
- Notebook is derived
- Markdown is derived
- Docs is curated/extracted

**2. Keep Scripts Runnable**
- Always test: `python scripts/X.py`
- No notebook-only code
- Clear error messages

**3. Consistent Structure**
- Use standard cell organization
- Print progress markers
- Save outputs to consistent paths

**4. Version Control**
- Commit scripts (always)
- Consider `.gitignore` for notebooks (derived)
- Commit docs (curated)
- Maybe ignore markdowns (auto-generated)

**5. Documentation Focus**
- Docs should be readable standalone
- ASCII graphs for quick reference
- Keep it concise and visual

**6. Automation**
- Script → notebook: automatic
- Notebook → markdown: `jupyter nbconvert`
- Markdown → docs: semi-automatic (curate key parts)

**7. Testing**
- Run script: `python scripts/X.py`
- Execute notebook: `jupyter nbconvert --execute`
- Verify markdown: `cat markdowns/X.md`
- Check docs: `cat docs/X.md`

---

Common Issues and Solutions
============================

**Issue: Notebook won't convert**
- Check for syntax errors in script
- Ensure `# %%` markers are correct
- Verify conversion script exists

**Issue: Markdown missing images**
- Use `--ExtractOutputPreprocessor.enabled=False` to embed
- Or save images to files first
- Check output directory permissions

**Issue: ASCII graphs don't render**
- Use monospace font in viewer
- Check terminal width (80+ chars recommended)
- Test with `cat docs/X.md` in terminal

**Issue: Paths don't work**
- Use `Path.cwd()` for repo root
- Make paths relative to config
- Test from repo root directory

**Issue: Output differs between runs**
- Set random seeds explicitly
- Check for time-dependent code
- Verify data hasn't changed

---

Quick Reference
===============

**File Locations:**
```
evaluation/
├── scripts/        # Source .py files (code)
├── notebooks/      # Derived .ipynb files (interactive)
├── markdowns/      # Full markdown from notebooks (with outputs)
└── docs/           # ASCII workflow diagrams (code structure)
```

**Commands:**
```bash
# Run script
python evaluation/scripts/1-topic.py

# Convert to notebook (check location: code/scripts/ or evaluation/notebooks/)
python evaluation/notebooks/convert_to_notebooks.py evaluation/scripts/1-topic.py
# or
python code/scripts/convert_to_notebooks.py evaluation/scripts/1-topic.py

# Convert to markdown
jupyter nbconvert --to markdown evaluation/notebooks/1-topic.ipynb \
    --output-dir evaluation/markdowns

# View docs
cat evaluation/docs/1-topic.md
```

**Cell Markers:**
```python
# %%              # Code cell
# %% Section      # Code cell with label
# %% [markdown]   # Markdown cell (optional)
```

**ASCII Characters for Diagrams:**
```
Boxes:   ┌ ┐ └ ┘ │ ─
Arrows:  → ↓ ← ↑
Tree:    ├ └ │ ─
Double:  ═ ║ ╔ ╗ ╚ ╝
```

---

End of Skill Definition
