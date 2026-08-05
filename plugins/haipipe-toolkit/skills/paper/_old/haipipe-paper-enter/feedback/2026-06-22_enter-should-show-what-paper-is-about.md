---
status: fixed
created: 2026-06-22
context: haipipe-paper-enter dashboard output
fixed_in: "haipipe-paper-enter v2.1.0"
---

When entering a paper, the dashboard should tell the user what this paper is about — not just the structural state. A new collaborator or a returning user after a break needs to be educated: what is the paper's question, what is the headline finding, who is the audience.

Currently the enter/dashboard output jumps straight into lifecycle layer, maturity, open needs — all operational. It does not surface the pitch (hook + surprise + so-what) or even the title and venue in a readable way.

The 1-pitch should be the FIRST thing a user sees when entering a paper: "here is what this paper is about in one minute." Then the operational state. The pitch exists in 0-lifecycle/1-pitch/1-pitch.tex for exactly this purpose — the enter skill should read it and render the kernel + hook + surprise at the top of the dashboard, before the status table.

Fix:
