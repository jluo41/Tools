"""
Where a SPACE keeps its stores, resolved rather than guessed.

Tools is shared by every SPACE. A path written as /home/jluo41/WellDoc-SPACE is
therefore wrong everywhere except one checkout of one SPACE on one host, and it
fails silently: the bank does not open, every lookup returns MISS, and the
benchmark reports the resolver as broken when the resolver was never reached.
That is exactly what happened to describe-food's B1 and BEHAVE on macOS.

Resolution order, the same one `exnorm/constants.py:_find_bank` already used and
this module now states once for all four nouns:

    1. an explicit environment variable      how a service on another host, or an
                                             A/B against a newer bank, is done
    2. $LOCAL_<KIND>_STORE from env.sh       a SPACE declares where its stores are
    3. a marker walk up from this file       for a bare import with nothing sourced

Every returned path is ABSOLUTE. A relative hit resolves only while the process
happens to sit in the SPACE root, and a server that must start from anywhere
cannot depend on its own working directory.
"""
import os
import pathlib

__all__ = ["space_root", "store", "external_store", "source_store",
           "raw_data_store", "find_asset"]

_MARKERS = ("pyproject.toml", "code")


def space_root(start=None) -> pathlib.Path:
    """The SPACE root: the nearest ancestor holding both pyproject.toml and code/.

    Not parents[N]. A caller may sit inside a git submodule (a Project often is),
    so the number of levels up is not a constant worth counting, and it changes
    the moment a file moves.
    """
    start = pathlib.Path(start or __file__).resolve()
    for p in [start, *start.parents]:
        if (p / _MARKERS[0]).exists() and (p / _MARKERS[1]).is_dir():
            return p
    raise RuntimeError(
        f"no SPACE root above {start}: want an ancestor with both "
        f"{_MARKERS[0]} and {_MARKERS[1]}/")


def store(kind: str, start=None) -> pathlib.Path:
    """One declared store, absolute. `kind` is the env.sh suffix: EXTERNAL,
    SOURCE, RAW_DATA, RECORD, CASE, AIDATA, MODELINSTANCE, ENDPOINT."""
    root = space_root(start)
    declared = os.environ.get(f"LOCAL_{kind}_STORE")
    if declared:
        p = pathlib.Path(declared)
        return p.resolve() if p.is_absolute() else (root / p).resolve()
    default = {"EXTERNAL": "ExternalStore", "SOURCE": "1-SourceStore",
               "RAW_DATA": "0-RawDataStore", "RECORD": "2-RecStore",
               "CASE": "3-CaseStore", "AIDATA": "4-AIDataStoreLocal",
               "MODELINSTANCE": "5-ModelInstanceStoreLocal",
               "ENDPOINT": "6-EndpointStore"}.get(kind, kind)
    return (root / "_WorkSpace" / default).resolve()


def external_store(start=None) -> pathlib.Path:
    return store("EXTERNAL", start)


def source_store(start=None) -> pathlib.Path:
    return store("SOURCE", start)


def raw_data_store(start=None) -> pathlib.Path:
    return store("RAW_DATA", start)


def find_asset(rel, env_var=None, kind="EXTERNAL", start=None) -> pathlib.Path:
    """One reference file under a store. Returns the resolved path when it
    exists, and otherwise the path it looked for, so the caller's own error names
    what is missing instead of crashing here with a sqlite3 message nobody can
    trace back to a store."""
    if env_var:
        explicit = os.environ.get(env_var)
        if explicit:
            return pathlib.Path(explicit).resolve()
    hit = store(kind, start) / rel
    return hit.resolve()
