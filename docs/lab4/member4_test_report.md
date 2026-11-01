\# Member 4 – External Weather API \& System Testing



\## 1. Weather API (T4)



\- Endpoint: `GET /v1/weather`

\- Calls `weather.current()` to retrieve current weather data.

\- Catches `ExternalServiceError`.

\- Returns HTTP 503 Service Unavailable when the external weather service fails.



\## 2. Automated Testing



Command:



```bash

python -m pytest -q

```



Result:



\- 30 passed

\- 0 failed

\- 1 warning



\## 3. Manual API Testing



Command:



```bash

BASE=http://127.0.0.1:8001 bash api-tests/curl\_tests.sh

```



Result: All 11 API checks returned the expected HTTP status codes.



| Endpoint / Scenario | Expected | Actual |

|---|---:|---:|

| Health | 200 | 200 |

| Chat fee | 200 | 200 |

| Chat rule | 200 | 200 |

| Empty chat | 422 | 422 |

| Wrong chat type | 422 | 422 |

| Submit feedback | 201 | 201 |

| Invalid feedback rating | 422 | 422 |

| Feedback without API key | 401 | 401 |

| Feedback with API key | 200 | 200 |

| Weather | 200 | 200 |

| Unknown route | 404 | 404 |



\## 4. Code Quality



\- `ruff check .`: All checks passed.

\- `ruff format --check .`: 24 files already formatted.



\## 5. Swagger Evidence



Screenshot: `docs/lab4/swagger\_chat\_success.png`



The `POST /v1/chat` endpoint returned HTTP 200 successfully.



\## 6. Conclusion



The Weather API and system testing activities were verified successfully. All automated tests passed, all 11 manual API checks returned their expected status codes, and Ruff checks passed.

