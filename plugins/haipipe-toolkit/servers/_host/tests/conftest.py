"""Make the host importable from tests/: `live.*`, `serve`, `server_config`, `host_*`."""
import sys
from pathlib import Path

_HOST = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_HOST))
