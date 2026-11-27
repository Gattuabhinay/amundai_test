# Test results

Generated 2026-11-27T05:26:35+00:00 UTC from: results.csv, results_before_v6.csv, results_before_v7_20261126_0921.csv, results_before_v8_20261126_1021.csv, results_nov24_old_format.csv, results_nov24_v1.csv, results_old.csv

**133 of 166 runs passed (80%)**

## By agent

| Group | Passed | Total | Rate |
|---|---|---|---|
| (older file) | 26 | 36 | 72% |
| customer-demo-agent | 9 | 10 | 90% |
| my-first-agent | 88 | 100 | 88% |
| sandbox-agent | 10 | 20 | 50% |

## By difficulty

| Group | Passed | Total | Rate |
|---|---|---|---|
| easy | 50 | 50 | 100% |
| hard | 28 | 57 | 49% |
| medium | 55 | 59 | 93% |

## By category

| Group | Passed | Total | Rate |
|---|---|---|---|
| constraints | 17 | 26 | 65% |
| counting | 23 | 23 | 100% |
| facts | 17 | 17 | 100% |
| format | 14 | 14 | 100% |
| json | 9 | 10 | 90% |
| logic | 5 | 5 | 100% |
| math | 31 | 31 | 100% |
| sorting | 6 | 9 | 66% |
| text | 11 | 31 | 35% |

## By model

| Group | Passed | Total | Rate |
|---|---|---|---|
| baidu/ernie-5.5-flash-preview:free | 17 | 18 | 94% |
| dots-studio/dots-3-note-preview:free | 3 | 3 | 100% |
| google/gemma-4-26b-a4b-it:free | 2 | 2 | 100% |
| inclusionai/ling-3.2-flash:free | 5 | 5 | 100% |
| liquid/lfm-3-1.7b:free | 11 | 16 | 68% |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 22 | 34 | 64% |
| nvidia/nemotron-3-ultra-550b-a55b:free | 11 | 13 | 84% |
| nvidia/nemotron-3.5-lightning:free | 7 | 13 | 53% |
| nvidia/nemotron-3.5-super-vl:free | 17 | 19 | 89% |
| particle-ai/particle-1:free | 17 | 17 | 100% |
| recursive/flint-v1.0:free | 21 | 26 | 80% |

## By finish reason

| Group | Passed | Total | Rate |
|---|---|---|---|
| (not logged) | 26 | 36 | 72% |
| length | 0 | 23 | 0% |
| stop | 107 | 107 | 100% |

## Failures

| Time (UTC) | Agent | Test | Model | Finish | Reason |
|---|---|---|---|---|---|
| 2026-11-26T05:06 | my-first-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-26T05:07 | my-first-agent | T19 | liquid/lfm-3-1.7b:free | length | expected last number 3, got none |
| 2026-11-27T05:25 | my-first-agent | T09 | recursive/flint-v1.0:free | length | expected 'epocselet' in answer |
| 2026-11-24T08:01 | my-first-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-24T08:02 | my-first-agent | T10 | nvidia/nemotron-3.5-super-vl:free | length | expected 12 words, got 0 |
| 2026-11-24T08:02 | my-first-agent | T12 | nvidia/nemotron-3.5-super-vl:free | length | needs 8+ words and no letter 'e' |
| 2026-11-24T08:03 | my-first-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-25T09:30 | my-first-agent | T12 | nvidia/nemotron-3.5-lightning:free | length | needs 8+ words and no letter 'e' |
| 2026-11-25T09:30 | my-first-agent | T19 | liquid/lfm-3-1.7b:free | length | expected last number 3, got none |
| 2026-11-25T10:06 | sandbox-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-25T10:07 | sandbox-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-25T10:12 | sandbox-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-25T10:12 | sandbox-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-25T10:12 | sandbox-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-25T10:12 | sandbox-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-25T10:12 | sandbox-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-25T10:12 | sandbox-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-25T10:13 | sandbox-agent | T09 | recursive/flint-v1.0:free | length | expected 'epocselet' in answer |
| 2026-11-25T10:14 | sandbox-agent | T12 | recursive/flint-v1.0:free | length | needs 8+ words and no letter 'e' |
| 2026-11-26T03:57 | my-first-agent | T07 | nvidia/nemotron-3.5-lightning:free | length | not valid JSON |
| 2026-11-26T03:58 | my-first-agent | T09 | liquid/lfm-3-1.7b:free | length | expected 'epocselet' in answer |
| 2026-11-26T03:58 | my-first-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-26T04:08 | customer-demo-agent | T08 | nvidia/nemotron-3.5-lightning:free | length | need 5 lines in alphabetical order |
| 2026-11-24T13:03 | - | - | nvidia/nemotron-3.5-lightning:free | - | need 5 lines in alphabetical order |
| 2026-11-24T13:04 | - | - | liquid/lfm-3-1.7b:free | - | expected 'epocselet' in answer |
| 2026-11-24T13:04 | - | - | nvidia/nemotron-3-ultra-550b-a55b:free | - | expected 12 words, got 0 |
| 2026-11-24T13:04 | - | - | recursive/flint-v1.0:free | - | needs 8+ words and no letter 'e' |
| 2026-11-24T13:03 | - | - | nvidia/nemotron-3.5-lightning:free | - | need 5 lines in alphabetical order |
| 2026-11-24T13:04 | - | - | liquid/lfm-3-1.7b:free | - | expected 'epocselet' in answer |
| 2026-11-24T13:04 | - | - | nvidia/nemotron-3-ultra-550b-a55b:free | - | expected 12 words, got 0 |
| 2026-11-24T13:04 | - | - | recursive/flint-v1.0:free | - | needs 8+ words and no letter 'e' |
| 2026-11-23T10:23 | - | - | baidu/ernie-5.5-flash-preview:free | - | expected 'epocselet' in answer |
| 2026-11-23T10:23 | - | - | nvidia/nemotron-3.5-lightning:free | - | needs 8+ words and no letter 'e' |
