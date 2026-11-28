"""patch_agent.py: applies the last fixes to agent.py without manual editing."""
import re
import sys

PATH = "agent.py"
src = open(PATH, encoding="utf-8").read()
if "def check_no_letter_e" not in src or "TESTS = [" not in src:
    sys.exit("agent.py looks damaged. Restore it first: git checkout 1fef4cb -- agent.py")

changes = []

# 1. import glob
if "import glob" not in src:
    src = src.replace("import csv\n", "import csv\nimport glob\n", 1)
    changes.append("added import glob")

# 2. quota guard reads every results*.csv file
NEW_GUARD = '''def openrouter_used_today():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used = 0
    for path in glob.glob("results*.csv"):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                when = row.get("time_utc") or row.get("time") or ""
                if row.get("provider", "openrouter") == "openrouter" and when.startswith(today):
                    used += 1
    return used
'''
if "glob.glob" not in src:
    src, n = re.subn(r"def openrouter_used_today\(\):.*?\n    return used\n",
                     lambda m: NEW_GUARD, src, count=1, flags=re.S)
    changes.append("replaced quota guard" if n else "!! quota guard NOT found")

# 3. the SDK must not retry silently
if "max_retries" not in src:
    src, n = re.subn(r'(\n([ \t]+)api_key=os\.environ\["(?:OPENROUTER|GEMINI)_API_KEY"\],)',
                     r"\1\n\2max_retries=0,", src)
    changes.append(f"set max_retries=0 on {n} client(s)")

# 4. provider errors are not agent failures: leave those runs unlabeled
if 'outcome != "api_error"' not in src:
    src, n = re.subn(
        r"\n([ \t]+)r\.set_outcome\(success=ok, outcome=outcome\)",
        lambda m: (f'\n{m.group(1)}if outcome != "api_error":  # provider problems are not agent failures'
                   f"\n{m.group(1)}    r.set_outcome(success=ok, outcome=outcome)"),
        src)
    changes.append(f"api_error runs left unlabeled ({n} place)")

# 5. send the stop reason to Amund, so truncation is visible there
if "stop_reason" not in src:
    src, n = re.subn(
        r'\n([ \t]+)finish_reason = resp\.choices\[0\]\.finish_reason or ""',
        lambda m: (f'\n{m.group(1)}finish_reason = resp.choices[0].finish_reason or ""'
                   f"\n{m.group(1)}morse_ai.set_context(stop_reason=finish_reason)"),
        src, count=1)
    changes.append(f"added stop_reason tag ({n} place)")

try:
    compile(src, PATH, "exec")
except SyntaxError as e:
    sys.exit(f"Patched file would not compile ({e}). Nothing written.")

open(PATH, "w", encoding="utf-8").write(src)
print("Patched agent.py:")
for c in changes:
    print("  -", c)
print("Now run: python -m py_compile agent.py")