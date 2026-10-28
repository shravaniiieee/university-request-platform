\*\*Role:\*\* Associate AI Forward Deployed Engineers — AI Forward Deployed Engineer



\## 1. Problem Statement



\### Business Context / Problem Route



Route student and faculty requests, retrieve policy-grounded answers, and track resolution and escalation.



\### Objective and Scope



Build a working solution for this end-to-end workflow: route student and faculty requests, retrieve policy-grounded answers, and track resolution and escalation.



The solution should expose key decisions and exceptions, preserve traceability, and produce measurable outputs.



Medium complexity means multiple related entities, conditional rules, at least one exception path, and meaningful evaluation metrics.



\### Primary Actors / Systems



\- Learner

\- Instructor

\- Academic administrator

\- Support staff

\- Platform administrator



\## 2. Business Workflow and Rules



1\. Generate or reference master data first: Requester, Role, Term, PolicyDocument, KnowledgeArticle.

2\. Generate dependent transaction and event records using valid parent IDs.

3\. Apply business logic:

&#x20;  - Create public or synthetic policy articles with versions and effective dates.

&#x20;  - Generate tickets across financial aid, registration, IT, and accessibility.

&#x20;  - Create message histories.

&#x20;  - Define routing and SLA rules.

&#x20;  - Link responses to applicable sources.

&#x20;  - Record resolution and feedback.

4\. Persist state changes as explicit records or events where relevant; do not overwrite history.

5\. Generate outcomes and ground-truth labels from documented rules, not independent random assignment.



\## 3. Entities and Relationships



\### Core Entities



Requester, Role, Term, PolicyDocument, KnowledgeArticle, Ticket, Message, Category, Assignment, SLA, and ResolutionFeedback.



Requirements:



\- Define a primary key for every entity and foreign keys for every relationship.

\- Document cardinality (1:1, 1:N, N:M), optional relationships, effective dates, and lifecycle states.

\- Use bridge tables for many-to-many relationships.

\- Retain event history for state changes.

\- Validate all joins.

\- For deliberate anomaly cases, keep an `issue\_type` or `ground\_truth` label rather than silently corrupting unrelated rows.



\## 4. ID / Nomenclature Conventions



Use the following conventions:



\- Ticket: `TKT-2026-000001`

\- Message: `MSG-<ticket-id>-001`

\- Knowledge article: `KB-000001`

\- Policy: `POL-<domain>-2026-001`

\- SLA: `SLA-<ticket-id>`



\## 5. Synthetic Data Generation Instructions



\### Step 1 — Data Dictionary



Write a data dictionary for Requester, Role, Term, PolicyDocument, KnowledgeArticle, Ticket, Message, Category, Assignment, SLA, and ResolutionFeedback.



For each field, specify its type, required or optional status, allowed values, units, uniqueness, and validation rule.



\### Step 2 — Generation Order and Domain Logic



Create parent/master tables first, followed by child and event tables.



Apply the domain-specific generation logic:



\- Create public or synthetic policy articles with versions and effective dates.

\- Generate tickets across financial aid, registration, IT, and accessibility.

\- Create message histories.

\- Define routing and SLA rules.

\- Link responses to applicable sources.

\- Record resolution and feedback.



\### Step 3 — Deterministic IDs



Use the specified naming conventions for tickets, messages, knowledge articles, policies, and SLAs.



Keep counters zero-padded, IDs immutable, and referenced IDs exactly consistent across files.



\### Step 4 — Baseline Data Volume



Generate:



\- 5,000 tickets

\- 200 articles

\- 20,000 messages



Include ambiguous questions, outdated policies, urgent deadlines, and cases requiring human escalation.



Use a fixed seed, such as `20261022`, and parameterize the scale so starter and full datasets use the same generator.



\### Step 5 — Labelled Edge Cases



Generate valid baseline records first, then inject labelled edge cases:



1\. Answer cites expired policy.

2\. Ticket routed to unauthorized team.

3\. Response claims unsupported fact.

4\. SLA clock ignores business hours.

5\. Escalation not triggered.



\### Step 6 — Derived Values



Calculate derived values, including totals, balances, scores, statuses, and dates, from source records rather than generating them independently.



\### Step 7 — Separate Ground Truth



Produce a separate `ground\_truth.csv` or `ground\_truth.json` for known anomalies, expected decisions, or labels.



Never leak ground truth into input features.



\### Step 8 — Validation



Run validation for:



\- Primary-key uniqueness

\- Foreign-key integrity

\- Allowed enumerations

\- Date ordering

\- Arithmetic reconciliation

\- Lifecycle transitions

\- Duplicate checks



\### Step 9 — Deliverables and Documentation



Export CSV, JSON, and SQL seed data, along with:



\- README

\- Database schema and data dictionary

\- Generator command

\- Fixed seed

\- Source manifest

\- Validation summary



\### Step 10 — Reproducibility



Regenerate the dataset twice with the same seed and compare row counts and checksums to demonstrate reproducibility.



\## 6. Suggested Volume and Coverage



Generate 5,000 tickets, 200 articles, and 20,000 messages.



Include ambiguous questions, outdated policies, urgent deadlines, and cases requiring human escalation.



\## 7. Required Edge Cases / Negative Scenarios



\- Answer cites expired policy.

\- Ticket routed to unauthorized team.

\- Response claims unsupported fact.

\- SLA clock ignores business hours.

\- Escalation not triggered.



\## 8. Validation Rules / Acceptance Criteria



\- Answers cite current sources.

\- Routing is consistent.

\- Unresolved or ambiguous cases escalate.

\- Article version is recorded.



\## 9. Evaluation Focus



Generated data will be reviewed for:



a. Realistic distributions and meaningful variation.



b. Consistent IDs and valid joins.



c. Dependency and lifecycle consistency across entities.



d. Correct derived values and reconciliation.



e. Normal, boundary, failure, and exception coverage.



f. Separate ground truth.



g. Fixed-seed reproducibility, documentation, and lawful provenance.



\## 10. Public Data Guidance / Lawful Use



External data is optional.



If used, record the source URL, dataset and version, retrieval date, license or terms, attribution, transformations, and fields discarded.



Use only data that you are legally permitted to access and redistribute. Do not bypass access controls or collect confidential or personal information.



If licensing or suitability is unclear, use synthetic data and cite public reference data only for schema inspiration.

