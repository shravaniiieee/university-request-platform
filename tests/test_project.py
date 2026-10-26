from pathlib import Path
import pandas as pd
from src.generator import add_business_hours, generate
from datetime import datetime

def test_business_hours_skips_weekend():
    start=datetime(2026,10,23,16,0)  # Friday
    assert add_business_hours(start,2)==datetime(2026,10,26,10,0)

def test_small_generation_and_ids(tmp_path):
    out=tmp_path/"data"
    tables,truth=generate(str(out),seed=20261022,tickets_n=20,articles_n=12,messages_n=80,requesters_n=10,inject_anomalies=True)
    assert len(tables["tickets"])==20
    assert len(tables["knowledge_articles"])==12
    assert len(tables["messages"])==80
    assert tables["tickets"][0]["ticket_id"]=="TKT-2026-000001"
    assert tables["knowledge_articles"][0]["article_id"]=="KB-000001"
    assert len(truth)==5

def test_deterministic_generation(tmp_path):
    a=tmp_path/"a"; b=tmp_path/"b"
    generate(str(a),seed=20261022,tickets_n=20,articles_n=12,messages_n=80,requesters_n=10)
    generate(str(b),seed=20261022,tickets_n=20,articles_n=12,messages_n=80,requesters_n=10)
    assert (a/"tickets.csv").read_bytes()==(b/"tickets.csv").read_bytes()
    assert (a/"messages.csv").read_bytes()==(b/"messages.csv").read_bytes()
