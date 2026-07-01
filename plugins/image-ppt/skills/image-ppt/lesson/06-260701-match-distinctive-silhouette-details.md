# Lesson 06: Reproduce the source's distinctive silhouette detail, not a generic version

## The Problem
The first-pass cloud icon had a scalloped/rounded bottom; the source cloud has a FLAT bottom. The
first database icon rendered as a solid dark blob instead of an outline cylinder. Both "read as a
cloud / a database" but the user immediately spotted them as not-the-same ("make the cloud bottom
flat, same as before").

## The Solution
When decomposing, note the ONE or TWO silhouette features that make the object look like *that*
drawing, and build to them:
- Flat-bottom cloud = a `rect` for the flat base + top-edge `circle`s for the bumps whose bottoms
  sit on the base line (NOT a chain of arcs that curves the bottom).
- Outline cylinder = top `ellipse` + side path + inner disc arcs with `fill="none" stroke=...`
  (match solid-vs-outline to the source).
Then diff the render against the original and fix the specific mismatch, not the whole icon.

## Why It Works
Recognition hinges on a few salient features (a cloud's flat base, a cylinder's disc seams, a
brain's two lobes). Getting the gestalt but missing the salient feature is exactly what a viewer
who knows the original will flag.

## When to Apply
Every icon — but especially common objects (cloud, database, shield, monitor, building) where the
source uses a specific rendering the reader will compare against.

## Caveats
Don't over-fit anti-aliasing/noise; reproduce the *intended* feature, not every stray pixel.
Match solid vs. outline style to the source (Lesson 03/04 scoring still applies).

## Update 2026-07-01
More icons that "read as the right thing" but missed the salient feature until fixed on a second
pass (Figure-2, AI-CPC):
- **Stethoscope** — first pass read as **scissors / a tuning fork**. The salient anatomy is a
  binaural headset (two ear-tip nubs → tubes splaying down in an inverted-U) → a single tube to a
  round **chestpiece** at lower-right → a small **spring loop** at lower-left. Two prongs + a dot is
  not a stethoscope.
- **Geriatric pair** — first pass was **bulbous/blobby**. Two *slim, human-proportioned* standing
  silhouettes (a shorter and a taller figure, a small white heart on the taller one) read as
  elder-care; wide rounded bodies don't.
- **Database** — first pass was a plain **barrel/can**. The salient feature is **three stacked disk
  tiers** (top ellipse cap + two curved white seam lines); without the seams it isn't a database.
- **Star of Life** — the six-bar star is easy; the salient center is a **legible Rod of Asclepius**
  (straight staff + a snake in clean S-curves), not a white blob.
Pattern holds: get the gestalt *and* the one defining detail, and diff to fix that specific detail.

