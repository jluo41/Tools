Evidence Principles (总纲)
==========================

The root design goal behind every evidence rule in this skill family, and the four principles everything else derives from. When a new design question comes up, do not hunt for a matching sub-rule -- ask the four questions at the bottom.

Distilled 2026-07-05 from three live replication runs (seed-test / test-v002 / probe-test), each of which exposed one layer of the same disease.


The root goal
-------------

```
❌ enemy:  work that lives only in ONE conversation
           an agent says "I checked, it's fine" -> the session ends -> it evaporates
           the next session re-does the work, and nobody can trust the last conclusion

✅ goal:   a TRUSTWORTHY SHARED MEMORY on disk
           any fresh session or agent can open the tree and continue
           a ledger entry can be USED without re-verifying it
```

The system's real product is not any single paper -- it is a disk state a stranger agent can trust.


The four principles
-------------------

```
① 🏠 EVERYTHING LANDS, in its HOME layer
    external lit lives in discovery's sources.md (S## ids); internal data in task results
    the paper side holds only transcriptions + anchors pointing home
    -- without this, memory does not exist
       (run-3: the probe agent's search results died in its reply text)

② 🔍 EVERY LEDGER WRITE gets a second pair of eyes (produce != approve)
    whoever writes an entry does not approve it; the REVIEWER FOLLOWS WRITES
    -- without this, memory exists but cannot be trusted, so readers re-verify
       anyway and the ledger is worthless
       (run-3: the agent self-passed its own output; hollow cards cleared "acceptance")

③ 🧱 EACH LAYER does only ITS OWN work; other layers' work is ORDERED, not done
    client says WHAT, contractor decides HOW; never reach past your contractor
    -- without this, work bypasses the pipes that enforce ① and ②
       (four live bypasses: stage->discovery direct; worker inline consumption;
        stage pre-reading the project tree; agent inline searching)

④ ⚖️ economy may trim CEREMONY, never PRINCIPLE
    light modes MAY: skip folder creation, fold creator into orchestrator,
    run a single review pass -- the CREATOR FOLLOWS WORKLOAD
    light modes may NOT: skip landing, skip review-on-write, cross layers
    -- without this, ①②③ cost too much and everyone routes around them
```

They chain, they are not parallel:

```
③ layered orders   --ensures-->  work flows through the right pipe
① land-at-home     --ensures-->  the pipe's outlet is DISK, not chat
② review-on-write  --ensures-->  what is on disk can be TRUSTED
④ trim ceremony    --ensures-->  the above stays cheap enough that nobody bypasses it
                                       |
                          🏆 trustworthy shared memory
```


The four questions
------------------

For any new evidence-design decision:

1. Whose layer is this work? (③ -> order it, don't do it)
2. Where does the result live? (① -> its home ledger, with an id)
3. Who reviews the write? (② -> someone other than the writer)
4. Which ceremony can be trimmed? (④ -> folders/loops yes, landing/review no)


Where the principles are enforced
---------------------------------

```
③  wiki/08-stage-gate.md Phase Transition Contract rule 4 (stage/worker);
   the executor orchestrators' clean context IS the wall (agent level)
①  haipipe-task-orchestrator-agent / haipipe-discovery-orchestrator-agent
   "fresh evidence must land" — the answer is a FILE: <task-folder>/QA/<n>-<slug>.md,
   which the section's `target:` then points at;
   a CLAIM's status lands in 0-lifecycle/1-claims/1-claims.md — per-claim,
   per-paper, private. 💀 `## Verdict` and `verdicted` are DELETED (R7); the
   probe section carries only its `reading:`.
②  discovery creator/reviewer loops (full) + reviewer quick-pass (ENRICH);
   probe Judge gates G1/G2/G3; paper-probe worker mechanical acceptance
④  probe light reuse (zero-write => zero ceremony);
   discovery ENRICH (no new folder, creator folded, one review pass)
```
