"""final_day.py: the last test day in one safe command.

python final_day.py                  -> official 20 + prompt A/B 12 + thread demo 9 (+ GitHub demo 1)
python final_day.py official thread -> only those groups
Add 'gemini' only after provider_check.py shows your Gemini key works (separate quota, optional).
"""
import csv
import glob
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

PY = sys.executable
DAILY_BUDGET = 44            # OpenRouter's free limit is 50/day; keep 6 spare for retries
LEDGER = "quota_ledger.csv"
THIS_FILE = os.path.basename(__file__)

AB_ENV = {"MORSE_AGENT": "sandbox-agent",
          "OPENROUTER_MODEL": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
          "ONLY_TESTS": "T04,T05,T09,T12,T18,T19"}
CLEAR = ["MORSE_AGENT", "ONLY_TESTS", "RUN_LABEL", "MAX_TOKENS", "OPENROUTER_MODEL", "PROMPT_VERSION"]
DEFAULT_GROUPS = ["official", "ab", "thread", "github"]
ALL_GROUPS = {"official", "ab", "thread", "github", "gemini"}
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


def build_steps(pr_key):
    steps = [
        {"name": "official run", "group": "official", "cmd": ["agent.py"], "env": {}, "n": 20},
        {"name": "prompt A/B v1", "group": "ab", "cmd": ["agent.py"],
         "env": {**AB_ENV, "RUN_LABEL": "prompt-v1", "PROMPT_VERSION": "1"}, "n": 6},
        {"name": "prompt A/B v2", "group": "ab", "cmd": ["agent.py"],
         "env": {**AB_ENV, "RUN_LABEL": "prompt-v2", "PROMPT_VERSION": "2"}, "n": 6},
        {"name": "thread demo", "group": "thread", "cmd": ["thread_demo.py"], "env": {}, "n": 9},
        {"name": "gemini run", "group": "gemini", "cmd": ["agent.py"],
         "env": {"MORSE_AGENT": "gemini-agent", "RUN_LABEL": "gemini", "OPENROUTER_API_KEY": None}, "n": 0},
    ]
    if pr_key:
        steps.append({"name": "github demo", "group": "github",
                      "cmd": ["github_demo.py", pr_key], "env": {}, "n": 1})
    return steps


def main():
    requested = sys.argv[1:] or DEFAULT_GROUPS
    if not set(requested) <= ALL_GROUPS:
        sys.exit(f"Unknown group(s) {sorted(set(requested) - ALL_GROUPS)}. Choose from {sorted(ALL_GROUPS)}.")

    missing = [] if os.environ.get("MORSE_API_KEY") else ["MORSE_API_KEY"]
    if any(g in requested for g in ("official", "ab", "thread", "github")) and not os.environ.get("OPENROUTER_API_KEY"):
        missing.append("OPENROUTER_API_KEY")
    if "gemini" in requested and not os.environ.get("GEMINI_API_KEY"):
        missing.append("GEMINI_API_KEY")
    if missing:
        sys.exit("Set these in this window first: " + ", ".join(missing))

    print("UTC now:", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"))
    if input("Is that the new UTC day you want, after the 05:30 AM IST reset? (y/n): ").strip().lower() != "y":
        sys.exit("Stopped. Wait for the reset and run again.")

    pr_key = ""
    if "github" in requested:
        pr_key = input('GitHub PR key like owner/repo#N (blank to skip the GitHub demo): ').strip()
        if pr_key and "#" not in pr_key:
            sys.exit("A PR key must look like owner/repo#number.")

    try:
        manual = int(input("Requests you already sent today by hand (0 if none): ") or 0)
    except ValueError:
        sys.exit("Please enter a number.")

    steps = [s for s in build_steps(pr_key) if s["group"] in requested]
    used, planned = ledger_used() + manual, sum(s["n"] for s in steps)
    print(f"Budget: used {used}, planned {planned}, limit {DAILY_BUDGET}")
    if used + planned > DAILY_BUDGET:
        sys.exit("Over budget. Choose fewer groups, e.g.: python final_day.py official thread")

    # Commit code first so the git revision attached to the runs matches the code that ran.
    if subprocess.run(["git", "status", "--porcelain", "--", "*.py"],
                      capture_output=True, text=True).stdout.strip():
        sh(["git", "add", "*.py"])
        sh(["git", "commit", "-m", f"Code update before final run {utc_today()}"], check=False)

    base_env = {k: v for k, v in os.environ.items() if k not in CLEAR}
    for s in steps:
        print(f"\n=== {s['name']} ({' '.join(s['cmd'])}) ===")
        env = dict(base_env)
        for k, v in s["env"].items():
            if v is None:
                env.pop(k, None)
            else:
                env[k] = v
        result = subprocess.run([PY] + s["cmd"], env=env)
        if s["group"] != "gemini":
            ledger_add(s["name"], s["n"])  # failed attempts count against the quota too
        if result.returncode != 0:
            print(f"'{s['name']}' stopped early. Not running further steps.")
            break

    coverage()
    for script in ("make_results_md.py", "report_summary.py", "lifetime_summary.py"):
        if os.path.exists(script):
            sh([PY, script], check=False)

    hits = secrets_found()
    if hits:
        sys.exit("STOP: possible key found in: " + ", ".join(hits) + ". Remove it and rotate that key.")
    sh(["git", "add", "."])
    sh(["git", "commit", "-m", f"Final day results {utc_today()}"], check=False)
    sh(["git", "push"], check=False)

    print("\nDone. Next: merge the pull request on GitHub, then Setup, Inbox, Threads, Prompts,")
    print("Cost > Segments and Settings > Outcomes screenshots. Export the Traces JSON.")


if __name__ == "__main__":
    main()