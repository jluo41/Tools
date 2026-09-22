# haipipe-page-guide · Content preview

Accepted candidate snapshot; adopted into Page Content under the user's direct CONTENT instruction on 260913. The Page Markdown source remains authoritative.

## C1.P1.B1
plan: v0.1
bullet-sha256: 3c39feabcdc07338740c84daa0c99410e68b8764ebd46a611c61558a9d93a937

A Page Folder keeps everything needed to understand, change, and deliver one Page in one place. It can hold the Markdown source, code, figures, evidence, Runs and Results, and generated web, LaTeX, and Word files. Studio is where people brainstorm for the Page. Studio Chat keeps the conversation, while Studio Draw turns ideas into visual sketches.

## C1.P1.B2
plan: v0.1
bullet-sha256: eb31b359d5475f880c8c90e1a05acccb9b4d287535fc8e43b5c76918ec26de1c

The Markdown source uses the same stem as the folder: haipipe-page-guide/ corresponds to haipipe-page-guide.md.

## C1.P1.B3
plan: v0.1
bullet-sha256: b647d8a7535c8f14f1f4d48c6417e9ad42436ae183903d6a9928f13ba74b11d5

Each delivery file is generated from that Markdown source instead of maintained as a separate source. The earlier HTML draft is kept only as material and does not control this Page or its outputs.

## C2.P2.B1
plan: v0.1
bullet-sha256: 084a3371c690237328ffb19d68ffb4d378568c7e713346fbff1706e1c5051884

Board supplies grouping, ordering, and navigation by registering the same Page Face. Removing that membership should leave the Page Folder and its content intact.

## C2.P2.B2
plan: v0.1
bullet-sha256: e10ea7a94020f39af65e8742eb5d56db109c6eff7f968d68799af36030b7898a

Workbenches present the Page's planning records, conversations, runs, outputs, and files through their own declared writers.

## C2.P2.B3
plan: v0.1
bullet-sha256: b59e53b3d1d2f2f4007d31de70e9007e85c8288cb33b79faf9790aa38e8562b9

Putting a workbench's name on a folder or button is not enough; the workbench must actually open the Page's records and perform the actions it promises.

## C2.P3.B1
plan: v0.1
bullet-sha256: 85eea34a3bca46a51894e72de49616d56277f3617129dd4cfca33a382f6b47ff

Each Page Run has a local identity and a Version that stores its feedback Steps.

## C2.P3.B2
plan: v0.1
bullet-sha256: 9840e3bac03b3afe59d65184cebea73beb71055644ab1cd79e9441c29079dfe4

Task Runs keep their native identity and return delegated outputs, such as paragraph drafts or Discovery results, for the Page to use.

## C2.P3.B3
plan: v0.1
bullet-sha256: 0cd8f9e79997b626ffd41074e9e30a32c01c90098e00772a1b715385337dadec

The `rpNN` and Task `rNN` sequences are independent, so `rp01` and `r01` may coexist in one Page Folder.

## C2.P3.B4
plan: v0.1
bullet-sha256: c65396a2de44c93b5ecc825fff9f9bde9d90d9f72ba887b41b9ec3c50c26c708

An automated CONTEXT-to-CHECK controller invocation is a Page workflow pass, not another Page Run.

## C2.P4.B1
plan: v0.1
bullet-sha256: bfa3e9cdee71f7b96a7aea5a19b6102fbdf326a1e0cdda39b558d4450d530809

The Page's Runs function proposes bounded interaction goals when a person needs to shape, compare, revise, or accept the Page itself.

## C2.P4.B2
plan: v0.1
bullet-sha256: d7f290c6b1bd84c3194fbc0a6b5e132fa5e633f49dda140c0bdc349d6ee01770

A proposal is not yet a Run and receives no `rpNN` until the person selects or directly commissions it.

## C2.P4.B3
plan: v0.1
bullet-sha256: 8a235eeb3613e84972bb8d36bfc2cd728d46901a85225d88db7f9f6acd7cbf51

A selected candidate resumes a matching open Page Run or allocates the next `rpNN` for an independent goal, and later feedback appends Steps to that Run's current Version.

## C2.P4.B4
plan: v0.1
bullet-sha256: a81ff108f7b5fd47db545b04c560839ab4bac0496f7c2851e429dd6e1cac18b5

Code, search, data, rendering, build, Discovery, and other output-producing work remains a normal Task Run even when a later human gate reviews its Result.

## C2.P5.B1
plan: v0.1
bullet-sha256: dddfd60205b38d92634b3021b44a2cb70e7e30ad15af962905917c74a3629fec

The first Page Run is always `rp-struct-01`, one shared Structure Run where the person and agent complete SHAPE and SURVEY for the whole Page until the person explicitly closes it. Multiple people may contribute Steps to this same Run.

## C2.P5.B2
plan: v0.1
bullet-sha256: cf7cdc6735215594c1b7a8b113ae52bb14314ac44b3ed8f43d25176579cc6f06

That Structure closure freezes the Page-global reading order as `P01`, `P02`, through `PN`, with every serial mapped to its plan address.

## C2.P5.B3
plan: v0.1
bullet-sha256: 1fe1200489a613fca5d3d921569a7b899339ce0fc03a5e92a12ea5ae9ee267f6

After the Structure closes, the Runs function creates Steps, each with a scope covering one or more of the `N` numbered paragraphs.

## C2.P5.B4
plan: v0.1
bullet-sha256: d80abe0efb1d62b802d7efcca45844f80874b6d2d9b27ddc85b96c4df8685364

Each selected paragraph Run uses a typed identity that exposes the exact serial or contiguous range, such as `rp-para-01_P01` or `rp-para-02_P02-P03`; its descriptive wording stays in Goal.

## C2.P5.B5
plan: v0.1
bullet-sha256: 1a5c642417f3f900eea9488111dfc5f07af7b9faf3f376b63ac85130b10998d9

Different human questions or acceptance boundaries call for different Step scopes, while code, Discovery, data, rendering, and build remain normal Task Runs.

## C3.P6.B1
plan: v0.1
bullet-sha256: d302d3d704f5037ab57f2ca2d8f61d712f626e50c4c20cc5e615b27db98bf94e

A request to revise Opening sets the editing boundary; it does not authorize rewriting the rest of the Page.

## C3.P6.B2
plan: v0.1
bullet-sha256: 9acebb0acfacc2a605f66ef118b7dd58bbaf8f0af0098534d4cce8522d78eb2c

During planning, the Outline workspace pairs each planned point with candidate prose for discussion.

## C3.P6.B3
plan: v0.1
bullet-sha256: 5078e2da3a121482094dc267d7e487ea7d391e4c282bd2086c5b2e9348c7308f

A Writing Run preserves the goal and feedback history through Versions and Steps, while accepted wording is adopted into Content through the Page workflow. Those records do not imply that a browser button executes an agent, and accepting one passage does not accept the whole Page.
