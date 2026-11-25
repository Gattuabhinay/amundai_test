\# Amund (formerly Morse) beta test



A small Python agent that sends 20 prompts to free OpenRouter models, checks each answer with a rule,

and reports pass or fail to Amund/Morse using the `morse-ai` SDK.



\## Files

\- `agent.py`: the test agent (20 tests, outcome checks, finish-reason logging)

\- `report\_summary.py`: summarizes `results.csv` by model, difficulty and finish reason

\- `provider\_check.py`: checks which API keys work

\- `results\*.csv`, `morse-traces-\*.json`: local logs and Morse exports



\## Run

Set `MORSE\_API\_KEY` and `OPENROUTER\_API\_KEY` as environment variables (never in files), then `python agent.py`.



\## Key findings

(fill in from the report)



\## Security

No API keys are stored in this repository.

