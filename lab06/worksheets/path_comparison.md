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


---

# Member 6: Đức — Path Comparison & Reflection

## 1. Comparison Table (30 test cases)

The 30 cases are the original 20, five cases from another member (E21–E25), and my five homework cases (E61–E65).

```text
path                correct  abstain ok  p50 ms  max ms
deterministic         11/30       9/9     0.0     0.6   fails: E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23 E61 E62 E63
retrieval             24/30       8/9     0.0     0.1   fails: E13 E14 E15 E19 E62 E63
llm (stub)            24/30       8/9     0.2     0.6   fails: E13 E14 E15 E19 E62 E63
```

### Three-sentence analysis

1. For handbook questions I would use the **llm path**, because it answers 24/30 questions correctly while the deterministic path answers only 11/30: it can only compute fees and look up offices.
2. The llm and retrieval paths have exactly the same failures, because the model only sees the paragraphs that search found; llm phrases the answer more readably, and retrieval remains the safe fallback when the model fails or is offline.
3. The first failures I would fix are E62 and E63, because they are the dangerous kind: search returns the wrong paragraph with a score above the 2.0 threshold, so the assistant does not abstain and gives a confident wrong answer.

## 2. Homework H1 — My five added questions (E61–E65)

I wrote three paraphrase questions that avoid the exact words used in the documents, and two questions the assistant should refuse.

| ID | Question | Expected | Result (BM25 top hits) |
|---|---|---|---|
| E61 | how do I get back into my school account if I forgot the login | S26#2 | Correct: S26#2 scored 3.44 |
| E62 | can I get my money back if I drop out | F26#4 | **Fail:** top hit H26#8.3 (4.09); F26#4 not in the top 3 |
| E63 | can I pause my studies for one semester | H26#8.1 | **Fail:** top hit S26#1 (2.30); H26#8.1 only third (1.20) |
| E64 | what is the best programming language to learn first | abstain | Correct: no hits, so the assistant abstains |
| E65 | can you suggest a good place to eat near campus | abstain | Correct: no hits, so the assistant abstains |

**Why E62 and E63 fail (one sentence each):**

- **E62:** the correct paragraph F26#4 uses the words "withdraw" and "refund", while my question says "money back" and "drop out", so no word matches and BM25 cannot connect them.
- **E63:** the correct paragraph H26#8.1 says "semesters" (plural), while my question says "semester", the same plural problem as E14; only a weak match remains, so a different paragraph scores higher.

**Observation:** both failures exceed `RETRIEVAL_MIN_SCORE = 2.0`, so the abstain guard (A1) does not trigger. A1 protects against "no match at all", but not against "a wrong match with a high score", which is why keyword search alone is not enough for paraphrased questions.

**What I would try next:** light plural stemming in `tokenize()` (the H3 fix) for E63, and a small synonym list ("refund" ~ "money back", "leave of absence" ~ "pause") for E62. I have not tested either fix.

## 3. Homework H2 — Reflection

Asking an AI model about our faculty's rules directly is like a closed-book exam: it answers fluently from memory, and it may invent a deadline or a fee.
RAG turns this into an open-book exam: our search code first finds the right paragraph in the official documents, then the model writes the answer from that paragraph only.
If search finds nothing relevant, our code says "I don't know" before the model is even called.
The model must return structured JSON with the answer and the ids of the sources it used.
One thing our code checks that the model does not is grounding: every cited source id must be one of the paragraphs we retrieved, and otherwise we discard the answer and quote the best paragraph instead.
