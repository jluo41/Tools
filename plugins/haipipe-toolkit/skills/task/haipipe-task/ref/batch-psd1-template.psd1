# === Does this job run its runs one by one, or several at once? =============
# run_slice.ps1 refuses to start without this file, because "sequential" is not a
# safe guess: a job whose runs overwrite each other and a job whose runs are
# independent look identical from the outside.
#
#   Mode          'sequential' (one at a time) or 'parallel' (several at once)
#   Ceiling       the most that may run at once. -Parallel N cannot go above it.
#   CollisionKey  two runs that AGREE on every one of these fields write the same
#                 files, so they are put in different waves however wide the job
#                 runs. This is the correctness half; Ceiling is the capacity half.
#   Why           one line, printed before every batch so the reader sees it
#
# WHY PARALLEL IS SAFE
#   A regression run reads the stage-C data asset READ-ONLY and writes only
#   results/<task>/<run>/ plus its own STATATMP. Two runs share no writable path.
#
# WHY THE FULL COORDINATE SET IS THE COLLISION KEY
#   These are exactly the fields the run name is built from, so no two tickets
#   agree on all of them today. Declaring them anyway means that if a future
#   ticket ever did, the engine would serialize it instead of racing it.
#
# WHY THE CEILING IS 4
#   Capacity, not correctness: a Stata-process budget for the secure server.
#   Raise it here, with the reason, rather than passing a bigger -Parallel.


@{
    Mode         = 'parallel'
    Ceiling      = 4
    CollisionKey = 'Task,Trait,Window,Family'
    Why          = 'a regression reads the data asset read-only and writes only its own results folder; the ceiling of 4 is a Stata-process budget'
}
