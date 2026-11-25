import os
import openai

CHECKS = []

if os.environ.get("OPENROUTER_API_KEY"):
    CHECKS.append(("openrouter", "https://openrouter.ai/api/v1",
                   os.environ["OPENROUTER_API_KEY"], "openrouter/free"))
if os.environ.get("GEMINI_API_KEY"):
    CHECKS.append(("gemini", "https://generativelanguage.googleapis.com/v1beta/openai/",
                   os.environ["GEMINI_API_KEY"], os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")))
if os.environ.get("OPENAI_API_KEY"):
    CHECKS.append(("openai", None,
                   os.environ["OPENAI_API_KEY"], os.environ.get("OPENAI_MODEL", "gpt-4.1-nano")))

if not CHECKS:
    raise SystemExit("No API keys set in this window.")

for name, base_url, key, model in CHECKS:
    try:
        client = openai.OpenAI(api_key=key, base_url=base_url) if base_url else openai.OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=50,
        )
        text = (resp.choices[0].message.content or "").strip()[:40]
        print(name, "works ->", repr(text), "| finish:", resp.choices[0].finish_reason)
    except Exception as e:
        print(name, "FAILED ->", type(e).__name__, str(e)[:120])
