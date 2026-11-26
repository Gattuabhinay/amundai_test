# Test results

Generated 2026-11-26T04:19:44+00:00 UTC from: results.csv, results_before_v6.csv, results_before_v7_20261126_0921.csv, results_nov24_old_format.csv, results_nov24_v1.csv, results_old.csv

**96 of 126 runs passed (76%)**

## By agent

| Group | Passed | Total | Rate |
|---|---|---|---|
| (older file) | 26 | 36 | 72% |
| customer-demo-agent | 9 | 10 | 90% |
| my-first-agent | 51 | 60 | 85% |
| sandbox-agent | 10 | 20 | 50% |

## By difficulty

| Group | Passed | Total | Rate |
|---|---|---|---|
| easy | 38 | 38 | 100% |
| hard | 19 | 45 | 42% |
| medium | 39 | 43 | 90% |

## By category

| Group | Passed | Total | Rate |
|---|---|---|---|
| constraints | 11 | 20 | 55% |
| counting | 17 | 17 | 100% |
| facts | 13 | 13 | 100% |
| format | 10 | 10 | 100% |
| json | 7 | 8 | 87% |
| logic | 3 | 3 | 100% |
| math | 23 | 23 | 100% |
| sorting | 4 | 7 | 57% |
| text | 8 | 25 | 32% |

## By model

| Group | Passed | Total | Rate |
|---|---|---|---|
| baidu/ernie-5.5-flash-preview:free | 9 | 10 | 90% |
| dots-studio/dots-3-note-preview:free | 3 | 3 | 100% |
| google/gemma-4-26b-a4b-it:free | 2 | 2 | 100% |
| inclusionai/ling-3.2-flash:free | 5 | 5 | 100% |
| liquid/lfm-3-1.7b:free | 9 | 13 | 69% |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 17 | 28 | 60% |
| nvidia/nemotron-3-ultra-550b-a55b:free | 6 | 8 | 75% |
| nvidia/nemotron-3.5-lightning:free | 3 | 9 | 33% |
| nvidia/nemotron-3.5-super-vl:free | 13 | 15 | 86% |
| particle-ai/particle-1:free | 10 | 10 | 100% |
| recursive/flint-v1.0:free | 19 | 23 | 82% |

## By finish reason

| Group | Passed | Total | Rate |
|---|---|---|---|
| (not logged) | 26 | 36 | 72% |
| length | 0 | 20 | 0% |
| stop | 70 | 70 | 100% |

## Failures

| Time (UTC) | Agent | Test | Model | Finish | Reason |
|---|---|---|---|---|---|
| 2026-11-26T03:57 | my-first-agent | T07 | nvidia/nemotron-3.5-lightning:free | length | not valid JSON |
| 2026-11-26T03:58 | my-first-agent | T09 | liquid/lfm-3-1.7b:free | length | expected 'epocselet' in answer |
| 2026-11-26T03:58 | my-first-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-26T04:08 | customer-demo-agent | T08 | nvidia/nemotron-3.5-lightning:free | length | need 5 lines in alphabetical order |
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
