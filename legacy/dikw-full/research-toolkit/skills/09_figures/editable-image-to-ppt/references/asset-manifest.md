# Asset Manifest Reference

Use an asset manifest to drive `scripts/asset_cropper.py`. The agent decides the crop boxes by inspecting the source slide image.

## Single Image Manifest

```json
{
  "source": "slide_02.png",
  "assets": [
    {
      "name": "01_header_logo_full.png",
      "box": [48, 36, 254, 101],
      "mode": "transparent",
      "transparent": 5,
      "opaque": 38,
      "pad": 3
    },
    {
      "name": "10_research_ribbon_blank.png",
      "box": [870, 178, 1083, 234],
      "mode": "mask",
      "mask": "purple",
      "row_fill_holes": true,
      "blank": true,
      "pad": 2
    }
  ]
}
```

Run:

```bash
python scripts/asset_cropper.py --manifest page_002.assets.json --out-dir assets/page_002 --contact-sheet
```

## Batch Manifest

```json
{
  "images": [
    {
      "source": "slide_01.png",
      "out_dir": "page_001",
      "assets": []
    },
    {
      "source": "slide_02.png",
      "out_dir": "page_002",
      "assets": []
    }
  ]
}
```

Run:

```bash
python scripts/asset_cropper.py --manifest batch.assets.json --out-dir assets --contact-sheet
```

## Asset Modes

`transparent`: remove a flat background sampled from crop corners. Best for icons, logos, purple line art on white background, and decorations.

`keep`: crop exactly and preserve all pixels. Best for full-width footer bars, photo areas, screenshots, or textured backgrounds.

`mask`: keep pixels matching a color family and make everything else transparent. Use `mask: "purple"` for purple ribbons or icons, `mask: "dark"` for dark marks, or `mask: "non-bg"` for anything different from a specified/sampled background.

`ellipse` or `circle`: create an oval/circular alpha mask for circular badges or numbered dots. Use `blank: true` and `fill` to create reusable blank circles without text.

## Extraction Rules

Extract image/icon materials, not normal body text. Treat wordmarks, logos, seals, stylized calligraphy, and emblems as visual assets when they would be hard to recreate as editable text.

Make one PNG per reusable visual asset. Merge tiny decorative fragments only when they are visually inseparable or only useful as a group, such as a footer ornament strip or paired title flourish.

Always generate `_contact_sheet.png` and inspect it. If a white glyph inside a purple circle disappears, rerun that asset with `mode: "ellipse"` or `mode: "mask"` instead of corner-background removal.
