# Audience Profile Schema

Every audience profile is a uniform 3-file pack (modeled on paper's
venue packs under `_venue/_SCHEMA.md`).

```
profile-<audience>/
├── README.md           hub: tone, length, citation format, lifecycle mappings
├── style-profile.md    voice examples to imitate
└── exemplars/          real messages/reports to pattern-match
```

Audience profiles are **knowledge, not skills**. They are consulted
by path, never invoked as skills. Every lifecycle stage that produces
audience-facing content reads the matching profile.


Lifecycle mappings (in README.md)
===================================

Each profile declares how it affects 4 lifecycle stages:

```
→ Claims:     what counts as a sufficient claim for this audience
→ Design:     tone, reading level, channel constraints
→ Variants:   standard variant set (e.g., patient always gets SMS)
→ Draft:      style to imitate from exemplars/
```


Available audiences
====================

```
patient       end-user (warm, plain, ≤ 200 words, no K-id in body)
clinician     provider (clinical precision, ≤ 400 words, inline K-id)
regulator     FDA/IRB (formal, ≤ 1500 words, footnote citations)
executive     leadership (direct, ≤ 600 words, endnote citations)
designer      UX/product (visual, ≤ 300 words + sketch)
dev           engineer (terse, ≤ 500 words + interface spec)
partner       collaborator (professional, ≤ 800 words, inline cites)
```
