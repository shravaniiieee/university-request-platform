"""Deterministic synthetic dataset generator for a university request-management workflow."""
from __future__ import annotations
import argparse, hashlib, json, random
from datetime import date, datetime, timedelta, time
from pathlib import Path
import pandas as pd
try:
    from .config import SEED, YEAR, VOLUME, CATEGORIES, ROLES, TEAMS_BY_CATEGORY, PRIORITIES
except ImportError:  # Supports running as `python src/generator.py`
    from config import SEED, YEAR, VOLUME, CATEGORIES, ROLES, TEAMS_BY_CATEGORY, PRIORITIES

def dtstr(v):
    return v.isoformat(timespec="seconds") if isinstance(v, datetime) else v.isoformat() if isinstance(v, date) else v

def generate(outdir: str = "data/generated", seed: int = SEED, tickets_n: int = VOLUME["tickets"],
             articles_n: int = VOLUME["knowledge_articles"], messages_n: int = VOLUME["messages"],
             requesters_n: int = VOLUME["requesters"], inject_anomalies: bool = True):
    rng = random.Random(seed)
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    now = datetime(2026, 10, 26, 12, 0, 0)
    # 1) Master data first
    roles = [{"role_id": f"ROLE-{i+1:03d}", "role_name": name,
              "description": name.replace("_", " ").title()} for i, name in enumerate(ROLES)]
    requesters = []
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Riley", "Casey", "Sam", "Jamie", "Avery", "Cameron"]
    last_names = ["Patel", "Kim", "Singh", "Garcia", "Chen", "Brown", "Shah", "Khan", "Jones", "Wilson"]
    for i in range(1, requesters_n+1):
        role = rng.choice(ROLES)
        requesters.append({"requester_id": f"REQ-{i:06d}", "display_name": f"{rng.choice(first_names)} {rng.choice(last_names)}",
          "role_id": f"ROLE-{ROLES.index(role)+1:03d}", "email": f"requester{i:06d}@example.edu",
          "department": rng.choice(["Arts", "Engineering", "Science", "Business", "Student Services"]),
          "active": True, "created_at": dtstr(now-timedelta(days=rng.randint(30,900)))})
    terms = []
    for i, (name, start, end) in enumerate([
        ("2025-FALL", date(2025,8,25),date(2025,12,19)), ("2026-SPRING",date(2026,1,12),date(2026,5,15)),
        ("2026-SUMMER",date(2026,5,26),date(2026,8,7)), ("2026-FALL",date(2026,8,24),date(2026,12,18))],1):
        terms.append({"term_id":f"TERM-{i:03d}","term_name":name,"start_date":start.isoformat(),"end_date":end.isoformat(),"is_current":name=="2026-FALL"})
    policy_docs=[]
    domains=["financial_aid","registration","it","accessibility"]
    for i in range(1,51):
        domain=domains[(i-1)%len(domains)]
        effective=date(2025,1,1)+timedelta(days=(i%18)*30)
        expiry=effective+timedelta(days=365 if i%5 else 180)
        policy_docs.append({"policy_id":f"POL-{domain}-2026-{i:03d}","domain":domain,"title":f"{domain.replace('_',' ').title()} Policy {i:03d}",
          "version":f"{1+(i%3)}.{i%4}","effective_from":effective.isoformat(),"effective_to":expiry.isoformat(),
          "status":"published","source_url":f"https://example.edu/policies/{domain}/{i:03d}",
          "license":"Synthetic content; no external text copied","retrieved_at":"2026-10-26"})
    articles=[]
    for i in range(1,articles_n+1):
        domain=domains[(i-1)%len(domains)]
        policy=policy_docs[(i-1)%len(policy_docs)]
        effective=date(2025,1,1)+timedelta(days=(i%20)*25)
        expires=effective+timedelta(days=500 if i%7 else 250)
        articles.append({"article_id":f"KB-{i:06d}","domain":domain,"title":f"{domain.replace('_',' ').title()} Help Article {i:03d}",
          "version":f"{1+(i%3)}.{i%5}","effective_from":effective.isoformat(),"effective_to":expires.isoformat(),
          "status":"published","policy_id":policy["policy_id"],
          "body":f"Synthetic guidance for {domain.replace('_',' ')}. Verify eligibility, dates, and account-specific details with the responsible university team.",
          "updated_at":dtstr(now-timedelta(days=rng.randint(0,300)))})
    categories=[{"category_id":f"CAT-{i+1:03d}","category_code":c,"display_name":c.replace("_"," ").title(),
      "default_team":TEAMS_BY_CATEGORY[c][0],"active":True} for i,c in enumerate(CATEGORIES)]
    # 2) Dependent tickets and associated events
    tickets=[]; messages=[]; assignments=[]; slas=[]; feedback=[]; citations=[]; events=[]; truth=[]
    message_count=0
    anomaly_ticket_ids={}
    ticket_domain={}
    for i in range(1,tickets_n+1):
        tid=f"TKT-2026-{i:06d}"
        cat=rng.choice(CATEGORIES)
        requester=rng.choice(requesters)
        created=now-timedelta(days=rng.randint(0,300), hours=rng.randint(0,23), minutes=rng.randint(0,59))
        priority=rng.choices(PRIORITIES,weights=[15,55,23,7])[0]
        ambiguous=(i%17==0)
        urgent_deadline=(priority=="urgent" or i%29==0)
        status=rng.choices(["open","in_progress","pending_requester","resolved","closed","escalated"],weights=[8,18,10,38,18,8])[0]
        if ambiguous: status="escalated"
        team=TEAMS_BY_CATEGORY[cat][0]
        tickets.append({"ticket_id":tid,"requester_id":requester["requester_id"],"term_id":rng.choice(terms)["term_id"],
          "category_id":f"CAT-{CATEGORIES.index(cat)+1:03d}","subject":f"{cat.replace('_',' ').title()} request {i:05d}",
          "description": rng.choice([
             f"Please explain the current {cat.replace('_',' ')} policy and next steps.",
             f"I need help with a deadline related to {cat.replace('_',' ')}.",
             f"Can you confirm whether this rule applies to my situation?",
             f"I received conflicting information about {cat.replace('_',' ')}; please clarify."
          ]),"priority":priority,"status":status,"created_at":dtstr(created),
          "due_at":dtstr(created+timedelta(hours={"low":120,"normal":72,"high":24,"urgent":4}[priority])),
          "ambiguous_flag":ambiguous,"urgent_deadline_flag":urgent_deadline,"closed_at":dtstr(created+timedelta(hours=rng.randint(1,120))) if status in ("resolved","closed") else "",
          "issue_type":"none"})
        ticket_domain[tid]=cat
        # Each ticket has at least 2 and typically 4 messages; allocate near target total later
        count=4 if i <= messages_n//4 else max(2, min(4, messages_n - message_count - (tickets_n-i)*2))
        if message_count+count > messages_n: count=max(1,messages_n-message_count)
        for j in range(1,count+1):
            message_count+=1
            author=requester["requester_id"] if j%2==1 else "SYS-SUPPORT"
            is_response=(j%2==0)
            body=("Could you clarify the applicable deadline and eligibility?" if ambiguous and j==1 else
                  f"Synthetic {'support response' if is_response else 'requester message'} for {cat.replace('_',' ')} ticket.")
            messages.append({"message_id":f"MSG-{tid}-{j:03d}","ticket_id":tid,"sequence_no":j,
              "sender_id":author,"sender_type":"requester" if j%2 else "support_staff","sent_at":dtstr(created+timedelta(minutes=10*j)),
              "body":body,"is_response":is_response,"response_supported":True if is_response else None})
        # Valid baseline routing, then anomaly injection can override one assignment
        assigned_team=team
        assignments.append({"assignment_id":f"ASN-{i:06d}-001","ticket_id":tid,"team_name":assigned_team,
          "assigned_at":dtstr(created+timedelta(minutes=5)),"assigned_by":"ROUTING-RULE-ENGINE","is_authorized":True,
          "ended_at":"","assignment_reason":"category_default"})
        # SLA business-hours (Mon-Fri 09:00-17:00); target hours by priority
        target={"low":40,"normal":24,"high":8,"urgent":2}[priority]
        slas.append({"sla_id":f"SLA-{tid}","ticket_id":tid,"policy_name":f"{priority.upper()}_FIRST_RESPONSE",
          "target_business_hours":target,"started_at":dtstr(created),"deadline_at":dtstr(add_business_hours(created,target)),
          "paused_business_hours":0,"breached":False,"clock_type":"business_hours"})
        # Link at least one article in baseline; choose matching domain and currently effective at response time
        eligible=[a for a in articles if a["domain"]==cat and a["effective_from"]<=created.date().isoformat()<=a["effective_to"]]
        article=rng.choice(eligible if eligible else [a for a in articles if a["domain"]==cat])
        citations.append({"ticket_id":tid,"article_id":article["article_id"],"article_version":article["version"],
          "message_id":f"MSG-{tid}-002" if count>=2 else f"MSG-{tid}-001","citation_role":"primary","is_current_at_response":True})
        events.append({"event_id":f"EVT-{i:06d}-001","ticket_id":tid,"event_type":"ticket_created","from_state":"","to_state":"open","event_at":dtstr(created),"actor":"SYSTEM","details":"Ticket created"})
        if status!="open":
            events.append({"event_id":f"EVT-{i:06d}-002","ticket_id":tid,"event_type":"status_changed","from_state":"open","to_state":status,"event_at":dtstr(created+timedelta(minutes=20)),"actor":"SYSTEM","details":"Synthetic lifecycle transition"})
        if status in ("resolved","closed") and rng.random()<0.72:
            feedback.append({"feedback_id":f"FB-{i:06d}","ticket_id":tid,"rating":rng.randint(1,5),"comment":"Synthetic feedback","submitted_at":dtstr(created+timedelta(days=2))})
    # Ensure exact message target, adding messages round-robin if needed
    while message_count < messages_n:
        t=tickets[(message_count-tickets_n*2) % len(tickets)]
        tid=t["ticket_id"]; existing=sum(1 for m in messages if m["ticket_id"]==tid)
        message_count+=1
        messages.append({"message_id":f"MSG-{tid}-{existing+1:03d}","ticket_id":tid,"sequence_no":existing+1,
          "sender_id":"SYS-SUPPORT","sender_type":"support_staff","sent_at":dtstr(datetime.fromisoformat(t["created_at"])+timedelta(minutes=10*(existing+1))),
          "body":"Synthetic follow-up message.","is_response":True,"response_supported":True})
    # 3) Labelled anomaly cases. Preserve labels in separate ground truth.
    if inject_anomalies and tickets_n >= 10 and articles_n >= 2:
        cases=[
          (1,"expired_policy_citation","Answer cites expired policy","citation"),
          (2,"unauthorized_team_routing","Ticket routed to unauthorized team","assignment"),
          (3,"unsupported_answer_claim","Response claims unsupported fact","message"),
          (4,"business_hours_sla_error","SLA clock ignores business hours","sla"),
          (5,"escalation_not_triggered","Escalation not triggered","escalation"),
        ]
        for idx, issue, desc, entity in cases:
            t=tickets[idx-1]; tid=t["ticket_id"]; t["issue_type"]=issue
            if entity=="citation":
                old=articles[0].copy(); old["effective_to"]="2025-01-01"
                # Keep article master intact; label citation as stale via the bridge row.
                citations[idx-1]["article_id"]=old["article_id"]
                citations[idx-1]["article_version"]=old["version"]
                citations[idx-1]["is_current_at_response"]=False
            elif entity=="assignment":
                assignments[idx-1]["team_name"]="Unauthorized Executive Office"
                assignments[idx-1]["is_authorized"]=False
            elif entity=="message":
                for m in messages:
                    if m["ticket_id"]==tid and m["is_response"]:
                        m["body"]="Your grant is guaranteed regardless of eligibility." 
                        m["response_supported"]=False
                        break
            elif entity=="sla":
                slas[idx-1]["clock_type"]="elapsed_hours"
                slas[idx-1]["deadline_at"]=dtstr(datetime.fromisoformat(t["created_at"])+timedelta(hours=slas[idx-1]["target_business_hours"]))
            elif entity=="escalation":
                t["status"]="in_progress"
                t["ambiguous_flag"]=True
                # intentionally no escalation event; assignment remains default
            truth.append({"ground_truth_id":f"GT-{len(truth)+1:03d}","ticket_id":tid,"issue_type":issue,
              "entity_type":entity,"expected_label":"anomaly","expected_decision":desc,
              "detection_rule": {
                "citation":"Citation article must be effective on response date.",
                "assignment":"Assigned team must be authorized for category.",
                "message":"Response claims must be supported by cited policy/article.",
                "sla":"SLA clock must use business-hours calendar.",
                "escalation":"Ambiguous or unresolved cases must escalate."
              }[entity],"severity":"high"})
    tables={
      "roles":roles,"requesters":requesters,"terms":terms,"policy_documents":policy_docs,
      "knowledge_articles":articles,"categories":categories,"tickets":tickets,"messages":messages,
      "assignments":assignments,"slas":slas,"resolution_feedback":feedback,
      "ticket_article_citations":citations,"ticket_events":events
    }
    for name, rows in tables.items():
        pd.DataFrame(rows).to_csv(out/f"{name}.csv",index=False)
        pd.DataFrame(rows).to_json(out/f"{name}.json",orient="records",indent=2,date_format="iso")
    pd.DataFrame(truth).to_csv(out/"ground_truth.csv",index=False)
    pd.DataFrame(truth).to_json(out/"ground_truth.json",orient="records",indent=2)
    manifest={"seed":seed,"generated_at":"2026-10-26T12:00:00","synthetic_only":True,"source_note":"All records are synthetic; example.edu URLs are placeholders, not retrieved policy content.",
      "volumes":{k:len(v) for k,v in tables.items()},"ground_truth_rows":len(truth)}
    (out/"source_manifest.json").write_text(json.dumps(manifest,indent=2))
    return tables, truth

def add_business_hours(start: datetime, hours: int) -> datetime:
    """Add business hours using Monday-Friday 09:00-17:00; excludes weekends."""
    cur=start
    remaining=float(hours)
    while remaining>0:
        if cur.weekday()>=5:
            cur=(cur+timedelta(days=1)).replace(hour=9,minute=0,second=0,microsecond=0); continue
        if cur.hour<9:
            cur=cur.replace(hour=9,minute=0,second=0,microsecond=0)
        if cur.hour>=17:
            cur=(cur+timedelta(days=1)).replace(hour=9,minute=0,second=0,microsecond=0); continue
        available=(datetime.combine(cur.date(),time(17,0))-cur).total_seconds()/3600
        take=min(remaining,available)
        cur+=timedelta(hours=take); remaining-=take
        if remaining>0:
            cur=(cur+timedelta(days=1)).replace(hour=9,minute=0,second=0,microsecond=0)
    return cur

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",default="data/generated")
    ap.add_argument("--seed",type=int,default=SEED)
    ap.add_argument("--tickets",type=int,default=VOLUME["tickets"])
    ap.add_argument("--articles",type=int,default=VOLUME["knowledge_articles"])
    ap.add_argument("--messages",type=int,default=VOLUME["messages"])
    ap.add_argument("--requesters",type=int,default=VOLUME["requesters"])
    ap.add_argument("--no-anomalies",action="store_true")
    args=ap.parse_args()
    tables,truth=generate(args.outdir,args.seed,args.tickets,args.articles,args.messages,args.requesters,not args.no_anomalies)
    print(json.dumps({"rows":{k:len(v) for k,v in tables.items()},"ground_truth":len(truth),"seed":args.seed},indent=2))
