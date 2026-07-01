# Lesson 05: An "editable PowerPoint" = the master SVG embedded as a native PPTX svgBlip

## The Problem
"Convert the figure to an editable PPT" doesn't mean a PNG on a slide, and python-pptx has no
native SVG-picture support. Naively adding the SVG failed / produced only a raster.

## The Solution
Embed the master SVG as PowerPoint's **native SVG picture** (vector, with a PNG fallback), so the
user opens the deck and does right-click → **Convert to Shape** for fully editable shapes + real
text. Build it by post-processing the .pptx zip:
1. Render a hi-res PNG fallback (`cairosvg`, ~3× the figure) and add it as the slide picture with
   python-pptx (this becomes `ppt/media/image1.png`, referenced by the blip's `r:embed`).
2. In the zip: register `<Default Extension="svg" ContentType="image/svg+xml"/>` in
   `[Content_Types].xml`; add `ppt/media/image2.svg`; add a slide relationship to it.
3. Inject into the `<a:blip>` (the one whose `r:embed` is the PNG):
   `<a:extLst><a:ext uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}">`
   `<asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" r:embed="<svg-rId>"/></a:ext></a:extLst>`
4. Size the slide to the figure's aspect ratio. Re-open with python-pptx to validate.

## Why It Works
PowerPoint stores an SVG picture as a blip with a raster fallback plus an `svgBlip` extension
pointing at the real vector. That extension is exactly what enables "Convert to Shape", which
ungroups the SVG into editable native shapes and text.

## When to Apply
Any time the deliverable is an *editable* PPT/deck from a vector figure (not just a picture).

## Caveats
The blip may be self-closing (`<a:blip r:embed="rId2"/>`) — handle that when injecting (make it
paired). Fonts become editable text but won't match a proprietary source face exactly; approximate
the family. "Convert to Shape" is a modern PowerPoint (2019+/365) feature.
