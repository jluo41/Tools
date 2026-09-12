#!/usr/bin/env python3
"""Regression checks for the shared Page-to-delivery reader."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import md2docx


class ParsePageTests(unittest.TestCase):
    def test_html_receipt_comment_is_not_delivery_prose(self):
        source = """# Example · §1 Introduction

## Content

### 1 · Introduction

#### P1. Opening

Visible sentence. <!-- realizes: C1.P1.B1 -->

## Aims
"""
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "Example.md"
            page.write_text(source)
            blocks, fenced = md2docx.parse_page(page)

        prose = [block[1] for block in blocks if block[0] == "p"]
        self.assertEqual(fenced, 0)
        self.assertEqual(prose, ["Visible sentence."])


if __name__ == "__main__":
    unittest.main()
