# Test results

Generated 2026-11-28T04:53:14+00:00 UTC from: results.csv, results_before_v6.csv, results_before_v7_20261126_0921.csv, results_before_v8_20261126_1021.csv, results_nov24_old_format.csv, results_nov24_v1.csv, results_old.csv

**148 of 186 runs passed (79%)**

## By agent

| Group | Passed | Total | Rate |
|---|---|---|---|
| (older file) | 18 | 24 | 75% |
| customer-demo-agent | 9 | 10 | 90% |
| my-first-agent | 104 | 120 | 86% |
| sandbox-agent | 17 | 32 | 53% |

## By difficulty

| Group | Passed | Total | Rate |
|---|---|---|---|
| easy | 53 | 54 | 98% |
| hard | 33 | 67 | 49% |
| medium | 62 | 65 | 95% |

## By category

| Group | Passed | Total | Rate |
|---|---|---|---|
| constraints | 18 | 28 | 64% |
| counting | 23 | 24 | 95% |
| facts | 20 | 20 | 100% |
| format | 15 | 15 | 100% |
| json | 9 | 10 | 90% |
| logic | 6 | 6 | 100% |
| math | 35 | 35 | 100% |
| sorting | 7 | 9 | 77% |
| text | 15 | 39 | 38% |

## By model

| Group | Passed | Total | Rate |
|---|---|---|---|
| baidu/ernie-5.5-flash-preview:free | 20 | 21 | 95% |
| dots-studio/dots-3-note-preview:free | 2 | 2 | 100% |
| google/gemma-4-26b-a4b-it:free | 2 | 2 | 100% |
| inclusionai/ling-3.2-flash:free | 4 | 4 | 100% |
| liquid/lfm-3-1.7b:free | 13 | 18 | 72% |
| nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | 33 | 52 | 63% |
| nvidia/nemotron-3-ultra-550b-a55b:free | 12 | 13 | 92% |
| nvidia/nemotron-3.5-lightning:free | 9 | 15 | 60% |
| nvidia/nemotron-3.5-super-vl:free | 18 | 20 | 90% |
| particle-ai/particle-1:free | 16 | 16 | 100% |
| recursive/flint-v1.0:free | 19 | 23 | 82% |

## By finish reason

| Group | Passed | Total | Rate |
|---|---|---|---|
| (not logged) | 18 | 24 | 75% |
| length | 0 | 32 | 0% |
| stop | 130 | 130 | 100% |

## Failures

| Time (UTC) | Agent | Test | Model | Finish | Reason |
|---|---|---|---|---|---|
| 2026-11-26T05:06 | my-first-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-26T05:07 | my-first-agent | T19 | liquid/lfm-3-1.7b:free | length | expected last number 3, got none |
| 2026-11-27T05:25 | my-first-agent | T09 | recursive/flint-v1.0:free | length | expected 'epocselet' in answer |
| 2026-11-28T04:50 | my-first-agent | T01 | nvidia/nemotron-3.5-lightning:free | length | expected 7 lines, got 6 |
| 2026-11-28T04:50 | my-first-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-28T04:50 | my-first-agent | T12 | liquid/lfm-3-1.7b:free | length | needs 8+ words and no letter 'e' |
| 2026-11-28T04:51 | my-first-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-28T04:51 | sandbox-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-28T04:51 | sandbox-agent | T12 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | needs 8+ words and no letter 'e' |
| 2026-11-28T04:52 | sandbox-agent | T18 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'ananab' in answer |
| 2026-11-28T04:52 | sandbox-agent | T09 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | expected 'epocselet' in answer |
| 2026-11-28T04:52 | sandbox-agent | T12 | nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free | length | needs 8+ words and no letter 'e' |
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
