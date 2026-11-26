import csv
import statistics
from collections import defaultdict

rows = list(csv.DictReader(open("results.csv", newline="", encoding="utf-8")))
if not rows:
    raise SystemExit("results.csv is empty")


def passed(r):
    return str(r.get("passed")) == "True"


def table(title, key):
    groups = defaultdict(list)
    for r in rows:
        groups[key(r)].append(r)
    print(f"\n== {title} ==")
    for k, g in sorted(groups.items(), key=lambda kv: str(kv[0])):
        p = sum(1 for r in g if passed(r))
        print(f"  {str(k)[:55]:55} {p}/{len(g)}  ({100 * p // len(g)}%)")


print(f"Total runs: {len(rows)}, passed {sum(1 for r in rows if passed(r))}")
table("By agent / label", lambda r: (r.get("agent", "?"), r.get("run_label", "?")))
table("By customer (synthetic)", lambda r: r.get("customer_id") or "(none)")
table("By difficulty", lambda r: r.get("difficulty"))
table("By category", lambda r: r.get("category"))
table("By model", lambda r: r.get("model") or "(none)")
table("By finish reason", lambda r: r.get("finish_reason") or "(none)")

lat = [float(r["latency_s"]) for r in rows if r.get("latency_s")]
if lat:
    print(f"\nLatency: mean {statistics.mean(lat):.2f}s, median {statistics.median(lat):.2f}s, max {max(lat):.2f}s")

print("\n== Failures ==")
for r in rows:
    if not passed(r):
        print(" ", r.get("time_utc", "")[:16], r.get("agent", ""), r.get("test_id"), "|",
              r.get("model"), "|", r.get("finish_reason"), "|", r.get("reason"))