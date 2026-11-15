"""Old name of focus_render (the page's build steps); kept so old imports keep working."""
from live.focus_render import *  # noqa: F401,F403
from live import focus_render as _new

globals().update({k: v for k, v in vars(_new).items() if not k.startswith("__")})
