# V16 save step: merges this run's PUBLIC files with anything changed on GitHub meanwhile, then pushes.
# Saves only jobs.json, README.md and outbox/ (encrypted). Never force-pushes. Keeps your own edits.
import json, os, shutil, subprocess, sys, time
from pathlib import Path
BR = os.environ.get("GITHUB_REF_NAME", "main")
TMP = Path(os.environ.get("RUNNER_TEMP", ".")) / "v16-save"
MANAGED = ["jobs.json", "README.md", "outbox"]
def git(*a): return subprocess.run(["git", *a], capture_output=True, text=True)
if not Path("jobs.json").exists(): print("Nothing to save."); sys.exit(0)
git("config", "user.name", "job-agent"); git("config", "user.email", "job-agent@users.noreply.github.com")
shutil.rmtree(TMP, ignore_errors=True); TMP.mkdir(parents=True)
for p in MANAGED:
    if Path(p).exists(): (shutil.copytree if Path(p).is_dir() else shutil.copy2)(p, TMP / p)
deleted = {f for f in git("ls-tree", "-r", "--name-only", "HEAD", "--", "outbox").stdout.split() if not Path(f).exists()}
k = lambda j: (j.get("link", "") + "|" + j.get("title", "")).lower()
hb = git("show", "HEAD:jobs.json")
try: BASE = {k(j): j for j in json.loads(hb.stdout).get("jobs", [])} if hb.returncode == 0 else {}
except Exception: BASE = {}
def merge(mine, theirs):
    if not theirs: return mine
    have = {k(j): j for j in mine["jobs"]}
    for o in theirs.get("jobs", []):
        b = BASE.get(k(o))
        if b == o: continue
        if k(o) not in have:
            if b is None: mine["jobs"].append(o)
            continue
        if o.get("status") == "removed": have[k(o)]["status"] = "removed"
    for n, s in theirs.get("meta", {}).get("sources", {}).items():
        m = mine["meta"].setdefault("sources", {}).setdefault(n, s)
        if s.get("last_ok", "") > m.get("last_ok", ""): m["last_ok"] = s["last_ok"]
    return mine
for attempt in range(1, 4):
    git("fetch", "--quiet", "origin", BR)
    th = git("show", f"origin/{BR}:jobs.json")
    try: theirs = json.loads(th.stdout) if th.returncode == 0 else None
    except Exception: theirs = None
    mine = merge(json.loads((TMP / "jobs.json").read_text(encoding="utf-8")), theirs)
    git("reset", "--quiet", "--hard", f"origin/{BR}")
    Path("jobs.json").write_text(json.dumps(mine, ensure_ascii=False, indent=1), encoding="utf-8")
    if (TMP / "README.md").exists(): shutil.copy2(TMP / "README.md", "README.md")
    if (TMP / "outbox").is_dir(): shutil.copytree(TMP / "outbox", "outbox", dirs_exist_ok=True)
    for f in deleted:
        if Path(f).exists(): Path(f).unlink()
    git("add", "-A", "--", *[p for p in MANAGED if Path(p).exists() or git("ls-files", p).stdout])
    if git("diff", "--cached", "--quiet").returncode == 0: print("Nothing changed."); sys.exit(0)
    git("commit", "--quiet", "-m", "agent update")
    if git("push", "--quiet", "origin", f"HEAD:{BR}").returncode == 0: print(f"Saved (attempt {attempt})."); sys.exit(0)
    time.sleep(5 * attempt)
print("Could not save after 3 tries."); sys.exit(1)
