# API examples

Real calls against a live `describe-food` service, three per category. Every
`response.json` is a verbatim reply. Nothing here is hand-written: if a reply in
this tree looks wrong, the service is wrong. Regenerate with

    python examples/run_examples.py

Each case folder holds:

    curl.sh        the call, reproducible by hand -- `cd` in and `bash curl.sh`
    request.json   what went in
    response.json  what came back, verbatim
    *.jpg          image cases only: the actual frames, so the case is
                   self-contained and curl.sh names them relatively
    body.json      image-batch cases only: the same frames base64-encoded,
                   which is the real body curl.sh posts

THE FRAMES ARE GITIGNORED. They are real CGMacros subject photographs and stay
out of the repository until their redistribution terms are settled: a photo
pushed once is in the history forever. A fresh clone therefore has the
transcripts but not the images, and `bash curl.sh` will not run until you
regenerate. The transcripts are what these examples are FOR, and those are
tracked.


## Read a response in this order

    1. NutritionConf    GOOD | PARTIAL | MISS
                        PARTIAL means some item did not resolve, so the totals
                        UNDERSTATE the meal. MISS means all five are null.

    2. NutritionBasis   per_meal | per_100g | null   <- read BEFORE the numbers
                        per_meal   a portion was stated; this IS the meal
                        per_100g   none was stated; this is the sum of each
                                   item's per-100g row. NOT a meal.
                        Compare 03-text-with-grams against 02-text-item-list:
                        identical shape, and only one of them is a meal.

    3. NutritionSource  bank_usda                looked up from a typed name
                        bank_usda|img:<engine>   the NAME came from a model
                        none                     nothing resolved

    4. NameSource / NameConf / FoodNameResolved
                        present when this library DERIVED the name rather than
                        reading it. FoodNameResolved is the exact string the
                        bank was asked for -- the audit trail for a photo.


## The image cases are not deterministic

`06-image-upload/3-image-nofood` is a sealed opaque BlenderBottle: no food is
visible anywhere in the frame. Across runs the engine sometimes declines to name
it and sometimes infers `protein shake` from the bottle, at a low `NameConf`.

Both outcomes are correct, and the pair is the reason `NameConf` exists. A
consumer reading only `Carbs` sees a confident-looking number; one reading
`NameConf` sees that the system is barely guessing. It is also why the test
suite asserts the CONTRACT rather than a specific food name.

## Cases

## 01-text-single-item

One food, one string. The simplest call there is.
- `1-fried-rice/` — one item -> MEASURED
- `2-boiled-egg/` — one item -> MEASURED
- `3-chinese-cabbage/` — one item -> ESTIMATED

## 02-text-item-list

A meal written as a ';' list, the WellDoc dialect.
- `1-list-1/` — MEASURED / per_serving
- `2-list-2/` — MEASURED / per_serving
- `3-list-3/` — ESTIMATED / per_meal

## 03-text-with-grams

Portions stated, so the answer IS the meal: basis=per_meal.
- `1-grams-1/` — basis=per_meal
- `2-grams-2/` — basis=per_meal
- `3-grams-3/` — basis=per_meal

## 04-text-names-no-food

The string names no food. A clean MISS that claims nothing.
- `1-just-carbs/` — MISS, all five nutrients null
- `2-unknown/` — MISS, all five nutrients null
- `3-dinner/` — MISS, all five nutrients null

## 05-text-batch

Many strings, one call. One result per input, in order.
- `1-batch-1/` — 3 distinct foods, order preserved
- `2-batch-2/` — a duplicate returns the identical record
- `3-batch-3/` — a hit, a declaration and an item the bank does not have

## 06-image-upload

Photo bytes over the wire. The caller shares no filesystem.
- `1-image-plate/` — one frame, a plated meal
- `2-image-pair/` — the before/after pair CGMacros logs for one meal
- `3-image-nofood/` — a sealed opaque bottle: nothing edible is visible

## 07-image-batch-base64

Many meals of frames in one JSON call.
- `1-imgbatch-1/` — one meal, one frame
- `2-imgbatch-2/` — one meal, two frames
- `3-imgbatch-3/` — two meals in one call: a hit and an honest MISS

## 08-errors

What a wrong call looks like. Never a 500, never a silent empty answer.
- `1-415-not-an-image/` — 415 - only image types are accepted
- `2-422-wrong-shape/` — 422 - foods must be a list, not a string
- `3-413-too-many-frames/` — 413 - one meal is one or two frames
