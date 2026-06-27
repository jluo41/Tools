# 💡 How to install Codex in SAFE

## Status: stub. The exact steps depend on SAFE's egress and software policy, which is [TODO: JL].

This is the worked example for `/jhu-research-it`. It shows the honest pattern: state what is known, name the blockers, do not invent the procedure.

## What we know
- SAFE Desktop is a locked-down, HIPAA virtual desktop. It ships SAS, Stata, RStudio, Anaconda (Python), PowerBI, NVivo. (See `../20-safe.md`.)
- Codex CLI needs: Node.js, network access to the npm registry, and network access to the model API endpoint, plus an API key.
- In a secure enclave, outbound internet and installing new software are usually restricted or proxied.

## The two likely paths

### Path A — request it through IT (most likely the supported route)
1. Check the SAFE software catalog for an approved Node.js / Codex option.
2. If not present, file a software-install request with Research IT.
3. Software-request form / catalog link: [TODO: JL]
4. Fallback if you have no form link yet: contact Research IT through the help/FAQs page (https://researchit.jhu.edu/faqs/) and ask for the software-install path. [TODO: JL replace with the direct ticket/help-desk contact]

### Path B — install yourself (only if SAFE allows a terminal + egress)
1. Confirm Node.js is available (Anaconda may help, or a separate Node install). [TODO: JL confirm Node availability]
2. Confirm outbound access to the npm registry and to the model API host through the SAFE proxy. [TODO: JL confirm egress + proxy settings]
3. If both are allowed, install per the official Codex CLI instructions, set the API key, point it at the allowed endpoint.
4. Exact proxy env vars and allowed hosts: [TODO: JL]

## Blockers to resolve before this page is real
- [ ] Does SAFE allow outbound to the npm registry?
- [ ] Does SAFE allow outbound to the model API host?
- [ ] Is there an approved software-request path, and what is its link?
- [ ] Is using an external LLM API on PHI-adjacent enclave data allowed by policy / IRB? Route this through an AI HSR Consult (see `../70-ai-hsr-consult.md`). [TODO: JL, important]

Answer these and this how-to turns from a stub into a real procedure.
