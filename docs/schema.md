# Schema and cardinality

- Role 1:N Requester; each requester has one role.
- Requester 1:N Ticket; each ticket has one requester.
- Term 1:N Ticket; each ticket belongs to one term.
- Category 1:N Ticket; each ticket has one primary category.
- PolicyDocument 1:N KnowledgeArticle; each article references one policy document.
- Ticket 1:N Message, Assignment, TicketEvent; these are history/event records.
- Ticket 1:1 SLA in the baseline; SLA ID is `SLA-<ticket-id>`.
- Ticket 1:N ResolutionFeedback is supported by the relational model, though baseline generates at most one response per ticket.
- Ticket N:M KnowledgeArticle through `ticket_article_citations`; citation row stores the exact article version and response message.
- Ground truth is separate from generated operational features and must only be used for evaluation.

Effective dates are inclusive: `effective_from <= response_date <= effective_to`. Synthetic timestamps are generated against a fixed reference time so reruns are reproducible.
