# Lab 4 — Reflection (H2)

1. **Protocol & Decoupling:** In Lab 3, calling `service.handle()` was a direct in-process Python function invocation requiring the caller and service to share the same runtime and memory space. In Lab 4, `POST /v1/chat` exposes a standard HTTP/JSON interface across the network.
2. **Language & Platform Agnostic:** The REST API allows diverse clients (React web apps, mobile apps, or other backend microservices) written in any language to communicate with the assistant without depending on internal Python modules.
3. **Independent Deployment & Scalability:** The backend service can be deployed, scaled horizontally, or updated in isolation without forcing clients to redeploy or recompile.
4. **Standardized Governance & Error Handling:** The HTTP API layer enforces unified input validation (Pydantic 422), rate limiting (429), status codes, and security guards before requests ever touch the core domain logic.
5. **Clear Team Collaboration Contract:** The OpenAPI specification (`/docs`) provides an interactive, live contract enabling frontend and backend teams to develop and test concurrently without blocking each other.
