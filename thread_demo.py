import os
import time
from datetime import datetime, timezone

import openai
import morse_ai
from morse_ai.adapters.openai import wrap

morse_ai.init()

client = wrap(openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
))
MODEL = os.environ.get("OPENROUTER_MODEL", "openrouter/free")
AGENT = "thread-demo-agent"
DAY = datetime.now(timezone.utc).strftime("%Y%m%d")

CONVERSATIONS = [
    ["Name one fruit. Answer in one word.",
     "What colour is it usually? Answer in one word.",
     "Name a different fruit with the same colour. Answer in one word."],
    ["Pick a whole number between 1 and 10. Reply with only the number.",
     "Double that number. Reply with only the number.",
     "Is the result even or odd? Answer in one word."],
    ["Name one planet. Answer in one word.",
     "Is it bigger than Earth? Answer yes or no.",
     "Name a planet that is smaller than Earth. Answer in one word."],
]

for n, turns in enumerate(CONVERSATIONS, start=1):
    thread_id = f"demo-{DAY}-{n}"
    history = []
    for turn_no, user_text in enumerate(turns, start=1):
        history.append({"role": "user", "content": user_text})
        answer, finish = "", ""
        with morse_ai.run(AGENT, thread_id=thread_id,
                          user_metadata={"customer_id": "demo-shop", "turn": str(turn_no)}) as r:
            try:
                resp = client.chat.completions.create(model=MODEL, messages=history, max_tokens=200)
                answer = (resp.choices[0].message.content or "").strip()
                finish = resp.choices[0].finish_reason or ""
                ok = bool(answer) and finish == "stop"
            except Exception as e:
                ok = False
                print("error:", type(e).__name__)
            # A weak check on purpose: did the agent give a usable, complete reply?
            r.set_outcome(success=ok, outcome="responded" if ok else "no_usable_reply")
        history.append({"role": "assistant", "content": answer})
        print(thread_id, "turn", turn_no, "|", "ok" if ok else "FAIL", "|", finish or "-", "|", answer[:40])
        time.sleep(2)

morse_ai.flush()