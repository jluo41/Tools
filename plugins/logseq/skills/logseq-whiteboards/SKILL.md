---
name: logseq-whiteboards
description: Create and edit LogSeq Whiteboard files (.edn) with shapes, connectors, portals, and embeds on an infinite canvas. Use when working with whiteboard .edn files in a LogSeq graph, creating visual diagrams, mind maps, or spatial canvases, or when the user mentions LogSeq whiteboards.
---

# LogSeq Whiteboards

LogSeq Whiteboards are infinite spatial canvases stored as `.edn` (Extensible Data Notation) files. Built on a custom fork of tldraw, they combine freeform drawing with LogSeq's knowledge graph — allowing you to place pages, blocks, shapes, connectors, images, and web embeds together on a visual canvas.

## File Location

Whiteboard files are stored in the `whiteboards/` directory of a LogSeq graph:

```
my-graph/
├── journals/
├── pages/
├── whiteboards/          ← Whiteboard .edn files here
│   ├── My Diagram.edn
│   └── Project Board.edn
├── assets/               ← Images referenced by whiteboards
└── logseq/
    └── config.edn        ← Can customize :whiteboards-directory
```

The directory name can be changed in `config.edn` via `:whiteboards-directory`.

## EDN File Structure

Every whiteboard `.edn` file has two top-level sections: `:blocks` (shapes) and `:pages` (canvas metadata).

```clojure
{:blocks (
  ;; Each shape is a block with :logseq.tldraw.shape properties
  {:block/created-at 1728698317371
   :block/properties
   {:ls-type :whiteboard-shape
    :logseq.tldraw.shape
    {:type "text"
     :id "unique-uuid"
     :point [100 200]
     :size [300 50]
     ;; ... shape-specific properties
     }}
   :block/updated-at 1728698317371}
  ;; More shape blocks...
  )
 :pages (
  ;; One page entry per whiteboard
  {:block/uuid #uuid "page-uuid-here"
   :block/properties
   {:ls-type :whiteboard-page
    :logseq.tldraw.page
    {:id "page-uuid-here"
     :name "whiteboard-name"
     :bindings {}
     :nonce 1
     :assets []
     :shapes-index ("shape-id-1" "shape-id-2" "shape-id-3")}}
   :block/type "whiteboard"
   :block/name "whiteboard-name"
   :block/original-name "Whiteboard Name"
   :block/created-at 1728698317371
   :block/updated-at 1728698317371}
  )}
```

## Shape Types

LogSeq whiteboards support 8 shape types:

| Type | Description |
|------|-------------|
| `"text"` | Text labels and paragraphs |
| `"box"` | Rectangles with optional labels |
| `"line"` | Lines and arrows (connectors) |
| `"pencil"` | Freehand drawings |
| `"image"` | Images (references assets) |
| `"logseq-portal"` | Embedded LogSeq pages or blocks |
| `"youtube"` | Embedded YouTube videos |
| `"iframe"` | Embedded web pages |

---

## Common Shape Properties

All shapes share these properties within `:logseq.tldraw.shape`:

| Property | Type | Description |
|----------|------|-------------|
| `:type` | String | Shape type (see table above) |
| `:id` | String | Unique UUID for this shape |
| `:point` | `[x y]` | Position (top-left corner) on canvas |
| `:size` | `[width height]` | Dimensions in pixels |
| `:index` | Integer | Z-order (rendering layer, higher = on top) |
| `:scale` | `[sx sy]` | Scale factors (usually `[1 1]`) |
| `:opacity` | Number | Opacity 0.0 to 1.0 |
| `:rotation` | Number | Rotation in radians (0 = no rotation) |
| `:parentId` | String | Parent shape ID (page ID for top-level shapes) |
| `:nonce` | Integer | Timestamp for change tracking |

---

## Text Shape

Text labels and headings on the canvas.

```clojure
{:logseq.tldraw.shape
 {:type "text"
  :id "uuid-here"
  :point [100 200]
  :size [300 50]
  :text "Hello World"
  :fontSize 32               ;; Font size in pixels
  :fontFamily "'Inter'"      ;; Font family (CSS)
  :fontWeight 700            ;; 400 = normal, 700 = bold
  :italic false              ;; Italic text
  :lineHeight 1.2            ;; Line height multiplier
  :isSizeLocked true         ;; Size auto-adjusts to text
  :scaleLevel "lg"           ;; "xs", "sm", "md", "lg", "xl"
  :padding 4                 ;; Internal padding
  :stroke "var(--tl-foreground, #000)"
  :fill "#ffffff"
  :noFill true               ;; true = transparent background
  :strokeType "line"
  :strokeWidth 2
  :borderRadius 0
  :index 0
  :scale [1 1]
  :opacity 1
  :parentId "page-uuid"
  :nonce 1664366266517}}
```

**Scale levels** control default font sizes:

| Level | Typical fontSize |
|-------|-----------------|
| `"xs"` | 12 |
| `"sm"` | 16 |
| `"md"` | 20 |
| `"lg"` | 32 |
| `"xl"` | 48 |

---

## Box Shape

Rectangles for containers, cards, and labeled shapes.

```clojure
{:logseq.tldraw.shape
 {:type "box"
  :id "uuid-here"
  :point [0 0]
  :size [1071 578]
  :label ""                  ;; Text label inside box (can be empty)
  :stroke "#ababab"          ;; Border color
  :fill "var(--ls-secondary-background-color)"  ;; Fill color
  :noFill false              ;; false = filled, true = transparent
  :strokeType "line"         ;; "line" or "dashed"
  :strokeWidth 2
  :borderRadius 2            ;; Corner rounding in pixels
  :fontSize 20               ;; Label font size
  :fontWeight 400
  :italic false
  :rotation 0
  :index 1
  :scale [1 1]
  :opacity 1
  :parentId "page-uuid"
  :nonce 1664366266231}}
```

---

## Line Shape (Connectors and Arrows)

Lines connect shapes with optional arrowheads and labels.

```clojure
{:logseq.tldraw.shape
 {:type "line"
  :id "uuid-here"
  :point [2824 284]          ;; Base point (origin for handles)
  :stroke "var(--ls-primary-text-color, #000)"
  :fill "var(--ls-secondary-background-color)"
  :noFill true
  :strokeType "line"         ;; "line" or "dashed"
  :strokeWidth 1
  :label ""                  ;; Text label on the line
  :fontSize 20
  :fontWeight 400
  :italic false
  :handles                   ;; Start and end points (relative to :point)
  {:start
   {:id "start"
    :canBind true            ;; Can snap to other shapes
    :point [0 0]             ;; Relative position [x y]
    :bindingId nil}          ;; UUID of bound shape (nil = unbound)
   :end
   {:id "end"
    :canBind true
    :point [52 0]            ;; End point relative to base
    :bindingId nil}}
  :decorations               ;; Arrowheads
  {:start nil                ;; nil or "arrow"
   :end "arrow"}             ;; nil or "arrow"
  :index 28
  :scale [1 1]
  :opacity 1
  :parentId "page-uuid"
  :nonce 1664464964296}}
```

**Decorations**: Set `:start` and/or `:end` to `"arrow"` for arrowheads. Use `nil` for no arrowhead.

**Bindings**: When a line connects to a shape, `:bindingId` references the bound shape's ID. The `:bindings` map in the page metadata tracks these connections.

---

## Pencil Shape (Freehand Drawing)

Freehand strokes from the pencil tool.

```clojure
{:logseq.tldraw.shape
 {:type "pencil"
  :id "uuid-here"
  :point [212 160]           ;; Base position
  :points [[0 0 0.5]]       ;; Array of [x y pressure] points (relative)
  :stroke ""                 ;; Stroke color (empty = theme default)
  :fill ""
  :noFill true
  :strokeType "line"
  :strokeWidth 2
  :scaleLevel "md"
  :isComplete true           ;; true when stroke is finished
  :index 0
  :scale [1 1]
  :opacity 1
  :parentId "page-uuid"
  :nonce 1730788259525}}
```

Each point in `:points` is `[x y pressure]` where:
- `x`, `y` are relative to the shape's `:point`
- `pressure` is pen pressure (0.0 to 1.0, typically 0.5 for mouse)

---

## Image Shape

Images reference assets stored in the graph's `assets/` directory.

```clojure
{:logseq.tldraw.shape
 {:type "image"
  :id "uuid-here"
  :point [136 200]
  :size [260 105]
  :assetId "asset-uuid"     ;; References asset in page's :assets array
  :isAspectRatioLocked true ;; Preserve aspect ratio on resize
  :isLocked false            ;; Prevent accidental moves
  :objectFit "fill"          ;; "fill", "contain", "cover"
  :clipping 0                ;; Clipping amount
  :index 0
  :scale [1 1]
  :opacity 1
  :parentId "page-uuid"
  :nonce 1770432010158}}
```

Assets are defined in the page's `:assets` array:

```clojure
:assets [
  {:id "asset-uuid"
   :type "image"
   :src "../assets/image_1770432010069_0.png"  ;; Relative path
   :size [520 210]}]                            ;; Original dimensions
```

---

## LogSeq Portal Shape

The unique LogSeq feature — embed pages or blocks from your graph directly onto the whiteboard.

```clojure
{:logseq.tldraw.shape
 {:type "logseq-portal"
  :id "uuid-here"
  :point [256 168]
  :size [400 141]
  :blockType "P"             ;; "P" = page portal, "B" = block portal
  :pageId "PageName"         ;; Page name (for page portals)
  ;; :blockId "block-uuid"  ;; Block UUID (for block portals)
  :collapsed false           ;; true = show only title
  :collapsedHeight 0         ;; Height when collapsed
  :compact false             ;; Compact display mode
  :isAutoResizing true       ;; Auto-resize to fit content
  :stroke ""
  :fill ""
  :noFill false
  :strokeType "line"
  :strokeWidth 2
  :borderRadius 8
  :scaleLevel "md"
  :index 2
  :scale [1 1]
  :opacity 1
  :parentId "page-uuid"
  :nonce 1731296148685}}
```

**Portal types**:
- **Page portal** (`blockType: "P"`): Uses `:pageId` — embeds an entire page
- **Block portal** (`blockType: "B"`): Uses `:blockId` — embeds a single block and its children

Portals render live LogSeq content. Editing the portal edits the actual page/block.

---

## YouTube Shape

Embed YouTube videos on the canvas.

```clojure
{:logseq.tldraw.shape
 {:type "youtube"
  :id "uuid-here"
  :point [7383 321]
  :size [283 159]
  :url "https://www.youtube.com/watch?v=VIDEO_ID"
  :rotation 0
  :index 49
  :scale [1 1]
  :parentId "page-uuid"
  :nonce 1664531347941}}
```

---

## IFrame Shape

Embed any web page on the canvas.

```clojure
{:logseq.tldraw.shape
 {:type "iframe"
  :id "uuid-here"
  :point [7730 321]
  :size [282 158]
  :url "https://logseq.com/"
  :rotation 0
  :index 50
  :scale [1 1]
  :parentId "page-uuid"
  :nonce 1664531425980}}
```

---

## Page Metadata

The `:pages` section contains canvas-level metadata:

```clojure
{:block/uuid #uuid "page-uuid"
 :block/properties
 {:ls-type :whiteboard-page
  :logseq.tldraw.page
  {:id "page-uuid"
   :name "whiteboard-name"        ;; Lowercase page name
   :bindings {}                    ;; Shape-to-shape binding map
   :nonce 1                        ;; Change counter
   :assets [                       ;; Image assets used by shapes
     {:id "asset-uuid"
      :type "image"
      :src "../assets/filename.png"
      :size [width height]}]
   :shapes-index ("id1" "id2")}}  ;; Ordered list of shape IDs
 :block/type "whiteboard"
 :block/name "whiteboard-name"     ;; Lowercase
 :block/original-name "Whiteboard Name"  ;; Original case
 :block/created-at 1728698317371
 :block/updated-at 1728698317371}
```

**`:shapes-index`** controls the order shapes are listed. This is a list of shape IDs.

**`:bindings`** tracks connections between lines and shapes when `:bindingId` is set on line handles.

**`:assets`** stores metadata for images used by image shapes. The `:src` path is relative to the graph root.

---

## Color Values

Shapes support these color formats:

| Format | Example |
|--------|---------|
| Hex color | `"#ababab"`, `"#ffffff"` |
| CSS variable | `"var(--ls-primary-text-color, #000)"` |
| Named color | `"gray"` |
| Empty (theme default) | `""` |

Common CSS variables:
- `var(--ls-primary-text-color, #000)` — primary text
- `var(--ls-secondary-background-color)` — secondary background
- `var(--tl-foreground, #000)` — tldraw foreground

---

## Coordinate System

- **Origin**: Top-left of the canvas (can extend into negative coordinates)
- **X axis**: Increases to the right
- **Y axis**: Increases downward
- **`:point`** is the top-left corner of each shape
- **`:size`** is `[width height]` in pixels
- **`:handles`** on lines are relative to the line's `:point`

---

## Complete Example

A minimal whiteboard with a box, text label, and an arrow:

```clojure
{:blocks (
  {:block/created-at 1700000000000
   :block/properties
   {:ls-type :whiteboard-shape
    :logseq.tldraw.shape
    {:type "box"
     :id "box-1"
     :point [100 100]
     :size [200 100]
     :stroke "#ababab"
     :fill "var(--ls-secondary-background-color)"
     :noFill false
     :strokeType "line"
     :strokeWidth 2
     :borderRadius 8
     :label "My Box"
     :fontSize 20
     :fontWeight 400
     :italic false
     :rotation 0
     :index 0
     :scale [1 1]
     :opacity 1
     :parentId "page-1"
     :nonce 1700000000000}}
   :block/updated-at 1700000000000}
  {:block/created-at 1700000000001
   :block/properties
   {:ls-type :whiteboard-shape
    :logseq.tldraw.shape
    {:type "text"
     :id "text-1"
     :point [100 50]
     :size [200 30]
     :text "Hello Canvas"
     :fontSize 24
     :fontFamily "'Inter'"
     :fontWeight 700
     :italic false
     :lineHeight 1.2
     :isSizeLocked true
     :scaleLevel "lg"
     :padding 4
     :stroke ""
     :fill ""
     :noFill true
     :strokeType "line"
     :strokeWidth 2
     :borderRadius 0
     :index 1
     :scale [1 1]
     :opacity 1
     :parentId "page-1"
     :nonce 1700000000001}}
   :block/updated-at 1700000000001}
  {:block/created-at 1700000000002
   :block/properties
   {:ls-type :whiteboard-shape
    :logseq.tldraw.shape
    {:type "line"
     :id "arrow-1"
     :point [350 150]
     :stroke ""
     :fill ""
     :noFill true
     :strokeType "line"
     :strokeWidth 1
     :label ""
     :fontSize 20
     :fontWeight 400
     :italic false
     :handles
     {:start
      {:id "start"
       :canBind true
       :point [0 0]
       :bindingId nil}
      :end
      {:id "end"
       :canBind true
       :point [100 0]
       :bindingId nil}}
     :decorations
     {:end "arrow"}
     :index 2
     :scale [1 1]
     :opacity 1
     :parentId "page-1"
     :nonce 1700000000002}}
   :block/updated-at 1700000000002})
 :pages (
  {:block/uuid #uuid "00000000-0000-0000-0000-000000000001"
   :block/properties
   {:ls-type :whiteboard-page
    :logseq.tldraw.page
    {:id "page-1"
     :name "my-diagram"
     :bindings {}
     :nonce 1
     :assets []
     :shapes-index ("box-1" "text-1" "arrow-1")}}
   :block/type "whiteboard"
   :block/name "my-diagram"
   :block/original-name "My Diagram"
   :block/created-at 1700000000000
   :block/updated-at 1700000000002})}
```

## Tips

1. **EDN format** — Uses Clojure-style syntax: `{}` for maps, `()` for lists, `[]` for vectors, `:keyword` for keys
2. **UUIDs** — Shape IDs are typically UUID v1 format (time-based), page UUIDs use `#uuid "..."` reader literal
3. **parentId** — Top-level shapes set `:parentId` to the page's UUID string
4. **Assets** — Images must have both an entry in `:assets` (page level) and a shape with matching `:assetId`
5. **Portals are live** — LogSeq portal shapes render actual graph content; edits sync bidirectionally
6. **CSS variables** — Use LogSeq CSS variables for theme-aware colors
7. **Whiteboard = page** — Every whiteboard is also a LogSeq page with `:block/type "whiteboard"`

## References

- [LogSeq Whiteboards Announcement](https://blog.logseq.com/whiteboards-and-queries-for-everybody/)
- [tldraw SDK](https://github.com/tldraw/tldraw) (base canvas library)
- [LogSeq GitHub](https://github.com/logseq/logseq)
- [EDN Format Specification](https://github.com/edn-format/edn)
