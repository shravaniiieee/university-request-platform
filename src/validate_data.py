"""Data integrity checks and validation report."""
import json
from pathlib import Path
import pandas as pd

def validate(data_dir="data/generated"):
    d=Path(data_dir)
    load=lambda n: pd.read_csv(d/f"{n}.csv",keep_default_na=False)
    tables={n:load(n) for n in ["roles","requesters","terms","policy_documents","knowledge_articles","categories","tickets","messages","assignments","slas","resolution_feedback","ticket_article_citations","ticket_events","ground_truth"]}
    errors=[]; metrics={}
    pk={"roles":"role_id","requesters":"requester_id","terms":"term_id","policy_documents":"policy_id","knowledge_articles":"article_id","categories":"category_id","tickets":"ticket_id","messages":"message_id","assignments":"assignment_id","slas":"sla_id","resolution_feedback":"feedback_id","ticket_events":"event_id","ground_truth":"ground_truth_id"}
    for name,key in pk.items():
        dup=int(tables[name][key].duplicated().sum())
        metrics[f"{name}_duplicate_primary_keys"]=dup
        if dup: errors.append(f"{name}: {dup} duplicate primary keys")
    def fk(child,field,parent,parent_field):
        bad=~tables[child][field].isin(set(tables[parent][parent_field]))
        n=int(bad.sum()); metrics[f"fk_{child}_{field}_to_{parent}"]=int(n)
        if n: errors.append(f"{child}.{field}: {n} invalid foreign keys to {parent}.{parent_field}")
    fk("requesters","role_id","roles","role_id")
    fk("tickets","requester_id","requesters","requester_id")
    fk("tickets","term_id","terms","term_id")
    fk("tickets","category_id","categories","category_id")
    fk("knowledge_articles","policy_id","policy_documents","policy_id")
    fk("messages","ticket_id","tickets","ticket_id")
    fk("assignments","ticket_id","tickets","ticket_id")
    fk("slas","ticket_id","tickets","ticket_id")
    fk("resolution_feedback","ticket_id","tickets","ticket_id")
    fk("ticket_article_citations","ticket_id","tickets","ticket_id")
    fk("ticket_article_citations","article_id","knowledge_articles","article_id")
    fk("ticket_events","ticket_id","tickets","ticket_id")
    if len(tables["tickets"]) != 5000: metrics["ticket_count_warning"]=len(tables["tickets"])
    metrics["ticket_count"]=len(tables["tickets"]); metrics["article_count"]=len(tables["knowledge_articles"]); metrics["message_count"]=len(tables["messages"])
    metrics["ground_truth_count"]=len(tables["ground_truth"])
    metrics["ticket_category_distribution"]=tables["tickets"]["category_id"].value_counts().to_dict()
    metrics["status_distribution"]=tables["tickets"]["status"].value_counts().to_dict()
    metrics["priority_distribution"]=tables["tickets"]["priority"].value_counts().to_dict()
    # Enumerations and required fields
    allowed_priority={"low","normal","high","urgent"}
    bad_priority=int((~tables["tickets"]["priority"].isin(allowed_priority)).sum())
    metrics["invalid_priorities"]=bad_priority
    if bad_priority: errors.append(f"tickets: {bad_priority} invalid priorities")
    if tables["messages"]["message_id"].duplicated().any(): errors.append("messages: duplicate message IDs")
    metrics["error_count"]=len(errors)
    report={"passed":not errors,"errors":errors,"metrics":metrics}
    (Path("reports")).mkdir(exist_ok=True)
    Path("reports/validation_summary.json").write_text(json.dumps(report,indent=2,default=str))
    if errors:
        raise SystemExit(json.dumps(report,indent=2,default=str))
    print(json.dumps(report,indent=2,default=str))
    return report

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/generated")
    args=ap.parse_args()
    validate(args.data_dir)
