"""The live layer: one ``live`` namespace over every server folder.

``serve.py`` composes its handler from mixins named ``live.<module>``. The
transport mixins (``base``, ``auth``) sit in this package; every other module
sits in the server folder that owns it (``servers/haipipe-board``,
``servers/workbench-page``, ``plugins/subjective-label/servers/workbench-labeling``,
...) and is grafted onto this package's search path here. Module names are
unique across folders, so ``from live.outline import OutlineMixin`` resolves the
same way wherever the file lives.
"""
import sys
from pathlib import Path

_HOST = Path(__file__).resolve().parents[1]
if str(_HOST) not in sys.path:
    sys.path.insert(0, str(_HOST))

from host_paths import bootstrap  # noqa: E402
from host_registry import live_folders  # noqa: E402

bootstrap()
for _folder in live_folders():
    if str(_folder) not in __path__:
        __path__.append(str(_folder))
