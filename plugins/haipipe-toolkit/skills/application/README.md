# Application skill family

Application first understands what its design needs, then designs and delivers.

```text
Brief → Application-local Insight Pages → Design Pages → Artifact projections/Pages → Deploy
               D→I→K→W                 PageX
```

## Ownership

| Layer | Owns | Does not own |
|---|---|---|
| Task/Discovery | execution and source evidence | Application framing |
| Application Insight | Task-backed Probe, D→I→K, contextual W, Design Handoff | final message copy |
| Application Design | PageX selection, applicability, principles, message system, acceptance | raw Task/Discovery inspection |
| Artifact/Deploy | exact visible version and shipment record | evidence repair |

Folder ownership does not transfer evidence authority. An Insight Page lives in the Application folder but follows Task source/run/staleness rules.

## Page Types

```text
application/page-types/
├── haipipe-page-for-brief/          one Application frame + Insight Need Map
├── haipipe-page-for-insight/        one Task-backed Application insight question
├── haipipe-page-for-intervention/   many audience/job/venue Design Pages
└── haipipe-page-for-artifact/       optional independently governed unit
```

`page-type: intervention` is the machine key; **Design Page** is the user-facing name.

## Target runtime

```text
<application-root>/
├── board.md
├── 0-brief/A00-brief/
├── 1-insights/I<NN>-<slug>/
├── 2-design/D<NN>-<audience>-<job>/
├── 3-artifacts/
├── 4-deploy/
└── 5-rounds/vYYMMDD/
```

Each Insight Page may own `probe/`; Brief, Design, and Artifact Pages may not. Each Design Page owns `pagex/` bindings to exact Brief/Insight handoff material.

## Router

```text
/haipipe-application brief             frame the Application and Insight needs
/haipipe-application insight           run one local Task-backed DIKW Page
/haipipe-application design            author one audience/job/venue message system
/haipipe-application artifact          project or promote one independent unit
/haipipe-application review|deploy     exact-version gates
/haipipe-application iterate           measurement → Task → Insight refresh → Design reopen
```

## Compatibility

Legacy stage skills remain readers during migration. New work does not copy the descriptions/themes/claims/advice ladder, flat `1-probes/`, or the one-Intervention/many-Artifact target. External settled Insight Pages remain valid PageX inputs and are never moved automatically.
