
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

print("Agent:", AGENT, "| label:", RUN_LABEL, "| prompt v", PROMPT_VERSION, "| max_tokens:", MAX_TOKENS,
      "| tests:", len(SELECTED), "| git:", GIT_REV or "(none)")
print("Providers this run:", [(p["name"], p["model"]) for p in PROVIDERS])


def ask(prompt):
    """At most two passes over the providers. Fails over on rate limits or server trouble."""
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({"role": "user", "content": prompt})
    errors = []
    for attempt in range(2):
        for p in PROVIDERS:
            try:
                resp = p["client"].chat.completions.create(
                    model=p["model"],
                    messages=messages,
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
    customer_id = CUSTOMERS[int(test_id[1:]) % len(CUSTOMERS)]   # synthetic, deterministic
    with morse_ai.run(AGENT, record_keys={"test_case": test_id}) as r:
        morse_ai.set_prompt("answer-style", version=PROMPT_VERSION)
        morse_ai.set_context(test_id=test_id, category=t["category"], difficulty=t["difficulty"],
                             run_label=RUN_LABEL, max_tokens=str(MAX_TOKENS),
                             customer_id=customer_id)
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

        # Do not label provider/API errors as agent failures.
        if outcome != "api_error":
            r.set_outcome(success=ok, outcome=outcome)

    print("PASS" if ok else "FAIL", "|", test_id, "|", t["category"], "|", t["difficulty"], "|",
          customer_id, "|", model_used or "-", "|", latency, "s |", finish_reason or "-", "|", reason)
    rows.append({
        "time_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent": AGENT, "run_label": RUN_LABEL, "prompt_version": PROMPT_VERSION,
        "git_revision": GIT_REV, "customer_id": customer_id,
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