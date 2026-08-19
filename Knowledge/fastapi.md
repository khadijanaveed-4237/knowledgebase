---
title: FastAPI
date: "2026-08-16"
author: ""
last_audited: "2026-08-16"
tags: [fastapi, python, web-framework]
status: literature # fleeting | literature | permanent
sources:
  - https://fastapi.tiangolo.com
  - https://github.com/fastapi/fastapi
references: []
aliases: []
---

# FastAPI

## Summary

FastAPI is a modern, high-performance Python web framework for building APIs. It is built on Starlette (for the web parts) and Pydantic (for data validation), and leverages Python type hints to give automatic request validation, serialization, and interactive API documentation with very little boilerplate.

## Notes

- **Architecture**: An ASGI framework layered on top of Starlette and Pydantic. ASGI support means async/await code works natively, alongside sync endpoints.
- **Type-hint-driven**: Path parameters, query parameters, and bodies are declared with Python type hints. FastAPI derives validation, parsing, and docs from the hints alone.
- **Automatic docs**: OpenAPI schema is generated from the code; interactive docs are served at `/docs` (Swagger UI) and `/redoc` (ReDoc) with zero configuration.
- **Pydantic models**: Request/response bodies are declared as Pydantic models, giving validation errors as structured JSON (`422` responses) and automatic serialization on output.
- **Dependency injection**: The `Depends` system provides reusable dependency resolution per-request (auth, DB sessions, config), with support for sub-dependencies and caching via `use_cache`.
- **Response models**: The `response_model` parameter controls what the API exposes, filtering out private fields from responses.
- **Async and sync**: `async def` endpoints run on the event loop; sync `def` endpoints run in a threadpool so blocking code doesn't stall the server.
- **Testing**: `fastapi.testclient.TestClient` (built on `httpx`) makes endpoint testing straightforward with pytest.
- **Ecosystem**: Typically deployed with uvicorn; integrates with SQLAlchemy, Pydantic Settings, structured logging, and modern tooling.
- **Performance**: Benchmarks rank it among the fastest Python frameworks, comparable to Starlette and faster than Flask/Django for API workloads.

## References

<!-- Internal [[wikilinks]] to related notes. -->
- (none yet — no related notes in the vault)

## Changelog

- `2026-08-16` — Created.