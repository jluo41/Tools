# j06 · The API

job-of: b02_haipipe-utils (261009)
spine: `servers/`: one host (:8070) with a lane per noun (/food, /exercise, /medication, /insulin), each answering healthz, normalize and normalize/batch; food also takes images.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

The host mounts every lane under one port; a caller's client.py switches between local and http transport. The
host suite passes here (10 of 10). Each lane's suite is a script that drives a running service through its
<NOUN>NORM_URL, so pytest cannot collect them.

## Questions

```yaml
questions:
- id: Q01
  title: How is the API tested and run?
  question: The lane suites are scripts against a running service and only the host suite needs no bank; where does
    the service run (it needs the banks), and should the suites run under one runner?
  hypothesis: Run the host where the banks are; give run_suites.py one entry that starts the host, runs every lane's
    suite and stops it.
  acceptance: Answered when one command runs every suite against a fresh host and reports per lane.
  work: []
  report: reports/q01_api_tests/q01_api_tests.md
```
