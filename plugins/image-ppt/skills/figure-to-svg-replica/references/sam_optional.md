# Optional: SAM-based tight cropping

The default crop path (`crop_bboxes.py`) cuts each icon along the rectangular `bbox` you recorded in
`items.json`. That is fast, dependency-light, and good enough for most figures. On **busy figures**
— icons that touch, overlap, or sit on a textured/colored panel — a rectangular box drags in
neighbors and background. [Segment Anything (SAM)](https://github.com/facebookresearch/segment-anything)
can instead return a **pixel-tight, transparent** crop of just the icon.

This is strictly optional and heavier. Only reach for it when rectangular crops are demonstrably
polluting the vectorization step.

## Cost / prerequisites
- Extra Python deps in the fig2svg venv: `torch`, `scipy` (plus `segment-anything`).
  ```bash
  ~/.cache/fig2svg-venv/bin/pip install torch scipy git+https://github.com/facebookresearch/segment-anything.git
  ```
- A model checkpoint (~375 MB for the base ViT-B):
  - URL: `https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth`
  - Larger, more accurate variants exist (`sam_vit_l`, `sam_vit_h`) but ViT-B is plenty for icons.
  - Cache it once, e.g. `~/.cache/sam/sam_vit_b_01ec64.pth`; do not re-download per run.
- CPU works (a handful of icons); it is just slower than GPU.

## Technique: box-prompt + clip-to-box
`items.json` already gives each icon a `bbox`. Feed that box to SAM as a prompt and keep the mask:

```python
import torch, numpy as np
from PIL import Image
from segment_anything import sam_model_registry, SamPredictor

sam = sam_model_registry["vit_b"](checkpoint="~/.cache/sam/sam_vit_b_01ec64.pth")
sam.to("cuda" if torch.cuda.is_available() else "cpu")
predictor = SamPredictor(sam)

img = np.array(Image.open(source).convert("RGB"))
predictor.set_image(img)

for it in items:                      # only type == "icon"
    x, y, w, h = it["bbox"]
    box = np.array([x, y, x + w, y + h])          # SAM wants xyxy
    masks, scores, _ = predictor.predict(box=box[None, :], multimask_output=True)
    mask = masks[np.argmax(scores)]               # best-scoring mask

    # clip-to-box: never let the mask spill past the recorded bbox
    clip = np.zeros_like(mask)
    clip[y:y + h, x:x + w] = True
    mask = mask & clip

    # export a transparent, pixel-tight crop
    rgba = np.dstack([img, (mask * 255).astype(np.uint8)])
    crop = Image.fromarray(rgba[y:y + h, x:x + w], "RGBA")
    crop.save(f"{out_dir}/{it['id']}.png")
```

Key points:
- **Box prompt**, not point prompt — you already know roughly where the icon is, and a box is far more
  reliable than guessing a foreground point.
- **`multimask_output=True`** then pick the highest-scoring mask; SAM often proposes part-vs-whole
  masks and the top score is usually the whole icon.
- **Clip-to-box** (`mask & clip`) guarantees SAM never annexes a neighboring icon that touches the
  box edge — the recorded bbox stays the hard boundary.
- Export **RGBA with the mask as alpha** so the transparent crop drops straight into `image-to-svg`;
  the transparent background makes shape/color decomposition cleaner than a boxed crop with
  background pixels.

## When NOT to bother
- Icons already sit on a flat white/near-white panel with clear gaps → rectangular crops are fine.
- You only have a few icons and can nudge `bbox`es by hand faster than setting up torch.
- The figure is small/simple → the 375 MB download and model load dwarf the benefit.

Downstream steps are unchanged: transparent SAM crops still go through `image-to-svg`, and
`compose_svg.py` places them by `bbox` exactly as it does rectangular crops.
