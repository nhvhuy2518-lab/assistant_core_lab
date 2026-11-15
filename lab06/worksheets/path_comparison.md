# Lab 6 — Three assistant paths

Evaluation results from `python eval/compare_paths.py` (25 cases; 7 expected abstentions).

| Path | Correct /25 | Abstain correct /7 | p50 latency | Controllability (1–5) | Main failure mode |
|---|---:|---:|---:|---:|---|
| deterministic | 9/25 | 7/7 | 0.0 ms | 5 | Limited coverage: predefined routing and tools do not answer many policy questions that require knowledge-base lookup. |
| retrieval | 25/25 | 7/7 | 0.1 ms | 4 | BM25 is lexical; paraphrases can be missed without query expansion, and synonym rules/coverage thresholds require careful maintenance. |
| llm (provider: stub) | 25/25 | 7/7 | 0.2 ms | 4 | The stub is deterministic and inherits retrieval limitations; it does not represent the semantic reasoning or variability of a real LLM provider. |

## Which path would you ship for policy questions, and why?

I would ship the retrieval path as the baseline because it answers from the official knowledge base, supports abstention when evidence is insufficient, and achieved 25/25 correct answers with 7/7 correct abstentions on this evaluation set. I would keep deterministic routing and tools for narrowly defined tasks such as fee calculations, where predictable rules are preferable. I would add a real LLM only behind source-grounding validation and monitoring, because the current `stub` result does not demonstrate the performance of a production LLM.

**Controllability ratings are qualitative judgments:** deterministic is rated highest because its behavior is rule-based; retrieval is slightly lower because ranking and query expansion affect which evidence is selected; the stub path remains constrained but adds a generated-answer interface. Latencies are the p50 values from the latest benchmark run and are environment-specific.
