import os
import sys

import openai
import morse_ai
from morse_ai.adapters.openai import wrap

PR_KEY = sys.argv[1] if len(sys.argv) > 1 else ""
if "#" not in PR_KEY:
    raise SystemExit('Usage: python github_demo.py "owner/repo#number"')

morse_ai.init()
client = wrap(openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
))

with morse_ai.run("github-demo-agent") as r:
    morse_ai.set_context(run_label="github-demo")
    morse_ai.link_record("github_pr", PR_KEY)
    resp = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": "In one sentence, what is a pull request?"}],
        max_tokens=150,
    )
    print("model:", resp.model, "| finish:", resp.choices[0].finish_reason)
    # No set_outcome on purpose: the GitHub connector should label this run when the PR merges.

morse_ai.flush()
print("sent run linked to", PR_KEY)