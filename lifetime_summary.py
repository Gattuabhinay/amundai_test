import csv
import glob
from collections import defaultdict

rows, seen = [], set()
for path in sorted(glob.glob("results*.csv")):
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r.get("time_utc") or r.get("time"), r.get("prompt"), r.get("model"), r.get("test_id"))
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)


def ok(r):
    return str(r.get("passed")) == "True"


logged = [r for r in rows if r.get("finish_reason")]
print(f"Unique rows: {len(rows)}   with finish_reason logged: {len(logged)}")
print(f"Overall: {sum(ok(r) for r in rows)}/{len(rows)} passed")
print(f"API errors: {sum(1 for r in rows if r.get('outcome') == 'api_error')}")

print("\nPassed by finish reason (rows where it was logged):")
by = defaultdict(lambda: [0, 0])
for r in logged:
    by[r["finish_reason"]][1] += 1
    by[r["finish_reason"]][0] += ok(r)
for k, (p, n) in sorted(by.items()):
    print(f"  {k:8} {p}/{n}")

fails = [r for r in logged if not ok(r)]
print(f"\nFailures with a logged finish reason: {len(fails)}")
print("  ended with length:", sum(1 for r in fails if r["finish_reason"] == "length"))
for r in fails:
    if r["finish_reason"] != "length":
        print("  NOT length:", r.get("time_utc"), r.get("test_id"), r.get("model"), r.get("reason"))

print("\nMost failed prompts:")
cnt = defaultdict(int)
for r in fails:
    cnt[(r.get("test_id"), (r.get("prompt") or "")[:55])] += 1
for (t, p), n in sorted(cnt.items(), key=lambda kv: -kv[1])[:6]:
    print(f"  {n:3} x {t} {p}")

print("\nBy model (logged rows):")
mod = defaultdict(lambda: [0, 0])
for r in logged:
    mod[r.get("model") or "-"][1] += 1
    mod[r.get("model") or "-"][0] += ok(r)
for k, (p, n) in sorted(mod.items(), key=lambda kv: -kv[1][1]):
    print(f"  {k[:52]:52} {p}/{n}")

print("\nBy UTC day:")
day = defaultdict(lambda: [0, 0])
for r in rows:
    d = (r.get("time_utc") or "")[:10]
    if d:
        day[d][1] += 1
        day[d][0] += ok(r)
for d, (p, n) in sorted(day.items()):
    print(f"  {d}  {p}/{n}  ({100 * p // n}%)")