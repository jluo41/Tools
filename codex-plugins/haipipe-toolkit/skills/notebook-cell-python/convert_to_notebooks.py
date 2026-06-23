#!/usr/bin/env python3
"""
Convert Python scripts with cell markers to Jupyter notebooks.

Supports %% cell markers for code cells and %% [markdown] for markdown cells.

Usage:
    # Convert single file (auto: script/ -> notebook/)
    python convert_to_notebooks.py path/to/script/file.py

    # Convert with explicit output
    python convert_to_notebooks.py input.py -o output.ipynb

    # Convert entire directory
    python convert_to_notebooks.py --dir path/to/script/
"""

import argparse
import json
import os
import re
from pathlib import Path


def parse_python_to_cells(py_content):
    """Parse Python file with %% markers into notebook cells."""
    cells = []
    current_cell = {"cell_type": "code", "source": []}

    lines = py_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for cell markers
        if line.strip().startswith('# %% [markdown]'):
            # Save current cell if it has content
            if current_cell["source"]:
                # Remove trailing empty lines
                while current_cell["source"] and not current_cell["source"][-1].strip():
                    current_cell["source"].pop()
                if current_cell["source"]:
                    cells.append(current_cell)

            # Start new markdown cell
            current_cell = {"cell_type": "markdown", "source": []}
            i += 1
            continue

        elif line.strip().startswith('# %% [parameters]'):
            # Save current cell if it has content
            if current_cell["source"]:
                while current_cell["source"] and not current_cell["source"][-1].strip():
                    current_cell["source"].pop()
                if current_cell["source"]:
                    cells.append(current_cell)

            # Start new parameters cell (code cell with papermill tag)
            current_cell = {"cell_type": "parameters", "source": []}
            i += 1
            continue

        elif line.strip().startswith('# %%'):
            # Save current cell if it has content
            if current_cell["source"]:
                # Remove trailing empty lines
                while current_cell["source"] and not current_cell["source"][-1].strip():
                    current_cell["source"].pop()
                if current_cell["source"]:
                    cells.append(current_cell)

            # Start new code cell
            current_cell = {"cell_type": "code", "source": []}
            i += 1
            continue

        # Add line to current cell
        if current_cell["cell_type"] == "markdown":
            # Remove leading '# ' from markdown lines
            if line.startswith('# '):
                current_cell["source"].append(line[2:])
            elif line.startswith('#'):
                current_cell["source"].append(line[1:])
            else:
                current_cell["source"].append(line)
        else:
            current_cell["source"].append(line)

        i += 1

    # Add last cell
    if current_cell["source"]:
        # Remove trailing empty lines
        while current_cell["source"] and not current_cell["source"][-1].strip():
            current_cell["source"].pop()
        if current_cell["source"]:
            cells.append(current_cell)

    return cells


def create_notebook(cells):
    """Create Jupyter notebook structure from cells."""
    nb_cells = []

    for cell in cells:
        if cell["cell_type"] == "markdown":
            nb_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": '\n'.join(cell["source"])
            }
        elif cell["cell_type"] == "parameters":
            nb_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"tags": ["parameters"]},
                "outputs": [],
                "source": '\n'.join(cell["source"])
            }
        else:  # code cell
            nb_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": '\n'.join(cell["source"])
            }
        nb_cells.append(nb_cell)

    notebook = {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    return notebook


def convert_py_to_ipynb(py_path, ipynb_path):
    """Convert a Python file to Jupyter notebook."""
    py_path = Path(py_path)
    ipynb_path = Path(ipynb_path)

    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()

    # Parse cells
    cells = parse_python_to_cells(py_content)

    # Create notebook
    notebook = create_notebook(cells)

    # Write notebook
    with open(ipynb_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

    print(f"✓ {py_path.name} → {ipynb_path.name}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert Python scripts with %% markers to Jupyter notebooks.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file (auto: script/ -> notebook/)
  python convert_to_notebooks.py path/to/script/file.py

  # Convert with explicit output
  python convert_to_notebooks.py input.py -o output.ipynb

  # Convert entire directory
  python convert_to_notebooks.py --dir path/to/script/
        """
    )
    parser.add_argument('input', nargs='?', help='Input .py file or directory')
    parser.add_argument('-o', '--output', help='Output .ipynb file (optional)')
    parser.add_argument('-d', '--dir', action='store_true', help='Treat input as directory')

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return 1

    input_path = Path(args.input)

    # Directory mode
    if args.dir or input_path.is_dir():
        script_dir = input_path
        if not script_dir.exists():
            print(f"Error: Directory not found: {script_dir}")
            return 1

        # Replace 'script' with 'notebook' in path
        script_dir_str = str(script_dir)
        if '/script' in script_dir_str:
            out_dir = Path(script_dir_str.replace('/script', '/notebook'))
        else:
            out_dir = script_dir.parent / 'notebook'

        out_dir.mkdir(parents=True, exist_ok=True)

        py_files = sorted(script_dir.glob('*.py'))
        if not py_files:
            print(f"No .py files found in {script_dir}")
            return 1

        print(f"Converting {len(py_files)} files:")
        print(f"  {script_dir} → {out_dir}")
        print("-" * 60)

        for py_file in py_files:
            ipynb_path = out_dir / (py_file.stem + '.ipynb')
            try:
                convert_py_to_ipynb(py_file, ipynb_path)
            except Exception as e:
                print(f"✗ Error: {py_file.name}: {e}")

        print("-" * 60)
        print(f"✓ Done!")
        return 0

    # Single file mode
    py_path = input_path
    if not py_path.exists():
        print(f"Error: File not found: {py_path}")
        return 1

    if args.output:
        ipynb_path = Path(args.output)
    else:
        # Auto: replace 'script' with 'notebook' in path
        py_path_str = str(py_path)
        if '/script/' in py_path_str:
            ipynb_path_str = py_path_str.replace('/script/', '/notebook/')
            ipynb_path = Path(ipynb_path_str).with_suffix('.ipynb')
        else:
            ipynb_path = py_path.with_suffix('.ipynb')

    # Create output directory if needed
    ipynb_path.parent.mkdir(parents=True, exist_ok=True)

    convert_py_to_ipynb(py_path, ipynb_path)
    return 0


if __name__ == '__main__':
    main()
