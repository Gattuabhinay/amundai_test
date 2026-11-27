# Test results

Generated 2026-11-27T05:58:47+00:00 UTC from: results.csv, results_before_v6.csv, results_before_v7_20261126_0921.csv, results_before_v8_20261126_1021.csv, results_nov24_old_format.csv, results_nov24_v1.csv, results_old.csv

**125 of 154 runs passed (81%)**

## By agent

| Group | Passed | Total | Rate |
|---|---|---|---|
| (older file) | 18 | 24 | 75% |
| customer-demo-agent | 9 | 10 | 90% |
| my-first-agent | 88 | 100 | 88% |
| sandbox-agent | 10 | 20 | 50% |

## By difficulty

| Group | Passed | Total | Rate |
|---|---|---|---|
| easy | 46 | 46 | 100% |
| hard | 27 | 53 | 50% |
| medium | 52 | 55 | 94% |

## By category

| Group | Passed | Total | Rate |
|---|---|---|---|
| constraints | 16 | 23 | 69% |
| counting | 21 | 21 | 100% |
| facts | 16 | 16 | 100% |
| format | 13 | 13 | 100% |
| json | 8 | 9 | 88% |
| logic | 5 | 5 | 100% |
| math | 29 | 29 | 100% |
| sorting | 6 | 8 | 75% |
| text | 11 | 30 | 36% |

## By model

| Group | Passed | Total | Rate |
|---|---|---|---|
| baidu/ernie-5.5-flash-preview:free | 17 | 18 | 94% |
| dots-studio/dots-3-note-preview:free | 2 | 2 | 100% |
| google/gemma-4-26b-a4b-it:free | 2 | 2 | 100% |
| inclusionai/ling-3.2-flash:free | 4 | 4 | 100% |
| liquid/lfm-3-1.7b:free | 10 | 14 | 71% |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 22 | 34 | 64% |
| nvidia/nemotron-3-ultra-550b-a55b:free | 11 | 12 | 91% |
| nvidia/nemotron-3.5-lightning:free | 7 | 12 | 58% |
| nvidia/nemotron-3.5-super-vl:free | 16 | 18 | 88% |
| particle-ai/particle-1:free | 16 | 16 | 100% |
| recursive/flint-v1.0:free | 18 | 22 | 81% |

## By finish reason

| Group | Passed | Total | Rate |
|---|---|---|---|
| (not logged) | 18 | 24 | 75% |
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
| 2026-11-23T10:23 | - | - | baidu/ernie-5.5-flash-preview:free | - | expected 'epocselet' in answer |
| 2026-11-23T10:23 | - | - | nvidia/nemotron-3.5-lightning:free | - | needs 8+ words and no letter 'e' |
