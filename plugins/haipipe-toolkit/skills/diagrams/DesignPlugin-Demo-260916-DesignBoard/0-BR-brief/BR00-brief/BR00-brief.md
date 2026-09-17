# Design Brief
folder-kind: brief

## Opening

Create a small set of patient-facing reminders whose wording can be reviewed
before any downstream implementation.

## Outline

The Brief freezes the audience, venue, design intent, and signed Insight input.

## Content

### 8 · What to design

One line per audience × job × venue. `designs` says how many designs the line
asks for. A line's `folder` names the Design Folder that serves it; `—` means
the folder has not been opened yet, and the Board-level Design plugin opens it
from this line.

| line | audience | job | venue | designs | folder |
|---|---|---|---|---|---|
| R1 | full SMSR2 population, unconditioned | prescription review | sms | 10 | `Design-01-patient-confirm-sms` |
| R2 | patients with a refill due within 7 days | refill review | ui-card | 1 | `Design-02-refill-reminder-ui` |
| R3 | young male, age 35 or under | prescription review | sms | 1 | — |
