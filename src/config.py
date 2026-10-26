"""Project configuration."""
SEED = 20261022
YEAR = 2026
VOLUME = {
    "requesters": 1000,
    "terms": 4,
    "policy_documents": 50,
    "knowledge_articles": 200,
    "tickets": 5000,
    "messages": 20000,
}
CATEGORIES = ["financial_aid", "registration", "it", "accessibility"]
ROLES = ["learner", "instructor", "academic_administrator", "support_staff", "platform_administrator"]
TEAMS_BY_CATEGORY = {
    "financial_aid": ["Financial Aid Office", "Student Accounts"],
    "registration": ["Registrar", "Academic Advising"],
    "it": ["IT Service Desk", "Platform Operations"],
    "accessibility": ["Accessibility Services", "Student Support"],
}
PRIORITIES = ["low", "normal", "high", "urgent"]
STATUSES = ["open", "in_progress", "pending_requester", "resolved", "closed", "escalated"]
