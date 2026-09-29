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
           "raw_data_store", "find_asset", "release_file", "release_key_column"]

_MARKERS = ("pyproject.toml", "code")


def space_root(start=None) -> pathlib.Path:
    """The SPACE root: the nearest ancestor holding both pyproject.toml and code/.

    Not parents[N]. A caller may sit inside a git submodule (a Project often is),
    so the number of levels up is not a constant worth counting, and it changes
    the moment a file moves.
    """
    # Tools is often a symlink into a SPACE (WellDoc-SPACE/Tools -> ../Tools-SPACE).
    # .resolve() follows it out of the SPACE, so walk the path as imported first,
    # then the resolved one, then the working directory a ticket runs from.
    if start:
        starts = [pathlib.Path(start).resolve()]
    else:
        starts = [pathlib.Path(os.path.abspath(__file__)), pathlib.Path(__file__).resolve(),
                  pathlib.Path.cwd()]
    for s in starts:
        for p in [s, *s.parents]:
            if (p / _MARKERS[0]).exists() and (p / _MARKERS[1]).is_dir():
                return p
    raise RuntimeError(
        f"no SPACE root above {starts[0]}: want an ancestor with both "
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


# ── the event release ─────────────────────────────────────────────────────────
# The four describe-* services read their tables through one release, the same
# file a WellDoc SourceFn pins (b51_externalstore/j49_external_releases). A service
# asks for an asset; the release names the version; the version card names the file
# and its sha256, which is checked once per process. No release, or an asset the
# release does not pin, returns None and the caller keeps its old path.

DEFAULT_RELEASE = "EventNormV3"                 # the release WellDocDataExtV260927 reads
_RELEASE_CACHE = {}


def _sha256(path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def release_file(asset, filename=None, release=None, start=None):
    """The file of `asset` that the event release pins, checksum verified, or None.

    release   release name; default $EVENTNORM_RELEASE, else DEFAULT_RELEASE. "none" turns
              the release off and every caller falls back to its flat folder.
    filename  a file in the version folder; default the version's table.
    """
    name = release or os.environ.get("EVENTNORM_RELEASE", DEFAULT_RELEASE)
    if name.lower() == "none":
        return None
    key = (name, asset, filename, str(start))
    if key in _RELEASE_CACHE:
        return _RELEASE_CACHE[key]
    import yaml
    try:
        root = external_store(start)
    except RuntimeError:
        return None
    release_path = root / "_releases" / f"{name}.yaml"
    if not release_path.exists():                  # a store not moved yet (Lambda) keeps _locks/
        release_path = root / "_locks" / f"{name}.yaml"
    pins = (yaml.safe_load(release_path.read_text()) or {}).get("assets", {}) if release_path.exists() else {}
    if asset not in pins:
        _RELEASE_CACHE[key] = None
        return None
    folder = root / asset / str(pins[asset])
    card = yaml.safe_load((folder / "version.yaml").read_text())
    fname = filename or card["table"]
    path = folder / fname
    expected = (card.get("sha256") or {}).get(fname)
    if expected and _sha256(path) != expected:
        raise RuntimeError(f"{asset}/{pins[asset]}/{fname}: sha256 does not match version.yaml; "
                           f"the pinned file changed after it was published")
    _RELEASE_CACHE[key] = path
    return path


def release_key_column(asset, release=None, start=None):
    """The key column of the table `release_file` returns (DrFirst's `<key>_original`)."""
    import yaml
    p = release_file(asset, release=release, start=start)
    if p is None:
        return None
    return yaml.safe_load((p.parent / "version.yaml").read_text())["key_column"]


def load_release_paths():
    """Import this module from a service without relying on PYTHONPATH."""
    return release_file, release_key_column
