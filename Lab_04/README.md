# Lab 4 — Microservices and Cloud-Native Design

**Course:** Cloud and Mobile Computing
**Student Name:** joy george

---

## Overview

This lab implements a mini e-commerce backend using two microservices built with Python Flask and orchestrated with Docker Compose. The focus is on cloud-native principles: 12-factor app design, service-to-service communication, health checks, environment-based configuration, and failure resilience.

---

## Architecture

```
┌────────────────────────────────────────────────────┐
│                  Docker Compose Network             │
│                                                     │
│   ┌─────────────────┐      ┌──────────────────┐    │
│   │  product-service│◄─────│  order-service   │    │
│   │  Flask @ :5001  │ HTTP │  Flask @ :5002   │    │
│   └─────────────────┘      └──────────────────┘    │
└────────────────────────────────────────────────────┘
        ▲                             ▲
   curl/client                   curl/client
```

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| `product-service` | Python Flask | Serves product data from an in-memory catalog |
| `order-service` | Python Flask + requests | Accepts order requests, validates product via `product-service`, returns order total |
| Docker Compose | Container orchestration | Wires both services together with health checks and env config |

---




## How to Run

**Prerequisites:** Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose (Linux).

```bash
# 1. Clone the repo and navigate to this lab
git clone <your-repo-url>
cd Lab_04

# 2. Build and start both services
docker compose up --build -d

# 3. Verify both containers are running and healthy
docker compose ps
```

Both services should be up with ports `5001` and `5002` exposed on your host.

---

## API Reference

### product-service (port 5001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/products/<product_id>` | Get product by ID |

**Available products:**

| ID | Name | Price |
|----|------|-------|
| 1 | Laptop | $1200 |
| 2 | Phone | $650 |
| 3 | Headphones | $120 |

**Example requests:**
```bash
curl http://localhost:5001/health
curl http://localhost:5001/products/1
curl http://localhost:5001/products/99   # returns 404
```

---

### order-service (port 5002)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/orders` | Create a new order |

**Example request:**
```bash
curl -X POST http://localhost:5002/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

**Expected response (201):**
```json
{
  "message": "Order created",
  "product": "Laptop",
  "quantity": 2,
  "total_price": 2400
}
```

**Error responses:**

| Status | Cause |
|--------|-------|
| 400 | Product ID not found |
| 503 | `product-service` is unreachable |

---

## Failure Simulation

To test resilience, stop `product-service` and send an order request:

```bash
# Stop product-service
docker stop product-service

# Send order request — should return 503
curl -X POST http://localhost:5002/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 2, "quantity": 1}'

# Expected response:
# {"error": "product-service unavailable"}

# Restart the service
docker start product-service
docker compose ps
```

`order-service` retries the request twice with a 1-second delay before returning a `503`. This demonstrates graceful degradation in a synchronous microservice architecture.

---

## Cloud-Native Design Decisions

- **Stateless services** — neither service stores local state; data lives in memory or comes from requests.
- **Environment variables** — `order-service` reads `PRODUCT_SERVICE_URL` from the environment instead of hardcoding an address.
- **Health endpoints** — both services expose `/health`, used by Docker Compose's `healthcheck` configuration.
- **Restart policy** — `restart: unless-stopped` gives a first layer of self-healing at the Compose level.
- **Retry logic** — `order-service` retries failed calls to `product-service` with a timeout before surfacing an error.

---

## Teardown

```bash
docker compose down
```

---

## Reflection
- Benefits of microservices vs. monolith in this implementation
- New complexities introduced by splitting into two services
- Impact of increased network latency or slow dependencies
- 12-factor app principles visible in this lab
