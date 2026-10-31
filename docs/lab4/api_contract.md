# Lab 4 — API contract worksheet

Fill in one row per endpoint **before** you code it.

| Method | Path | Request body / params | Success (code + body) | Errors (code + error.code) | Who calls it |
|---|---|---|---|---|---|
| GET | /health | — | 200 `{"status": "ok", "version": "1.0.0"}` | — | ops, UI |
| POST | /v1/chat | `{"message": str, "session_id"?: str}` | 200 `{"answer", "intent", "sources", "degraded", "request_id"}` | 422 (`invalid_request`), 429 (`too_many_requests`) | UI, tests |
| POST | /v1/feedback | `{"request_id": str, "rating": int (-1, 0, 1), "comment"?: str}` | 201 `{"request_id", "rating", "comment", "id", "created_at"}` | 422 (`invalid_request`) | UI |
| GET | /v1/feedback | header `X-API-Key: <key>` | 200 `[{"request_id", "rating", "comment", "id", "created_at"}, ...]` | 401 (`missing_or_invalid_api_key`) | staff dashboard |
| GET | /v1/weather | — | 200 `{"temperature_c", "wind_kmh", "description", "observed_at", "stale"}` | 503 (`weather_service_unavailable`) | UI |
| GET | /v1/offices | — | 200 `[{"name", "room", "hours"}, ...]` | — | UI, tests |

Questions:
1. Which fields are required, and what are their limits?
- `ChatRequest`: `message` (required, 1 <= length <= 2000 chars), `session_id` (optional, default "anonymous", max 64 chars).
- `FeedbackIn`: `request_id` (required, 1 <= length <= 64 chars), `rating` (required integer in {-1, 0, 1}), `comment` (optional, max 500 chars).
- `GET /v1/feedback`: `X-API-Key` header is required and must match `API_ADMIN_KEY`.

2. What does the UI show for each error code?
- 401 Unauthorized: Prompt admin to log in or enter a valid API key.
- 404 Not Found: "The requested resource could not be found."
- 422 Unprocessable Entity: Highlight specific invalid input field (e.g., "Message cannot be empty").
- 429 Too Many Requests: "You are sending requests too quickly. Please wait a minute and try again."
- 503 Service Unavailable: "Weather service is currently unavailable. Please try again later."

3. What changes would force a `/v2`?
- Breaking schema changes, such as renaming fields (e.g., `message` to `prompt`, `answer` to `text`).
- Removing fields or making optional fields required.
- Altering the URL structure or fundamental contract behavior (e.g. changing request/response envelope format).
