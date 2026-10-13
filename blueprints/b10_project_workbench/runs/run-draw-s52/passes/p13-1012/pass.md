# Sign-in fixed: recent codes, limit, owner Home

## Ask

(screenshot) No response.

## Summary

Rate limit (5/hour) had silently stopped new codes and a newer code replaced the emailed one; now any code within 10 minutes works, limit 10/hour, page says so, owner Home is the share list; verified through block.jjluo.com; JL's count cleared; D14

## Changed

- `plugins/haipipe-toolkit/servers/_host/live/share.py`
- `plugins/haipipe-toolkit/servers/_host/tests/test_share.py`
- `blueprints/b10_project_workbench/studio/s52-host-and-share/s52-host-and-share.md`
