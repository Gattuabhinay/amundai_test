"""daily_run.py: one safe command for a full test day.

python daily_run.py            -> official run (20 requests) + thread demo (9)
python daily_run.py ab thread  -> prompt A/B on one pinned model (16) + thread demo (9)
Order: keys and date -> budget check -> commit code -> run steps -> reports -> key scan -> commit and push.
"""
import csv
import glob
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

PY = sys.executable
DAILY_BUDGET = 30            # real free-tier budget; OpenRouter's limit is 50/day, retries eat the rest
LEDGER = "quota_ledger.csv"
THIS_FILE = os.path.basename(__file__)

AB_ENV = {"MORSE_AGENT": "sandbox-agent",
          "OPENROUTER_MODEL": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
          "ONLY_TESTS": "T04,T07,T08,T09,T10,T12,T18,T19"}

# (name, group, script, extra environment, planned requests)
STEPS = [
    ("official run", "official", "agent.py", {}, 20),
    ("thread demo", "thread", "thread_demo.py", {}, 9),
    ("prompt A/B v1", "ab", "agent.py", {**AB_ENV, "RUN_LABEL": "prompt-v1", "PROMPT_VERSION": "1"}, 8),
    ("prompt A/B v2", "ab", "agent.py", {**AB_ENV, "RUN_LABEL": "prompt-v2", "PROMPT_VERSION": "2"}, 8),
]
DEFAULT_GROUPS = {"official", "thread"}
CLEAR = ["MORSE_AGENT", "ONLY_TESTS", "RUN_LABEL", "MAX_TOKENS", "OPENROUTER_MODEL", "PROMPT_VERSION"]
# Built from pieces so this file does not match its own scan.
PATTERN = re.compile("sk" + "-or-|mh" + "q_|AI" + "za|sk" + "-proj")


def utc_today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def sh(cmd, check=True):
    print(">", " ".join(cmd))
    return subprocess.run(cmd, check=check)


def ledger_used():
    if not os.path.exists(LEDGER):
        return 0
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return sum(int(r["requests"]) for r in csv.DictReader(f) if r["date_utc"] == utc_today())


def ledger_add(step, n):
    new = not os.path.exists(LEDGER)
    with open(LEDGER, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date_utc", "step", "requests"])
        w.writerow([utc_today(), step, n])


def secrets_found():
    hits = []
    for path in glob.glob("**/*", recursive=True):
        if os.path.basename(path) == THIS_FILE or not os.path.isfile(path):
            continue
        if not path.lower().endswith((".py", ".csv", ".md", ".txt", ".json", ".ps1")):
            continue
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                if PATTERN.search(f.read()):
                    hits.append(path)
        except OSError:
            pass
    return hits


def coverage():
    if not os.path.exists("results.csv"):
        return
    with open("results.csv", newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("time_utc") or "").startswith(utc_today())]
    print(f"\nField coverage in results.csv today ({len(rows)} rows; thread demo is not in this file):")
    for field in ("customer_id", "git_revision", "prompt_version", "finish_reason", "model"):
        print(f"  {field:15} {sum(1 for r in rows if r.get(field))}/{len(rows)}")


def main():
    groups = set(sys.argv[1:]) or DEFAULT_GROUPS
    known = {s[1] for s in STEPS}
    if not groups <= known:
        sys.exit(f"Unknown group(s) {sorted(groups - known)}. Choose from {sorted(known)}.")
    steps = [s for s in STEPS if s[1] in groups]

    missing = [k for k in ("MORSE_API_KEY", "OPENROUTER_API_KEY") if not os.environ.get(k)]
    if missing:
        sys.exit("Set these in this window first: " + ", ".join(missing))
    print("UTC now:", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))

    try:
        manual = int(input("Requests you already sent today by hand (0 if none): ") or 0)
    except ValueError:
        sys.exit("Please enter a number.")
    used, planned = ledger_used() + manual, sum(s[4] for s in steps)
    print(f"Budget: used {used}, planned {planned}, limit {DAILY_BUDGET}")
    if used + planned > DAILY_BUDGET:
        sys.exit("Over budget. Wait for the UTC reset (05:30 AM IST) or choose fewer steps.")

    # Commit code first so the git revision attached to the runs matches the code that ran.
    if subprocess.run(["git", "status", "--porcelain", "--", "*.py"],
                      capture_output=True, text=True).stdout.strip():
        sh(["git", "add", "*.py"])
        sh(["git", "commit", "-m", f"Code update before run {utc_today()}"], check=False)

    env = {k: v for k, v in os.environ.items() if k not in CLEAR}
    for name, _group, script, extra, n in steps:
        print(f"\n=== {name} ({script}) ===")
        result = subprocess.run([PY, script], env={**env, **extra})
        ledger_add(name, n)  # failed attempts count against the quota too
        if result.returncode != 0:
            print(f"'{name}' stopped early. Not running further steps.")
            break

    coverage()
    sh([PY, "make_results_md.py"], check=False)
    sh([PY, "report_summary.py"], check=False)

    hits = secrets_found()
    if hits:
        sys.exit("STOP: possible key found in: " + ", ".join(hits) + ". Remove it and rotate that key.")
    sh(["git", "add", "."])
    sh(["git", "commit", "-m", f"Results for {utc_today()}"], check=False)
    sh(["git", "push"], check=False)

    print("\nNow screenshot: Setup (all cards), each agent's Capture health, Inbox, Cost > Segments,")
    print("Threads, Prompts. Then export the Traces JSON and send it to me.")


if __name__ == "__main__":
    main()