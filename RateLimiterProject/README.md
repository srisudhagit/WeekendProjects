# RateLimiter Project

## Description
ThrottleBox is a lightweight API rate-limiting service built using FastAPI, Redis, and Uvicorn, designed to control request traffic on a per-user or per-IP basis. It implements a Fixed Window algorithm to track and enforce rate limits efficiently.

## Tech Stack Used
FastAPI – For building high-performance, async API endpoints

Redis – Acts as a fast, in-memory data store for request counters and user-specific limit configurations

Uvicorn (ASGI server) – Runs the FastAPI app with async capabilities


## Core Features

### Fixed Window Rate Limiting:
Tracks requests per user/IP in Redis using a key like rate:<ip>. Limits are enforced using TTLs and counters.

### Dynamic Configuration via Admin API:
Admin endpoints (GET/POST /config/{user_id}) allow runtime configuration of rate limits, stored in Redis (config:<user_id>).

### Defaults + Overrides:
If no custom config exists, a default rate limit (e.g., 10 req/min) is applied automatically.


### Request Flow





