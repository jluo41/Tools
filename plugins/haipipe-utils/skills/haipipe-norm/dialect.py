"""
The dialect API: a vendor's code in, the vendor's own words out.

It runs BEFORE a describe-* service's input layer, so the service is only ever asked words. A
code means something only in the book of the vendor that wrote it, and the row's EntrySourceID
says which vendor that is: naming it is a fact about the data source, not about the activity.
JL asked for this split on 2026-09-30; before it, describe-exercise read codes itself
(exnorm/codebooks.py), and a SourceFn named some codes inline.

    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location("dialect", "<haipipe-norm>/dialect.py")
    ...
    name_exercise(['1001', 'Walking', '20905', '25', '9002'], source_ids=[23, 1, 20, 23, 24])

    value    source  Words    RowKind       Book     what happens next
    1001     23      Walking  session       validic  sent to describe-exercise as words
    Walking  1       Walking  words                  sent as written
    20905    20               daily_rollup  apple    not sent: a day's total
    25       23               placeholder   validic  not sent: the book's own "Other" names nothing
    9002     24               unread                 not sent: a code no book holds

Only RowKind 'words' and 'session' go on (SENT). A value made only of digits is a code; anything
else is words and passes through untouched (whether words name an activity is the service's call,
not this one's). The one table read is ext_exercise_codebook, "<code>|<EntrySourceID>", pinned by
the event release (paths.release_file), or at an explicit version. Its source is the vendor books
in ExternalStore/ext_exercise_codebook/@raw/ (PROVENANCE.md there).

The same rule, written into a SourceFn, is name_ExerciseCode in WellDocDataExtV260930B
(code/scripts/haibuilder/1-source/c1x_build_source_welldocdataextv260930b.py), and the first copy
is b51_externalstore/j02_ext_exercise/src/dialect_exercise.py. WellDoc's MedicationIDs are the
next dialect (ext_med_lexicon, today the SourceFn's name_MedicationID).
"""
import importlib.util
import pathlib

SENT = ("words", "session")
FIELDS = ["Name", "Label", "Book", "RowKind"]
COLUMNS = ["Words", "RowKind", "Book", "Label", "CodeKey"]


def _paths():
    spec = importlib.util.spec_from_file_location("haipipe_norm_paths", pathlib.Path(__file__).with_name("paths.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_P = _paths()
_TABLES = {}


def _source_id(v):
    try:
        return None if v is None or v != v or str(v).strip() == "" else int(float(v))
    except (TypeError, ValueError):
        return None


def exercise_book(release=None, version=None):
    """ext_exercise_codebook as {"<code>|<EntrySourceID>": {Name, Label, Book, RowKind}}: the version
    `version` names, else the one the release pins (default: $EVENTNORM_RELEASE, else paths.DEFAULT_RELEASE)."""
    import pandas as pd
    import yaml
    key = (release, version)
    if key in _TABLES:
        return _TABLES[key]
    if version:
        folder = _P.external_store() / "ext_exercise_codebook" / str(version)
        card = yaml.safe_load((folder / "version.yaml").read_text())
        path = folder / card["table"]
    else:
        path = _P.release_file("ext_exercise_codebook", release=release)
        if path is None:
            raise FileNotFoundError(f"release {release or 'default'} pins no ext_exercise_codebook")
        card = yaml.safe_load((path.parent / "version.yaml").read_text())
    t = pd.read_parquet(path)
    book = {k: {f: (None if v != v else v) for f, v in zip(FIELDS, vals)}
            for k, *vals in zip(t[card["key_column"]], *(t[f] for f in FIELDS))}
    _TABLES[key] = book
    return book


def exercise_sources():
    """EntrySourceID -> {vendor, book, code_prefix}, from the vendor books' own sources.csv."""
    import pandas as pd
    t = pd.read_csv(_P.external_store() / "ext_exercise_codebook" / "@raw" / "sources.csv")
    return {int(r.EntrySourceID): {"vendor": r.vendor, "book": r.book, "code_prefix": int(r.code_prefix)}
            for r in t.itertuples()}


def name_exercise(values, source_ids=None, release=None, version=None):
    """One row per value, in order: Words, RowKind, Book, Label, CodeKey ("<code>|<EntrySourceID>", or
    empty for words). `source_ids` is one EntrySourceID per value, or None."""
    import pandas as pd
    values = ["" if v is None or v != v else str(v) for v in values]
    sids = [None] * len(values) if source_ids is None else [_source_id(s) for s in source_ids]
    if len(sids) != len(values):
        raise ValueError(f"{len(sids)} source ids for {len(values)} values")
    book = exercise_book(release, version)
    rows = []
    for v, s in zip(values, sids):
        code = v.strip()
        if not code.isdigit():
            rows.append({"Words": v, "RowKind": "words", "Book": None, "Label": None, "CodeKey": ""})
            continue
        k = f"{code}|{'' if s is None else s}"
        b = book.get(k)
        if b is None:
            rows.append({"Words": None, "RowKind": "unread", "Book": None, "Label": None, "CodeKey": k})
        else:
            rows.append({"Words": b["Name"] if b["RowKind"] == "session" else None, "RowKind": b["RowKind"],
                         "Book": b["Book"], "Label": b["Label"], "CodeKey": k})
    return pd.DataFrame(rows, columns=COLUMNS)
