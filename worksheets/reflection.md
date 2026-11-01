# Lab 4 – Member 6: Reflection and Test Explanation

## H2 – Reflection

In Lab 3, we call `service.handle()` directly from Python code to get an answer.

In Lab 4, the client sends an HTTP POST request to `/v1/chat` with JSON data.

FastAPI receives the request, calls `service.handle()`, and returns the result as JSON.

The HTTP API allows websites, mobile apps, and other programs to use the same backend.

This helps teamwork because frontend and backend developers can work independently using the same API contract.

## Part E.4 – Test Explanation

**Test:** `test_weather_down_returns_503`

The test uses a mock HTTP transport that raises a `ConnectTimeout` exception to simulate a weather API failure, then checks that the application returns HTTP 503 with the correct error code.

**Why is this useful?**

It allows us to test how the application handles network failures without disconnecting from the Internet or depending on a real weather service.