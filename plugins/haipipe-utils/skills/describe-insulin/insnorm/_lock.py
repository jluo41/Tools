"""
The event lock, read through haipipe-norm/paths.py beside this skill (no PYTHONPATH needed).

    lock_file(asset, filename=None)   the pinned file of an ext_ asset, sha256 checked, or None
    lock_key_column(asset)            that table's key column (<key>_original), or None

None means no lock or no pin: the caller keeps its old flat-folder path. Set
EVENTNORM_LOCK=none to force the old paths; a checksum mismatch raises.
"""
import importlib.util
import pathlib


def _load():
    here = pathlib.Path(__file__)
    for base in (here.absolute(), here.resolve()):
        p = base.parents[2] / "haipipe-norm" / "paths.py"
        if p.exists():
            spec = importlib.util.spec_from_file_location("haipipe_norm_paths", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


_paths = _load()


def lock_file(asset, filename=None):
    return _paths.lock_file(asset, filename) if _paths else None


def lock_key_column(asset):
    return _paths.lock_key_column(asset) if _paths else None
