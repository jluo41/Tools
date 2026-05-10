# Reconstruction SOP

Use this checklist for each source slide image.

## 1. Inspect

Record:

- source image size
- slide aspect ratio and target PPT size
- dominant colors
- visual asset inventory: logos, icons, photos, background ornaments, rules, cards, ribbons, separators, badges
- editable text inventory: titles, body labels, numbers, captions, section headings

For repeated page templates, solve one representative slide first, then reuse its geometry and adjust only page-specific content.

## 2. Extract Assets

Create `page_###.assets.json`.

Extract:

- logos and wordmarks
- icons and pictograms
- photos/screenshots
- background line art and decorative bands
- complex ribbons, flourishes, badges, patterned rules
- reusable blank variants when useful, such as blank numbered circles or empty tabs

Do not extract normal editable slide text as PNG. The text must be rebuilt as PowerPoint text boxes.

Run `asset_cropper.py`, inspect `_contact_sheet.png`, and iterate until no obvious asset is missing or damaged.

## 3. Rebuild As Editable PPT

Create `page_###.layout.json`.

Prefer native PowerPoint objects:

- text boxes for all ordinary text
- shapes for card frames, circles, simple rectangles, and basic separators
- lines/connectors for simple rules and dividers
- images for extracted assets

Use source-image pixel coordinates in layout JSON. Preserve element ordering from background to foreground.

Keep each text box roomy. If rendered text wraps differently from the source, adjust box width/height, font, or line breaks instead of shrinking to unreadable sizes.

## 4. Batch

For many pages:

1. Create one asset folder per page: `assets/page_001`, `assets/page_002`, ...
2. Create one layout file per page: `layouts/page_001.layout.json`, ...
3. Build and preview a few representative pages first.
4. Combine all layouts with `combine_layouts.py`.
5. Build the final deck with `build_pptx_from_layout.py`.

## 5. QA

Run `inspect_pptx.py` on the final PPTX.

Also render or open a preview of the saved PPTX when available. Compare to the source images and check:

- no missing icons or decorative materials
- text remains editable, not embedded as screenshots
- images remain editable picture objects
- frames, ribbons, footer/header bands, and major alignments match the source
- no text clipping or accidental wrapping
- no placeholder text or empty media

If a preview renderer is unavailable, still inspect the PPTX package and state that visual parity was checked by opening/exporting through the available tool or by manual image comparison.
