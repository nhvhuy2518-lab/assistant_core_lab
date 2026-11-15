# Lab 06 — Path Comparison & Reflection (Member 2: Hiếu)

## 1. Baseline Comparison Table (Original 20 Test Cases)

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          7/20       5/5     0.0     0.2   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
retrieval             16/20       4/5     0.0     0.0   fails: E13 E14 E15 E19
llm (stub)            16/20       4/5     0.1     0.2   fails: E13 E14 E15 E19
```

### Three-Sentence Analysis (Part F Exercise)
1. **Path choice for handbook questions:** For student handbook and academic regulation questions (`handbook_2026.md`), I would use the **LLM path (`llm` with RAG grounding and retrieval fallback)** (or the `retrieval` path when running strictly offline without a local LLM).
2. **Reason:** Unlike the `deterministic` path which only handles fee calculations and office locations (7/20 correct), the RAG pipeline retrieves the exact official paragraph (16/20 correct), enforces citation grounding (`set(draft.source_ids) <= allowed_ids`), abstains when confidence score is below `2.0`, and safely falls back to quoting the source chunk if the LLM output fails validation.
3. **First failure to fix:** I would prioritize fixing **E14 ("can I take 32 credits")** first by adding light plural stemming in `tokenize()` (stripping trailing `"s"` from words longer than 4 characters so `"credits"` matches `"credit"`), followed by refining the router rules for **E15 ("how long can I keep a library book")** so policy questions about library borrowing duration go to RAG instead of the static office-lookup tool.

---

## 2. Homework H1 — Extended Comparison Table (25 Test Cases: +5 Academic & Thesis Questions)

### Added Test Cases (`E21` – `E25` in `eval/cases.jsonl`)
- **E21 (Normal - Handbook):** `"thesis registration window in week 1 to week 3"` -> Expected source: `H26#5.3`
- **E22 (Normal - Handbook):** `"can I take more than 30 credits in a regular semester"` -> Expected source: `H26#6.1`
- **E23 (Normal - Handbook):** `"what to do if absent from final exam for medical reasons"` -> Expected source: `H26#7.2`
- **E24 (Out-of-scope / Abstain):** `"what is the minimum IELTS score for the master degree exchange scholarship in Japan"` -> `expect_abstain: true`
- **E25 (Out-of-scope / Abstain):** `"can the university approve a remote internship salary of 5000 USD"` -> `expect_abstain: true`

### Updated Comparison Table (25 Cases)

```text
path                correct  abstain ok  p50 ms  max ms
deterministic          9/25       7/7     0.0     0.3   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23
retrieval             21/25       6/7     0.0     0.1   fails: E13 E14 E15 E19
llm (stub)            21/25       6/7     0.1     0.2   fails: E13 E14 E15 E19
```

**Observation on the 5 new questions (1 sentence):**
All five new academic/thesis and out-of-scope questions (`E21`–`E25`) were handled accurately by the `retrieval` and `llm (stub)` paths because the normal queries shared domain keywords with `handbook_2026.md` sections (`score >= 2.0`), while the two out-of-scope questions scored below `RETRIEVAL_MIN_SCORE` and triggered the `A1` abstain guard before reaching the model.

---

## 3. Homework H2 — Reflection (5 Lines: Open-Book Exam Analogy)

Asking a standalone AI model about university rules is like giving a student a **closed-book exam**: it answers fluently from memory, which often leads to hallucinated deadlines or fees.
**RAG (Retrieval-Augmented Generation)** turns this into an **open-book exam** by first using our search engine (BM25) to locate the exact relevant paragraph in the official faculty handbook.
Before calling the AI, our code checks whether the best search score meets the minimum threshold (`score >= 2.0`), immediately saying *"I don't know"* (`abstain`) if no reliable paragraph is found.
We then hand only those retrieved paragraphs to the model and require it to return a structured JSON response containing both the answer and the cited `source_ids`.
Crucially, **our Python code—not the model—performs the grounding check (`set(draft.source_ids) <= allowed_ids`)**, verifying that every cited section was actually retrieved and falling back to a direct quote if the AI invents a fake citation.
