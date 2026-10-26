# University Request Management — Synthetic Data Pipeline

A reproducible Python and PostgreSQL pipeline for generating, validating, and storing synthetic university support-request data.

## Overview

University support teams manage requests involving financial aid, registration, IT services, accessibility, and other administrative processes. These workflows require structured data representing requesters, support tickets, conversations, policy documents, knowledge articles, assignments, service-level agreements (SLAs), and resolution history.

This project generates a configurable synthetic dataset representing these workflows. It provides CSV and JSON exports, a relational PostgreSQL schema, data-quality validation, reproducibility checks, automated tests, and documentation.

The project is intended for development, data-quality analysis, relational database exercises, and evaluation of request-management workflows. It does not represent a deployed university helpdesk application.

**Project status:** Core generation, validation, and PostgreSQL import verified in the local development environment.

## Key Features

- **Reproducible generation:** Seed-based dataset generation with configurable record volumes.
- **Relational data model:** 13 entities connected through primary keys and foreign keys.
- **Multiple export formats:** CSV and JSON for downstream processing.
- **Data-quality validation:** Checks for duplicate identifiers, selected foreign-key relationships, record counts, and invalid priority values.
- **PostgreSQL support:** SQL schema and instructions for importing generated CSV files.
- **Evaluation scenarios:** Separate ground-truth records and labelled synthetic edge cases.
- **Automated testing:** pytest-based test suite.
- **Documentation:** Schema overview, data dictionary, setup instructions, and validation reports.

## Technology Stack

| Technology     | Purpose                                     |
| -------------- | ------------------------------------------- |
| Python 3.10+   | Data generation and validation              |
| PostgreSQL 14+ | Relational data storage                     |
| SQL            | Schema definition, constraints, and queries |
| Faker          | Synthetic sample-data generation            |
| psycopg        | PostgreSQL connectivity support             |
| pytest         | Automated testing                           |
| CSV and JSON   | Data export and exchange                    |
| Git and GitHub | Version control and submission              |

## Architecture

```text
Generation Configuration
          |
          v
   Python Generator
          |
          v
 Synthetic Dataset
     CSV + JSON
          |
          +-------------------+
          |                   |
          v                   v
 Python Data Validator    PostgreSQL Schema
          |                   |
          v                   v
 Validation Report       CSV Data Import
                              |
                              v
                     Relational Database
                              |
                              v
                    SQL Queries and Checks
```

The Python pipeline generates the dataset independently of PostgreSQL. The database is an optional persistence layer for relational queries and database-level validation.

## Dataset

The full configuration uses seed `20261022` and generates the following records.

| Entity                       |    Records |
| ---------------------------- | ---------: |
| Roles                        |          5 |
| Requesters                   |      1,000 |
| Academic terms               |          4 |
| Policy documents             |         50 |
| Knowledge articles           |        200 |
| Categories                   |          4 |
| Tickets                      |      5,000 |
| Messages                     |     20,000 |
| Assignments                  |      5,000 |
| SLAs                         |      5,000 |
| Resolution feedback          |      1,873 |
| Ticket-article citations     |      5,000 |
| Ticket events                |      9,623 |
| **Total relational records** | **51,759** |

The ground-truth dataset contains an additional five records and is maintained separately from the 13 relational entities.

### Data model

The principal relationships include:

- Requesters reference roles.
- Tickets reference requesters, categories, and academic terms.
- Knowledge articles reference policy documents.
- Messages, assignments, SLAs, resolution feedback, and ticket events reference tickets.
- Ticket-article citations reference tickets, knowledge articles, and messages.

The supported categories are financial aid, registration, IT, and accessibility.

The generated data also includes synthetic edge cases involving expired citations, unauthorized assignments, unsupported response claims, SLA scenarios, and missing escalations. These scenarios are intended for evaluation; their presence does not guarantee that every anomaly is detected by the current validator.

## Repository Structure

```text
university-request-platform/
├── data/
│   └── generated/          # Generated CSV and JSON datasets
├── docs/
│   ├── AI_PROMPT_HISTORY.md
│   ├── data_dictionary.md
│   └── schema.md
├── reports/
│   ├── validation_summary.json
│   └── reproducibility.json
├── sql/
│   └── schema.sql
├── src/
│   ├── generator.py
│   ├── validate_data.py
│   └── reproducibility.py
├── tests/                  # Automated tests
├── .gitignore
├── requirements.txt
└── README.md
```

This tree describes the intended project layout. Check the actual repository contents before submission, particularly the reports and generated artifacts.

## Environment Requirements

- Python 3.10 or later.
- pip for dependency installation.
- PostgreSQL 14 or later for database import and SQL validation.
- Git for cloning and version control.

PostgreSQL is not required for dataset generation or Python-only validation.

The setup commands below use Windows PowerShell. Linux and macOS users can adapt the virtual-environment activation command.

## Installation and Setup

### 1. Clone the repository

After creating the public GitHub repository, clone it:

```bash
git clone <YOUR_PUBLIC_REPOSITORY_URL>
cd university-request-platform
```

Alternatively, navigate to your existing local project directory.

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify the Python installation:

```bash
python --version
```

## Generate the Dataset

Run the following command from the repository root:

```bash
python src/generator.py --seed 20261022 --tickets 5000 --articles 200 --messages 20000 --requesters 1000
```

The command generates the full dataset using the specified seed and record volumes. Generated files are expected under `data/generated/`.

### Validate the generated data

```bash
python -m src.validate_data --data-dir data/generated
```

A successful validation reports:

```json
{
  "passed": true,
  "errors": []
}
```

The complete output contains additional metrics. The snippet above shows only the essential success indicators.

### Run the automated tests

```bash
python -m pytest -q
```

For detailed test names and output:

```bash
python -m pytest -v
```

### Check reproducibility

```bash
python src/reproducibility.py
```

The reproducibility script is intended to compare generated outputs using checksums. Review `reports/reproducibility.json` if the script produces that file.

A reproducibility claim should be supported by actual checksum results under a consistent Python environment and configuration.

## PostgreSQL Setup and Import

PostgreSQL is an optional component for persisting and querying the generated data.

### 1. Create the database

Connect to your local PostgreSQL server:

```bash
psql -U postgres -d postgres
```

At the PostgreSQL prompt, execute:

```sql
CREATE DATABASE university_requests;
\connect university_requests
```

If the database already exists, connect to it rather than creating it again.

### 2. Create the schema

From PowerShell, run:

```powershell
psql -U postgres -d university_requests -f sql/schema.sql
```

Alternatively, from inside psql while connected to `university_requests`:

```sql
\i 'sql/schema.sql'
```

### 3. Import the CSV files

From the repository root, run the following commands inside psql, connected to `university_requests`.

Import parent tables before dependent tables:

```sql
\copy roles FROM 'data/generated/roles.csv' WITH (FORMAT csv, HEADER true);
\copy requesters FROM 'data/generated/requesters.csv' WITH (FORMAT csv, HEADER true);
\copy terms FROM 'data/generated/terms.csv' WITH (FORMAT csv, HEADER true);
\copy policy_documents FROM 'data/generated/policy_documents.csv' WITH (FORMAT csv, HEADER true);
\copy knowledge_articles FROM 'data/generated/knowledge_articles.csv' WITH (FORMAT csv, HEADER true);
\copy categories FROM 'data/generated/categories.csv' WITH (FORMAT csv, HEADER true);
\copy tickets FROM 'data/generated/tickets.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy messages FROM 'data/generated/messages.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy assignments FROM 'data/generated/assignments.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy slas FROM 'data/generated/slas.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy resolution_feedback FROM 'data/generated/resolution_feedback.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy ticket_article_citations FROM 'data/generated/ticket_article_citations.csv' WITH (FORMAT csv, HEADER true, NULL '');
\copy ticket_events FROM 'data/generated/ticket_events.csv' WITH (FORMAT csv, HEADER true, NULL '');
```

Each successful command reports the number of imported rows.

**Important:** Do not run an import command a second time against an already-populated table. Duplicate primary-key values will cause an error. For a clean repeatable import, use a fresh database or deliberately reset the existing data after backing up anything you need.

The ground-truth files are separate evaluation artifacts and are not included in the 13-table import sequence.

### 4. Verify the tables

Inside psql:

```sql
\pset pager off
\dt
```

You should see all 13 relational tables.

### 5. Verify record counts

```sql
SELECT 'roles' AS table_name, COUNT(*) AS total FROM roles
UNION ALL SELECT 'requesters', COUNT(*) FROM requesters
UNION ALL SELECT 'terms', COUNT(*) FROM terms
UNION ALL SELECT 'policy_documents', COUNT(*) FROM policy_documents
UNION ALL SELECT 'knowledge_articles', COUNT(*) FROM knowledge_articles
UNION ALL SELECT 'categories', COUNT(*) FROM categories
UNION ALL SELECT 'tickets', COUNT(*) FROM tickets
UNION ALL SELECT 'messages', COUNT(*) FROM messages
UNION ALL SELECT 'assignments', COUNT(*) FROM assignments
UNION ALL SELECT 'slas', COUNT(*) FROM slas
UNION ALL SELECT 'resolution_feedback', COUNT(*) FROM resolution_feedback
UNION ALL SELECT 'ticket_article_citations', COUNT(*) FROM ticket_article_citations
UNION ALL SELECT 'ticket_events', COUNT(*) FROM ticket_events;
```

Compare the results with the expected counts in the Dataset section.

## Verification Results

The following results were observed during the local project run.

| Verification                                            | Observed result |
| ------------------------------------------------------- | --------------- |
| Dataset validation                                      | Passed          |
| Validator errors                                        | 0               |
| Duplicate primary keys in checked datasets              | 0               |
| Invalid foreign-key references in checked relationships | 0               |
| Invalid priority values                                 | 0               |
| Tickets generated                                       | 5,000           |
| Messages generated                                      | 20,000          |
| Knowledge articles generated                            | 200             |
| Ground-truth records                                    | 5               |
| PostgreSQL tables imported                              | 13              |
| Python tests                                            | 3 passed        |

The PostgreSQL row-count query matched the expected counts for all 13 tables. Additional SQL queries returned zero invalid references for the ticket, message, article, assignment, SLA, feedback, citation, and event relationships checked.

These results demonstrate that the recorded generation, validation, import, and test runs succeeded. They do not establish that every possible business rule or edge case has been fully tested.

## Business Rules and Evaluation Scenarios

The project documentation describes these intended rules:

- Categories map to authorized default teams.
- Policy documents and knowledge articles are versioned.
- Article citations should refer to versions effective at the response timestamp.
- Ambiguous requests should trigger clarification or escalation.
- SLA targets depend on priority and use Monday–Friday, 09:00–17:00 business hours.
- Ticket lifecycle changes are represented in the event history.
- Injected anomalies are labelled separately in the ground-truth dataset.

The current validator focuses on selected structural and relational checks. Additional automated tests are needed to establish complete enforcement of these rules.

## Data Provenance and Privacy

All generated people, messages, policies, and articles are synthetic. The `example.edu` links are placeholders, not verified external policy sources.

The project is not intended to reproduce actual student or faculty records. Before publication, inspect the repository for personal files, credentials, local database configuration, and other sensitive material.

## Known Limitations

1. **Synthetic dataset:** The records are illustrative and should not be interpreted as real university activity or operational statistics.
2. **No production integrations:** The project does not connect to real student information systems, identity providers, email services, or policy repositories.
3. **No hosted application:** The deliverable is a data pipeline and relational schema, not a web application or dashboard.
4. **Limited test coverage:** The recorded test suite contains three passing tests. More edge-case and business-rule tests would improve confidence.
5. **Validation coverage:** The validator does not prove the correctness of every business rule, anomaly, citation timing condition, or SLA calculation.
6. **Small ground-truth set:** Five evaluation records are not sufficient for statistically robust benchmarking.
7. **Reproducibility:** Identical output files should be demonstrated with checksum comparisons under a consistent environment.
8. **Database imports:** The CSV import commands must be run in dependency order, and tables must not be populated repeatedly with the same records.

## Troubleshooting

### Python or pip is not recognized

```powershell
python --version
python -m pip --version
```

Confirm that Python is installed and available on PATH.

### PostgreSQL is not recognized

On a typical Windows installation, `psql.exe` may be under:

```text
C:\Program Files\PostgreSQL\<version>\bin\psql.exe
```

Use the actual installed version or add its `bin` directory to PATH.

### Duplicate primary-key error during import

The table may already contain records from a previous import. Check the table count and continue with the remaining tables if appropriate. Do not blindly repeat successful imports.

### Foreign-key violation

Check that the parent table was loaded before the child table and that all CSV files came from the same generated dataset.

### Validation failure

Inspect the validator's error list, correct the underlying data or generation logic, regenerate affected data when necessary, and rerun validation and tests.


## Conclusion

The University Request Management Synthetic Data Pipeline provides a reproducible foundation for generating structured support-request data and loading it into PostgreSQL. The recorded run passed the implemented validation checks, imported all 13 relational tables with expected row counts, and passed three automated tests.

Future improvements should expand business-rule testing, strengthen SLA and anomaly validation, increase ground-truth coverage, and demonstrate reproducibility in a clean environment.
