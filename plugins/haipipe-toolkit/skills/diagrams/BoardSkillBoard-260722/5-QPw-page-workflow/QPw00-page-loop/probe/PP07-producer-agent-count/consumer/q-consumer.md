# Q-consumer · PP07-producer-agent-count

**The question, as this page needs it**
How many producer agents exist on disk for the page workflow's phases, and which phases lack one of their own?

**What this page loses if it never comes back**
C12.P3 claims the producer role is filled per phase, one agent per phase in the controller's own PRODUCER_AGENTS table. A missing agent does not error: the controller silently falls back to haipipe-page-creator-agent, so the claim can read true while a phase runs on the fallback. Without the measured roster, Aim A12.1 (one automatic router composing phase producers) rests on a design statement nobody counted.

**Where it is used**
`C12.P3.B3` in `outline/QPw00-page-loop-outline-v3.md`, and the sentence that bullet becomes.
