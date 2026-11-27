import csv
import glob
from collections import defaultdict
from datetime import datetime, timezone

files = sorted(glob.glob("results*.csv"))
rows, seen = [], set()
for f in files:
    with open(f, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r.get("time_utc") or r.get("time"), r.get("prompt"), r.get("model"), r.get("test_id"))
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)
def ok(r):
    return str(r.get("passed")) == "True"


def pct(p, n):
    return f"{100 * p // n}%" if n else "-"


out = ["# Test results", ""]
out.append(f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')} UTC from: {', '.join(files)}")
total = len(rows)
passed = sum(1 for r in rows if ok(r))
out += ["", f"**{passed} of {total} runs passed ({pct(passed, total)})**"]


def table(title, keyfn):
    groups = defaultdict(list)
    for r in rows:
        groups[keyfn(r)].append(r)
    out.extend(["", f"## {title}", "", "| Group | Passed | Total | Rate |", "|---|---|---|---|"])
    for k, g in sorted(groups.items(), key=lambda kv: str(kv[0])):
        p = sum(1 for r in g if ok(r))
        out.append(f"| {k} | {p} | {len(g)} | {pct(p, len(g))} |")


table("By agent", lambda r: r.get("agent") or "(older file)")
table("By difficulty", lambda r: r.get("difficulty") or "-")
table("By category", lambda r: r.get("category") or "-")
table("By model", lambda r: r.get("model") or "-")
table("By finish reason", lambda r: r.get("finish_reason") or "(not logged)")

out.extend(["", "## Failures", "", "| Time (UTC) | Agent | Test | Model | Finish | Reason |", "|---|---|---|---|---|---|"])
for r in rows:
    if not ok(r):
        t = (r.get("time_utc") or r.get("time") or "")[:16]
        cells = [t, r.get("agent") or "-", r.get("test_id") or "-", r.get("model") or "-",
                 r.get("finish_reason") or "-", (r.get("reason") or "-").replace("|", "/")]
        out.append("| " + " | ".join(cells) + " |")

with open("RESULTS.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("Wrote RESULTS.md")