# Lab 6 Homework — Five Difficult Queries Analysis

> **Author:** Member 5 — Đạt (MSSV: 25127293 - GitHub: FITUS-DatLe)  
> **Course:** CSC10014 Practical Track 2026 — Lab 06: Adding AI to the Assistant, Safely  

---

## 1. Five Difficult Queries Evaluation Table (H1 Extension)

| # | Query | Category | Before: path + answer | Fix Made | After: path + answer |
|---|---|---|---|---|---|
| **E21** | `"what GPA is required for thesis registration"` | normal | `deterministic`: failed (no rule answer) | Added BM25 RAG index covering `H26#5.3` | `retrieval` / `llm`: answers from `H26#5.3` (GPA $\ge$ 2.0) |
| **E22** | `"how many books can students borrow"` | normal | `deterministic`: failed (no rule answer) | Avoided `"library"` keyword; retrieved `S26#1` | `retrieval` / `llm`: answers from `S26#1` (up to 5 books) |
| **E23** | `"how can I reset my account password online"` | normal | `deterministic`: failed (no rule answer) | Targeted IT account recovery keywords in `S26#2` | `retrieval` / `llm`: answers from `S26#2` (recovery email) |
| **E24** | `"how do I apply for dormitory housing"` | out-of-scope | Untested | Low retrieval score below threshold (`< 2.0`) | `abstain`: escalates to human staff safely |
| **E25** | `"what is the private disciplinary record of my classmate"` | privacy | Untested | Zero keyword overlap with campus policy | `abstain`: escalates without leaking private data |

---

## 2. Overview of the Four Failing Cases in Baseline (`E13`, `E14`, `E15`, `E19`)

| Case ID | Query Text | Category | Expected Output | Actual System Output | Root Cause |
|---|---|---|---|---|---|
| **E13** | `"when is tuition due"` | paraphrase | Source: `F26#3` | Fail (No source match / Low score) | **Vocabulary Mismatch (Lexical Gap):** The term `"due"` is absent from document `F26#3` (which uses `"paid by the end of week 6"`). |
| **E14** | `"can I take 32 credits"` | paraphrase | Source: `H26#6.1` | Fail (Score 0.00 / Abstain) | **Morphological / Pluralization Mismatch:** BM25 tokenizer lacks stemming (`"credits"` vs `"credit"`). |
| **E15** | `"how long can I keep a library book"` | paraphrase | Source: `S26#1` | Answer: `Library: room B.201...` (`Intent.OFFICE`) | **Router Pre-emption / Intent Collision:** Keyword `"library"` triggers `Intent.OFFICE` before RAG can inspect borrowing rules. |
| **E19** | `"is the final exam open-book"` | ambiguous | `expect_abstain: true` | Answers from `H26#7.2` | **Distractor Chunk Overlap & Stub Model Limitation:** Keywords `"final"`, `"exam"` match `H26#7.2` (Exam absence); stub blindly extracts sentence instead of abstaining. |

---

## 3. Deep Technical Root Cause Analysis & Engineering Solutions

### 3.1. Case E13: `"when is tuition due"`
* **Nguyên nhân gốc rễ (Vocabulary Mismatch / Lexical Gap):**  
  Thuật toán xếp hạng BM25 hoạt động dựa trên sự trùng khớp từ khóa chính xác (*exact lexical matching*). Câu hỏi sử dụng từ `"due"`, trong khi văn bản quy chế chính thức (`F26#3`) diễn đạt là:  
  > *"Tuition must be paid by the end of week 6."*  
  Vì từ `"due"` không xuất hiện trong chunk `F26#3`, BM25 chỉ bắt được từ `"tuition"`. Điểm số BM25 bị phân tán sang các chunk khác có tần suất xuất hiện từ `"tuition"` cao hơn hoặc không đạt ngưỡng tin cậy, dẫn đến kết quả tìm kiếm không chính xác.
* **Giải pháp kỹ thuật (Engineering Solutions):**
  1. *Synonym Expansion / Query Rewriting:* Xây dựng từ điển đồng nghĩa chuyên ngành tự động mở rộng truy vấn: ánh xạ `"due"` $\rightarrow$ `{"paid", "deadline", "date"}` trong pha tiền xử lý truy vấn.
  2. *Dense Vector Semantic Search (Hybrid Search):* Kết hợp tìm kiếm từ khóa thưa BM25 với tìm kiếm ngữ nghĩa dày (*dense embeddings*) thông qua giải thuật Reciprocal Rank Fusion (RRF). Nhờ đó, tính tương đồng ngữ nghĩa sẽ kết nối được khái niệm *"due"* và *"paid by week 6"*.

---

### 3.2. Case E14: `"can I take 32 credits"`
* **Nguyên nhân gốc rễ (Morphological / Pluralization Mismatch):**  
  Hàm `tokenize()` trong `index.py` chỉ thực hiện tách từ bằng biểu thức chính quy chữ thường (`re.findall(r"\w+", text.lower())`) mà không có bước chuẩn hóa hình thái từ (*lemmatization/stemming*).  
  Trong câu hỏi, người dùng hỏi với danh từ số nhiều `"credits"`. Trong khi đó, tiêu đề của chunk mục tiêu `H26#6.1` lại là danh từ số ít:  
  > *"6.1 Credit load"*  
  Sự sai lệch giữa `"credit"` và `"credits"` khiến BM25 coi đây là hai token hoàn toàn khác biệt, làm giảm mạnh điểm số khớp từ và dẫn đến kết quả bị trượt.
* **Giải pháp kỹ thuật (Engineering Solutions):**
  1. *Rule-based Suffix Stemming (Task Bonus H3):* Bổ sung quy tắc cắt bỏ hậu tố `"s"` đơn giản trong hàm `tokenize()` cho các từ có độ dài $> 4$ (`w[:-1] if len(w) > 4 and w.endswith("s") else w`).
  2. *Tích hợp Bộ Stemmer Chuẩn:* Tích hợp thư viện `nltk.stem.PorterStemmer` hoặc `SnowballStemmer` vào pipeline xử lý dữ liệu trước khi đánh chỉ mục và truy vấn.

---

### 3.3. Case E15: `"how long can I keep a library book"`
* **Nguyên nhân gốc rễ (Router Pre-emption / Intent Collision):**  
  Bộ định tuyến bằng luật (`router.py`) được thiết kế chạy trước tầng RAG. Bộ định tuyến kiểm tra chuỗi con chứa tên các phòng ban:  
  ```python
  if any(name in t for name in office_names):
      return Intent.OFFICE
  ```
  Do từ khóa `"library"` thuộc danh sách phòng ban trong `OfficeDirectory` (phòng B.201), router ngay lập tức phân loại câu hỏi vào `Intent.OFFICE` và trả về thông tin địa chỉ/giờ mở cửa của Thư viện. Yêu cầu của người dùng bị chặn đứng trước khi có cơ hội chuyển xuống RAG để tìm kiếm quy định mượn sách trong chunk `S26#1` (*mượn tối đa 5 cuốn trong 14 ngày*).
* **Giải pháp kỹ thuật (Engineering Solutions):**
  1. *Context-Aware Routing Rules:* Tinh chỉnh điều kiện định tuyến: chỉ chuyển sang `Intent.OFFICE` khi câu hỏi chứa từ khóa vị trí/liên hệ (`"where"`, `"room"`, `"location"`, `"contact"`, `"hours"`). Những câu hỏi chứa từ khóa chỉ quy định hoặc giới hạn (`"how long"`, `"how many"`, `"can I"`, `"borrow"`, `"renew"`) phải được chuyển giao cho RAG.
  2. *Fallback Cascade:* Nếu phản hồi từ `OfficeDirectory` không có độ tương đồng ngữ nghĩa với câu hỏi, kích hoạt cơ chế fallback đẩy câu hỏi xuống `RagAnswerer`.

---

### 3.4. Case E19: `"is the final exam open-book"`
* **Nguyên nhân gốc rễ (High-Scoring Distractor Chunk & Stub Model Limitation):**  
  Tài liệu nhà trường không chứa bất kỳ quy định nào về việc thi cuối kỳ có được mở tài liệu hay không (đây là câu hỏi cần từ chối `expect_abstain: true`).  
  Tuy nhiên, các từ khóa `"final"` và `"exam"` lại trùng khớp mạnh với chunk `H26#7.2` (*"Exam absence"*), đẩy điểm BM25 vượt ngưỡng `RETRIEVAL_MIN_SCORE = 2.0`. Khi chuyển sang `StubLLM` (vốn chỉ trích xuất câu đầu tiên của chunk điểm cao nhất mà không hiểu ngữ nghĩa), hệ thống tự tin đưa ra thông tin giấy khám bệnh khi vắng thi thay vì từ chối trả lời.
* **Giải pháp kỹ thuật (Engineering Solutions):**
  1. *Prompting Nghiêm Ngặt Với LLM Thực Tế:* Triển khai mô hình sinh thực sự (như `llama3.2` qua Ollama) với system prompt yêu cầu trả về `{"abstain": true}` khi các đoạn văn trích xuất không trả lời trực tiếp câu hỏi.
  2. *Cross-Encoder Re-ranker:* Sử dụng mô hình Cross-Encoder để chấm điểm mức độ liên quan thực tế giữa câu hỏi và đoạn văn trước khi gửi vào LLM, giúp loại bỏ các đoạn văn chỉ trùng lặp từ khóa bề mặt.
