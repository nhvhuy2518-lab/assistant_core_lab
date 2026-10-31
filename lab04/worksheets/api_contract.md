# Lab 4 — API contract worksheet

Fill in one row per endpoint **before** you code it.

| Method | Path | Request body / params | Success (code + body) | Errors (code + error.code) | Who calls it |
|---|---|---|---|---|---|
| GET | /health | None | 200 {status, version} | — | ops, UI |
| POST | /v1/chat | JSON: message, session_id | 200 ChatResponse | 422 invalid_request | UI, tests |
| POST | /v1/feedback | JSON: request_id, rating, comment | 201 FeedbackOut | 422 invalid_request | UI |
| GET | /v1/feedback | header X-API-Key | 200 feedback list | 401 missing_or_invalid_api_key | staff dashboard |
| GET | /v1/weather | None | 200 Weather | 503 weather_service_unavailable | UI |

Questions:
1. Which fields are required, and what are their limits?
ChatRequest.message: bắt buộc, 1–2000 ký tự.
ChatRequest.session_id: tùy chọn, tối đa 64 ký tự, mặc định "anonymous".
FeedbackIn.request_id: bắt buộc, 1–64 ký tự.
FeedbackIn.rating: bắt buộc, giá trị từ -1 đến 1.
FeedbackIn.comment: tùy chọn, tối đa 500 ký tự.

2. What does the UI show for each error code?
HTTP code	UI nên hiển thị
401	        Invalid or missing API key
422	        Invalid input. Please check your data
429	        Too many requests. Please try again later
503	        Weather service is unavailable

3. What changes would force a `/v2`?
A /v2 API would be needed when we make breaking changes, such as removing or renaming required fields, changing response formats, or changing endpoint behavior in a way that breaks existing clients.
