# Lab 4 Report – Microservices and Cloud-Native Design
**Student Name:** [Your Name Here]  
**Course:** Cloud and Mobile Computing  
**Lecturer:** Dr. Youssef Senousy  

---

## Overview

In this lab, I built a small cloud-native e-commerce backend using two microservices — `product-service` and `order-service` — containerized with Docker and orchestrated using Docker Compose. The goal was to understand microservice architecture, synchronous service-to-service communication, container packaging, and basic resilience patterns.

---

## Reflection Questions

### 1. Which parts of this lab show the benefits of microservices over a monolith?

Several aspects of the lab made the advantages of microservices concrete:

- **Independent deployment:** Each service (`product-service` and `order-service`) has its own `Dockerfile`, `requirements.txt`, and source code. This means either service could be updated, rebuilt, or redeployed without touching the other. In a monolith, all components are tightly coupled in a single codebase and deployed together.

- **Technology isolation:** Each service has its own dependency file. If `order-service` needed a different version of Flask or an additional library (e.g., a circuit-breaker), it could be added independently without breaking `product-service`.

- **Single responsibility:** `product-service` is only responsible for storing and returning product data. `order-service` handles the business logic of creating an order. This clean separation makes the codebase easier to understand, test, and maintain.

- **Scalability:** If the application were under heavy load from order creation, we could scale only `order-service` horizontally (e.g., run three replicas) without scaling `product-service`. A monolith would force us to scale the entire application.

---

### 2. Which new complexities were introduced by splitting the system into two services?

While microservices offer clear benefits, splitting the system introduced real challenges:

- **Network dependency:** In a monolith, `product-service` logic would be a simple function call in memory. In our microservice setup, `order-service` must make an HTTP request over the network to `product-service`. This adds latency and the possibility of network failure.

- **Failure propagation:** If `product-service` crashes or becomes slow, `order-service` is directly affected. This is visible in Part H of the lab — stopping `product-service` causes order creation to fail with a 503 error. Managing these cascading failures requires additional patterns (retries, timeouts, circuit breakers).

- **Service discovery:** `order-service` needs to know where `product-service` is running. In this lab, Docker Compose's built-in DNS (the container name `product-service` resolves automatically on the internal network) handles this. In a real cloud environment, this requires a service registry or a platform like Kubernetes.

- **Operational overhead:** Running two services means managing two containers, two sets of logs, two health checks, and two deployment pipelines. This overhead increases as more services are added.

---

### 3. What would break if network latency increased or one service became slow?

If network latency increased significantly:

- The `fetch_product()` function in `order-service` uses a 2-second timeout (`timeout=2`). If `product-service` becomes slow and responses take longer than 2 seconds, `order-service` will treat it as a failure and retry up to 2 more times. Each retry adds a 1-second delay. This means a single slow request could take up to 8 seconds to resolve before returning a 503 error.

- User-facing requests to `/orders` would become very slow, degrading the experience even though neither service has fully failed.

- If latency is intermittent (jitter), retries might mask the problem temporarily, but the retry logic itself consumes resources (threads, connections), which could lead to resource exhaustion under high load.

In a production system, this problem is typically addressed with circuit breakers (e.g., using a library like `pybreaker`), which stop sending requests to a slow or failing service for a period and return a fast fallback response instead.

---

### 4. Which 12-factor app principles are visible in this implementation?

The 12-factor app methodology (from https://12factor.net) defines best practices for cloud-native applications. Several principles are clearly visible in this lab:

| Factor | How it appears in this lab |
|---|---|
| **III. Config** | `PRODUCT_SERVICE_URL` is read from an environment variable, not hardcoded. This means the same Docker image can be deployed to different environments (dev, staging, production) just by changing the environment variable. |
| **IV. Backing services** | `product-service` acts as a backing service for `order-service`. It is accessed via a URL (a network address), which could be changed without modifying code. |
| **VI. Processes** | Both services are stateless processes. They do not write data to local disk or rely on session state. The product catalog is in-memory (acceptable for a lab scenario). |
| **VIII. Concurrency** | Each service is its own process running in its own container, making horizontal scaling straightforward. |
| **IX. Disposability** | Both services start quickly and can be stopped cleanly. Docker's `restart: unless-stopped` policy reflects the principle that processes should be disposable and replaceable. |
| **X. Dev/prod parity** | Docker containers ensure the development and production environment are identical. The same image that runs locally is the one that would be deployed to a cloud environment. |

---

## Failure Simulation Results

When `product-service` was stopped with `docker stop product-service` and a POST request was sent to `order-service`, the observed behavior was:

- `order-service` attempted the request, waited up to 2 seconds, then retried twice.
- After all retries were exhausted, it returned:
  ```json
  {"error": "product-service unavailable"}
  ```
  with HTTP status code **503 Service Unavailable**.

When `product-service` was restarted with `docker start product-service`, it recovered automatically and `order-service` was able to serve requests again.

This demonstrates how microservices need to be designed with the assumption that their dependencies may fail at any time — a principle called *design for failure*.

---

## Conclusion

This lab gave me a hands-on understanding of how microservices differ from monolithic applications in practice. The split introduced real operational complexity — network calls, failure handling, service discovery — but also gave each service the freedom to be deployed, scaled, and maintained independently. The Docker Compose setup made the architecture portable and reproducible. The key takeaway is that microservices are not inherently better than monoliths; the right choice depends on team size, scalability requirements, and operational maturity.
