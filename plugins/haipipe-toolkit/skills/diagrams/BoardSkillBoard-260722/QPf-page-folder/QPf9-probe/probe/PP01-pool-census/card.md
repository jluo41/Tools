# PP01-pool-census
question: Which papers and applications in the toolkit still carry a `1-probes/` pool, and how many PPNN cards live in each?
state: bound
binding: → tasks/A01_repo_inventory/01_scan_1probes_dirs/QA/1-scan-1probes-dirs.md
stake: A1.2 retires `1-probes/`; the migration cannot be scoped, sequenced, or declared done without this census.

## Q-executor
Scan the repository at /Users/floydluo/Desktop/Tools-SPACE for directories named `1-probes`. For each one found, report the owning paper or application folder and how many PP-numbered entries it holds, listing their names.
Deliverable: QA digest + a machine-readable listing. Accepted: complete list | none-found.

## bank binding
route: task · bank: new → answered · target: the binding line above

## A-executor
Three `1-probes` directories exist, all inside fixture or test folders of skill packages: the paper fixture (2 entries), the application fixture (0), and the probe skill's test fixture (1). No live paper or application in this repository carries one.
