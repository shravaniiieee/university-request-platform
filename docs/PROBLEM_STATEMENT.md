# Problem Statement

## Role

**Associate AI Forward Deployed Engineers — AI Forward Deployed Engineer**

## 1. Problem Statement

Build a synthetic university request management dataset and supporting data model for routing student and faculty requests, retrieving policy-grounded answers, and tracking resolution and escalation.

The dataset should represent realistic university workflows, including requesters, roles, academic terms, policy documents, knowledge articles, tickets, messages, assignments, SLAs, resolution feedback, and event history.

## 2. Requirements

### Data Model

- Define the required entities, primary keys, foreign keys, relationships, cardinalities, and optional relationships.
- Include effective dates, lifecycle states, bridge tables, and event history.
- Follow the naming conventions and identifier formats specified in the original assignment.

### Synthetic Data Generation

- Generate 5,000 tickets, 200 knowledge articles, and 20,000 messages.
- Use a fixed random seed, such as `20261022`, and support configurable dataset sizes.
- Keep ground-truth labels separate from input features.

### Edge Cases

Include cases such as:

- Answers citing expired policies.
- Tickets routed to unauthorized teams.
- Responses containing unsupported facts.
- SLA calculations that ignore business hours.
- Escalations that fail to trigger.

### Validation

Validate primary-key uniqueness, foreign-key integrity, enumerated values, date ordering, arithmetic reconciliation, lifecycle transitions, and duplicate records.

### Deliverables

- CSV, JSON, and SQL seed data.
- Database schema and data dictionary.
- README with setup and generation instructions.
- Source manifest and validation summary.
- Reproducibility verification using the same seed.
- AI prompt documentation.

## 3. Acceptance Criteria

- Answers cite current, relevant sources.
- Ticket routing follows the defined rules.
- Unresolved or ambiguous cases are escalated.
- The article version used for an answer is recorded.

## 4. Data Provenance

Use lawful data sources where applicable. When source provenance is uncertain, use synthetic data.

