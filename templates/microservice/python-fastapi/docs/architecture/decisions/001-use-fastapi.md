# 001: Use FastAPI

## Context

The initial microservice needs a small HTTP API with an OpenAPI description and testable endpoints.

## Decision

Use FastAPI for the initial Python service.

## Alternatives Considered

Flask and Django REST Framework were considered.

## Consequences

The service receives OpenAPI generation and request validation while keeping the initial dependency set small.