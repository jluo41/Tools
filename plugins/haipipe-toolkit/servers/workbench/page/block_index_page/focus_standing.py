"""Old name of focus_plan_results (Plan + Results); kept so old imports keep working."""
from live.focus_plan_results import *  # noqa: F401,F403
from live import focus_plan_results as _new

globals().update({k: v for k, v in vars(_new).items() if not k.startswith("__")})
