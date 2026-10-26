"""Generate twice and compare CSV SHA-256 checksums."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

def checksums(folder):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(folder).glob("*.csv"))}
if __name__=="__main__":
    for target in ("data/repro_a","data/repro_b"):
        shutil.rmtree(target,ignore_errors=True)
        subprocess.run([sys.executable,"src/generator.py","--outdir",target],check=True)
    a,b=checksums("data/repro_a"),checksums("data/repro_b")
    result={"identical":a==b,"checksums_run_a":a,"checksums_run_b":b}
    Path("reports/reproducibility.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({"identical":a==b,"files_compared":len(a)},indent=2))
    if a!=b: raise SystemExit(1)
