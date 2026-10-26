# Data dictionary

All names and messages are synthetic. IDs are stable strings and should not be changed after generation. Dates use ISO-8601; timestamps are naive ISO strings representing the synthetic university local time (documented anchor: 2026-10-26).

| Entity | Field | Type | Required | Allowed values / validation | Unique |
|---|---|---|---|---|---|
| Requester | requester_id | string | Yes | `REQ-` + six digits | PK |
| Requester | display_name | string | Yes | Synthetic display name | No |
| Requester | role_id | string | Yes | Must exist in Role | FK |
| Requester | email | string | Yes | `@example.edu`; synthetic only | Yes |
| Requester | department | string | Yes | Arts, Engineering, Science, Business, Student Services | No |
| Requester | active | boolean | Yes | true/false | No |
| Requester | created_at | timestamp | Yes | ISO timestamp | No |
| Role | role_id | string | Yes | `ROLE-` + 3 digits | PK |
| Role | role_name | string | Yes | learner, instructor, academic_administrator, support_staff, platform_administrator | Yes |
| Role | description | string | Yes | Human-readable role | No |
| Term | term_id | string | Yes | `TERM-` + 3 digits | PK |
| Term | term_name | string | Yes | Academic term label | Yes |
| Term | start_date/end_date | date | Yes | end >= start | No |
| Term | is_current | boolean | Yes | true/false | No |
| PolicyDocument | policy_id | string | Yes | `POL-<domain>-2026-###` | PK |
| PolicyDocument | domain | enum | Yes | financial_aid, registration, it, accessibility | No |
| PolicyDocument | title/version | string | Yes | Non-empty; version retained | No |
| PolicyDocument | effective_from/effective_to | date | Yes | end >= start; response date must fall within range for current citation | No |
| PolicyDocument | status | enum | Yes | published, draft, retired | No |
| PolicyDocument | source_url/license/retrieved_at | string/date | Yes | Placeholder URLs; provenance disclosed | No |
| KnowledgeArticle | article_id | string | Yes | `KB-` + 6 digits | PK |
| KnowledgeArticle | domain | enum | Yes | Four supported categories | No |
| KnowledgeArticle | title/body | string | Yes | Non-empty synthetic content | No |
| KnowledgeArticle | version | string | Yes | Version retained on citation | No |
| KnowledgeArticle | effective_from/effective_to | date | Yes | end >= start | No |
| KnowledgeArticle | status | enum | Yes | published, draft, retired | No |
| KnowledgeArticle | policy_id | string | Yes | Must exist in PolicyDocument | FK |
| KnowledgeArticle | updated_at | timestamp | Yes | ISO timestamp | No |
| Ticket | ticket_id | string | Yes | `TKT-2026-` + 6 digits | PK |
| Ticket | requester_id/term_id/category_id | string | Yes | Must exist in parent tables | FK |
| Ticket | subject/description | string | Yes | Non-empty synthetic text | No |
| Ticket | priority | enum | Yes | low, normal, high, urgent | No |
| Ticket | status | enum | Yes | open, in_progress, pending_requester, resolved, closed, escalated | No |
| Ticket | created_at/due_at | timestamp | Yes | due_at >= created_at | No |
| Ticket | ambiguous_flag/urgent_deadline_flag | boolean | Yes | Derived from generation rules | No |
| Ticket | closed_at | timestamp | Optional | Required for resolved/closed in production rules; empty in CSV means null | No |
| Ticket | issue_type | string | Yes | `none` or anomaly code | No |
| Message | message_id | string | Yes | `MSG-<ticket-id>-###` | PK |
| Message | ticket_id | string | Yes | Existing ticket | FK |
| Message | sequence_no | integer | Yes | Positive, unique per ticket | Composite unique |
| Message | sender_id/sender_type | string/enum | Yes | requester/support_staff in this baseline | No |
| Message | sent_at/body | timestamp/string | Yes | Sent after ticket creation; non-empty | No |
| Message | is_response | boolean | Yes | True/false | No |
| Message | response_supported | boolean/null | Optional | Response support label, not ground truth | No |
| Category | category_id | string | Yes | `CAT-` + 3 digits | PK |
| Category | category_code | enum | Yes | financial_aid, registration, it, accessibility | Yes |
| Category | display_name/default_team | string | Yes | Routing table determines default team | No |
| Category | active | boolean | Yes | true/false | No |
| Assignment | assignment_id | string | Yes | `ASN-######-###` | PK |
| Assignment | ticket_id | string | Yes | Existing ticket | FK |
| Assignment | team_name | string | Yes | Must be authorized for category in baseline | No |
| Assignment | assigned_at/ended_at | timestamp | Yes/Optional | Event chronology; blank ended_at means active | No |
| Assignment | assigned_by/is_authorized/reason | string/bool | Yes | Routing engine or labelled anomaly | No |
| SLA | sla_id | string | Yes | `SLA-<ticket-id>` | PK |
| SLA | ticket_id | string | Yes | Existing ticket, one baseline SLA per ticket | FK/unique |
| SLA | policy_name | string | Yes | Priority-based policy | No |
| SLA | target_business_hours | integer | Yes | Positive business hours | No |
| SLA | started_at/deadline_at | timestamp | Yes | Business-hours calendar, Mon-Fri 09:00-17:00 | No |
| SLA | paused_business_hours | numeric | Yes | >= 0 | No |
| SLA | breached | boolean | Yes | Derived from event/deadline data in production | No |
| SLA | clock_type | enum | Yes | business_hours or elapsed_hours (elapsed is an injected anomaly) | No |
| ResolutionFeedback | feedback_id | string | Yes | `FB-######` | PK |
| ResolutionFeedback | ticket_id | string | Yes | Existing resolved/closed ticket | FK |
| ResolutionFeedback | rating | integer | Yes | 1-5 | No |
| ResolutionFeedback | comment/submitted_at | string/timestamp | Yes | Synthetic feedback | No |

## Additional relationship/event tables

- `ticket_article_citations`: bridge table for Ticket ↔ KnowledgeArticle (N:M); stores the cited version and message reference.
- `ticket_events`: append-only lifecycle history; one Ticket has many events (1:N).
- `ground_truth`: evaluation-only labels, intentionally kept out of model/input features.
- `assignments`: one Ticket can have multiple assignment records over time (1:N); starter generator emits one per ticket.
- `slas`: one SLA per ticket in the baseline (1:1); schema can be extended to SLA history if policies change mid-ticket.
