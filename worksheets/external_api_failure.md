# Lab 4 homework — design for an external service that goes down

Service chosen (weather / maps / news / other approved): weather (Open-Meteo) Base URL: https://api.open-meteo.com/v1/forecast

| Failure | How you simulate it | What your API returns | What the user sees |
|---|---|---|---|
| timeout | transport raises ConnectTimeout | 503 if no cache; 200 with stale=true if cache exists |Weather unavailable or cached weather|
| 500 from upstream | MockTransport returns 500 |503 without cache; cached weather otherwise|Error or old weather|
| malformed JSON | MockTransport returns `{}` |503 without cache; cached weather otherwise|Error or old weather|
| rate limited (429) | MockTransport returns 429 |503 without cache; cached weather otherwise|Error or old weather|

Timeout value and why: 3 seconds to prevent the application from waiting too long for the weather API. 
  
Retries and why: 1 retry to handle temporary network problems.

Cache TTL and why: 600 seconds (10 minutes) to reduce unnecessary API requests while keeping weather data reasonably recent.

Tests added (file + names):
- test_weather_ok
- test_weather_down_returns_503
- test_weather_stale_cache_when_upstream_fails
