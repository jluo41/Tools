"""Old name of focus_styles_bands (shared CSS and band sections); kept so old imports keep working."""
from live.focus_styles_bands import *  # noqa: F401,F403
from live import focus_styles_bands as _new

globals().update({k: v for k, v in vars(_new).items() if not k.startswith("__")})
