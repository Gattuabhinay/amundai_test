import csv
import json
import os
import re
import time
from datetime import datetime, timezone

import openai
import morse_ai
from morse_ai.adapters.openai import wrap

morse_ai.init()

# ---------- settings (all overridable from the terminal) ----------
AGENT = os.environ.get("MORSE_AGENT", "my-first-agent")      # use "sandbox-agent" for experiments
RUN_LABEL = os.environ.get("RUN_LABEL", "official")          # tags each run in Morse and the CSV
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "400"))
ONLY = {x.strip().upper() for x in os.environ.get("ONLY_TESTS", "").split(",") if x.strip()}
RESULTS_FILE = "results.csv"
OPENROUTER_DAILY_BUDGET = 40  # free tier allows 50/day; keep a safety margin

# ---------- providers, tried in order ----------
PROVIDERS = []

if os.environ.get("OPENROUTER_API_KEY"):
    PROVIDERS.append({
        "name": "openrouter",
        # Set OPENROUTER_MODEL to pin one model. If unset, the random free router is used.
        "model": os.environ.get("OPENROUTER_MODEL", "openrouter/free"),
        "client": wrap(openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )),
        "extra": {},
    })

if os.environ.get("GEMINI_API_KEY"):
    PROVIDERS.append({
        "name": "gemini",
        "model": os.environ.get("GEMINI_MODEL", "gemini-3.8-flash"),
        "client": wrap(openai.OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=os.environ["GEMINI_API_KEY"],
        )),
        "extra": {"reasoning_effort": "low"},
    })


# ---------- checks: each returns (passed, reason) ----------

def lines_of(text):
    return [l.strip() for l in text.splitlines() if l.strip()]


def check_lines(n):
    def check(text):
        got = len(lines_of(text))
        return got == n, f"expected {n} lines, got {got}"
    return check


def check_exact_word(word):
    def check(text):
        cleaned = re.sub(r"[^a-z]", "", text.lower())
        return cleaned == word, f"expected only '{word}'"
    return check


def check_last_number(n):
    def check(text):
        nums = re.findall(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
        return bool(nums) and nums[-1] == str(n), f"expected last number {n}, got {nums[-1:] or 'none'}"
    return check


def check_contains(value):
    def check(text):
        return value in text.lower(), f"expected '{value}' in answer"
    return check


def check_word_count(n):
    def check(text):
        got = len(text.split())
        return got == n, f"expected {n} words, got {got}"
    return check


def check_json_keys(keys):
    def check(text):
        cleaned = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
        try:
            data = json.loads(cleaned)
        except Exception:
            return False, "not valid JSON"
        ok = isinstance(data, dict) and all(k in data for k in keys)
        return ok, f"JSON missing keys {keys}"
    return check


def check_no_letter_e(text):
    words = len(text.split())
    ok = words >= 8 and "e" not in text.lower()
    return ok, "needs 8+ words and no letter 'e'"


def check_palindromes(text):
    ls = [l.lower() for l in lines_of(text)]
    ok = len(ls) == 3 and all(len(l) > 2 and l == l[::-1] for l in ls)
    return ok, "need 3 palindromes, one per line"


def check_alphabetical(text):
    ls = [l.lower() for l in lines_of(text)]
    ok = len(ls) == 5 and ls == sorted(ls)
    return ok, "need 5 lines in alphabetical order"


def check_hello_caps(text):
    cleaned = text.strip().strip(".!\"'")
    return cleaned == "HELLO", "expected HELLO"


# ---------- test suite (20 tests) ----------

TESTS = [
    {"category": "counting", "difficulty": "easy",
     "prompt": "List exactly seven animals, one per line, no numbering.",
     "check": check_lines(7)},
    {"category": "counting", "difficulty": "easy",
     "prompt": "Name four rivers, one per line, no extra text.",
     "check": check_lines(4)},
    {"category": "format", "difficulty": "easy",
     "prompt": "Write the word yes and nothing else.",
     "check": check_exact_word("yes")},
    {"category": "facts", "difficulty": "easy",
     "prompt": "What is the capital of Australia? Answer with one word only.",
     "check": check_contains("canberra")},
    {"category": "math", "difficulty": "medium",
     "prompt": "What is 17 times 23? Reply with only the number.",
     "check": check_last_number(391)},
    {"category": "math", "difficulty": "medium",
     "prompt": "What is 15 percent of 240? Reply with only the number.",
     "check": check_last_number(36)},
    {"category": "json", "difficulty": "medium",
     "prompt": "Return only valid JSON with keys name and age for a fictional person. No other text.",
     "check": check_json_keys(["name", "age"])},
    {"category": "sorting", "difficulty": "medium",
     "prompt": "List five fruits in alphabetical order, one per line, no numbering.",
     "check": check_alphabetical},
    {"category": "text", "difficulty": "hard",
     "prompt": "Reverse the word telescope. Output only the reversed word.",
     "check": check_contains("epocselet")},
    {"category": "constraints", "difficulty": "hard",
     "prompt": "Describe the ocean in exactly 12 words. Output only the sentence.",
     "check": check_word_count(12)},
    {"category": "constraints", "difficulty": "hard",
     "prompt": "Give three palindromic words, one per line, no extra text.",
     "check": check_palindromes},
    {"category": "constraints", "difficulty": "hard",
     "prompt": "Write one sentence of at least 8 words without using the letter e.",
     "check": check_no_letter_e},
    {"category": "math", "difficulty": "easy",
     "prompt": "What is 144 divided by 12? Reply with only the number.",
     "check": check_last_number(12)},
    {"category": "math", "difficulty": "medium",
     "prompt": "Convert 3.5 hours to minutes. Reply with only the number.",
     "check": check_last_number(210)},
    {"category": "facts", "difficulty": "easy",
     "prompt": "Which is the largest planet in our solar system? Answer with one word only.",
     "check": check_contains("jupiter")},
    {"category": "format", "difficulty": "medium",
     "prompt": "Write the word hello in capital letters and nothing else.",
     "check": check_hello_caps},
    {"category": "counting", "difficulty": "medium",
     "prompt": "Write the numbers 1 to 5, one per line, nothing else.",
     "check": check_lines(5)},
    {"category": "text", "difficulty": "hard",
     "prompt": "Spell the word banana backwards. Output only the result.",
     "check": check_contains("ananab")},
    {"category": "text", "difficulty": "hard",
     "prompt": "How many times does the letter r appear in the word strawberry? Reply with only the number.",
     "check": check_last_number(3)},
    {"category": "logic", "difficulty": "medium",
     "prompt": "Is 97 a prime number? Answer yes or no only.",
     "check": check_exact_word("yes")},
]

ALL_TESTS = [(f"T{i:02d}", t) for i, t in enumerate(TESTS, start=1)]
unknown = ONLY - {tid for tid, _ in ALL_TESTS}
if unknown:
    raise SystemExit(f"Unknown test IDs in ONLY_TESTS: {sorted(unknown)}")
SELECTED = [(tid, t) for tid, t in ALL_TESTS if not ONLY or tid in ONLY]

FIELDS = ["time_utc", "agent", "run_label", "test_id", "category", "difficulty", "provider", "model",
          "max_tokens", "prompt", "passed", "outcome", "latency_s", "finish_reason", "reason",
          "answer_preview"]


# ---------- quota guard (approximate: counts today's logged OpenRouter requests) ----------

def openrouter_used_today():
    if not os.path.exists(RESULTS_FILE):
        return 0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used = 0
    with open(RESULTS_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("provider") == "openrouter" and row.get("time_utc", "").startswith(today):
                used += 1
    return used


used = openrouter_used_today()
if used + len(SELECTED) > OPENROUTER_DAILY_BUDGET:
    print(f"OpenRouter budget reached ({used} logged today, {len(SELECTED)} planned). Skipping OpenRouter.")
    PROVIDERS = [p for p in PROVIDERS if p["name"] != "openrouter"]

if not PROVIDERS:
    raise SystemExit("No provider available. Set OPENROUTER_API_KEY and/or GEMINI_API_KEY.")

print("Agent:", AGENT, "| label:", RUN_LABEL, "| max_tokens:", MAX_TOKENS, "| tests:", len(SELECTED))
print("Providers this run:", [(p["name"], p["model"]) for p in PROVIDERS])


def ask(prompt):
    """At most two passes over the providers. Fails over on rate limits or server trouble."""
    errors = []
    for attempt in range(2):
        for p in PROVIDERS:
            try:
                resp = p["client"].chat.completions.create(
                    model=p["model"],
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=MAX_TOKENS,
                    **p["extra"],
                )
                return resp, p["name"]
            except (openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError) as e:
                errors.append(f'{p["name"]}:{type(e).__name__}')
        if attempt == 0:
            time.sleep(20)
    raise RuntimeError("all providers failed: " + ", ".join(errors))


rows = []

for test_id, t in SELECTED:
    with morse_ai.run(AGENT) as r:
        morse_ai.set_context(test_id=test_id, category=t["category"], difficulty=t["difficulty"],
                             run_label=RUN_LABEL, max_tokens=str(MAX_TOKENS))
        start = time.time()
        provider = model_used = finish_reason = answer = ""
        try:
            resp, provider = ask(t["prompt"])
            model_used = getattr(resp, "model", "") or ""
            morse_ai.set_context(provider=provider, served_model=model_used)
            finish_reason = resp.choices[0].finish_reason or ""
            answer = resp.choices[0].message.content or ""
            ok, reason = t["check"](answer)
            outcome = "passed" if ok else "failed_check"
            if not ok and finish_reason == "length":
                outcome = "truncated"
            if ok:
                reason = ""
        except Exception as e:
            ok, outcome = False, "api_error"
            reason = f"api error: {type(e).__name__}: {str(e)[:100]}"
        latency = round(time.time() - start, 2)
        r.set_outcome(success=ok, outcome=outcome)

    print("PASS" if ok else "FAIL", "|", test_id, "|", t["category"], "|", t["difficulty"], "|",
          model_used or "-", "|", latency, "s |", finish_reason or "-", "|", reason)
    rows.append({
        "time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent": AGENT, "run_label": RUN_LABEL,
        "test_id": test_id, "category": t["category"], "difficulty": t["difficulty"],
        "provider": provider, "model": model_used, "max_tokens": MAX_TOKENS,
        "prompt": t["prompt"], "passed": ok, "outcome": outcome, "latency_s": latency,
        "finish_reason": finish_reason, "reason": reason,
        "answer_preview": answer.replace("\n", " | ")[:300],
    })
    time.sleep(2)

morse_ai.flush()

# ---------- local ground truth for your report ----------
new_file = not os.path.exists(RESULTS_FILE)
with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    if new_file:
        w.writeheader()
    w.writerows(rows)

passed = sum(1 for row in rows if row["passed"])
print(f"\nPassed {passed}/{len(rows)}. Saved to {RESULTS_FILE}")
for level in ("easy", "medium", "hard"):
    group = [row for row in rows if row["difficulty"] == level]
    if group:
        print(f"  {level}: {sum(1 for row in group if row['passed'])}/{len(group)}")
print("  truncated (finish=length):", sum(1 for row in rows if row["finish_reason"] == "length"))