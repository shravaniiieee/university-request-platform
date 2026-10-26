# University Request Management — Synthetic Data Pipeline

A reproducible Python/PostgreSQL project that generates university support tickets, policy articles, conversations, assignments, SLAs, resolution feedback, event history, and a separate anomaly ground-truth dataset.

## Features
- Fixed seed `20261022`; configurable full or starter scale.
- Required full volume: 5,000 tickets, 200 knowledge articles, 20,000 messages.
- Four categories: financial aid, registration, IT, accessibility.
- Deterministic IDs, referential integrity checks, business-hours SLA helper, versioned policy citations, labelled edge cases.
- CSV and JSON exports; PostgreSQL schema; validation and reproducibility scripts.
- Synthetic-only data. No real student or faculty information is included.

## Requirements
Python 3.10+ recommended. PostgreSQL 14+ is required only if you want to load the SQL schema/data into a database.

## Setup
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Generate the full dataset
Run from the repository root:
```bash
python src/generator.py --seed 20261022 --tickets 5000 --articles 200 --messages 20000 --requesters 1000
python src/validate_data.py
python src/reproducibility.py
pytest -q
```

Starter dataset for quick development:
```bash
python src/generator.py --outdir data/starter --seed 20261022 --tickets 100 --articles 20 --messages 400 --requesters 50
python src/validate_data.py
```
For starter validation, run `validate(data_dir="data/starter")` from Python or change the validator CLI path argument if using a local edit.

## Outputs
`data/generated/` contains one CSV and JSON file for each entity:
`roles`, `requesters`, `terms`, `policy_documents`, `knowledge_articles`, `categories`, `tickets`, `messages`, `assignments`, `slas`, `resolution_feedback`, `ticket_article_citations`, `ticket_events`, plus `ground_truth.csv/json` and `source_manifest.json`.

`reports/validation_summary.json` records validation results; `reports/reproducibility.json` stores checksums after two runs.

## PostgreSQL
Create a database, then run:
```bash
createdb university_requests
psql -d university_requests -f sql/schema.sql
```
CSV loading is intentionally left as a separate import step because local PostgreSQL credentials and paths differ by environment. Example:
```sql
\\copy roles FROM 'data/generated/roles.csv' CSV HEADER;
```
Run `\\copy` for each table in dependency order (parents before children). The ground-truth file is evaluation-only and should not be loaded into production feature tables.

## Business rules
- Route each category to its authorized default team.
- Retrieve/cite article versions whose effective dates cover the response timestamp.
- Ambiguous requests should request clarification or escalate.
- SLA targets are priority-based and use Monday-Friday 09:00-17:00 business hours.
- Keep lifecycle changes in `ticket_events`; do not overwrite history in a production workflow.
- Injected anomalies are labelled separately: expired citation, unauthorized team, unsupported response claim, elapsed-hours SLA, missing escalation.

## Data provenance
All generated people, messages, policies and articles are synthetic. `example.edu` links are placeholders and do not represent retrieved public policy documents. No external datasets are copied. This avoids uncertain redistribution licenses and personal-data risks.

## Reproducibility
The generator uses Python's `random.Random(seed)` and a fixed synthetic time anchor. Run the reproducibility script to compare SHA-256 checksums across two full runs. Keep the Python version and configuration constant when demonstrating identical output.

## Tests
```bash
pytest -q
```

## GitHub submission checklist
- [ ] Create a public repository named `university-request-platform`.
- [ ] Commit source, schema, tests, documentation, and the validation report.
- [ ] Decide whether generated data files fit repository size limits; otherwise publish a release artifact or a documented generation command.
- [ ] Confirm no secrets, local database credentials, or personal information are committed.
- [ ] Include seed, command, row counts, checksums, and test results in README.
- [ ] Verify `git clone` + setup + generation works in a clean environment.
- [ ] Push to GitHub and include the repository URL in the submission.
