# Cloud and Mobile Computing — Labs 1–5

**Course:** Cloud and Mobile Computing  
**Instructor:** Dr. Youssef Senousy  
**Student Name:** Joy George  

---

## Lab Summaries

### Lab 1 — Cloud Virtualization and Data Center Architecture
**Topic:** Comparing VMs vs. containers, exploring cloud infrastructure, and simulating tail latency.

**What was done:**
- Launched a local Ubuntu VM using Multipass and a container using Docker, then compared their startup time, memory usage, and process count.
- Explored the AWS Nitro Hypervisor on an EC2 t2.micro instance — observed that Nitro components are visible but not directly accessible, demonstrating security enforcement.
- Built and deployed a Flask web app with artificial exponential delay to simulate tail latency, then benchmarked it using Apache Bench (`ab`) and plotted a response-time histogram.

**Key files:**

| File | Description |
|------|-------------|
| `screenshots/` | VM vs. container resource comparison, EC2 console, htop output |
| `latency_histogram.*` | Response-time distribution from the Flask benchmark |
| `reflection.md` | Written answers: VM vs. container trade-offs, Nitro architecture, tail latency behavior |

---

### Lab 2 — Distributed Consistency and Consensus
**Topic:** Hands-on exploration of the CAP theorem using Redis replication and Raft consensus using etcd.

**What was done:**
- Spun up a multi-node Redis environment using Docker Compose and demonstrated eventual consistency by writing to one replica and reading from another.
- Simulated a network partition by stopping a Redis node and observed the effect on write availability.
- Set up a three-node etcd cluster, wrote key-value pairs using `etcdctl`, inspected cluster leader status, and triggered a leader re-election by stopping the leader container.

**Key files:**

| File | Description |
|------|-------------|
| `docker-compose.yml` | Multi-container setup for Redis nodes and etcd cluster |
| `commands_output.md` | Terminal outputs for all `redis-cli` and `etcdctl` commands |
| `screenshots/` | Replication behavior, partition simulation, leader election |

---

### Lab 3 — Containerization and Cluster Orchestration
**Topic:** Linux namespaces and cgroups, Docker image layering, Kubernetes deployment, scheduling, and self-healing.

**What was done:**
- Ran an interactive Ubuntu container and inspected its isolated hostname, PID namespace, network interface, and cgroup hierarchy.
- Applied CPU and memory limits via Docker `--cpus` and `--memory` flags, then verified enforcement with `docker stats`.
- Built a basic and a multi-stage Dockerfile for a Flask app and compared image sizes and layer reuse.
- Created a local Kubernetes cluster with `kind`, deployed a multi-replica Flask application, and exposed it with a Service.
- Tested self-healing by force-deleting Pods and confirming the Deployment controller recreated them automatically.
- Configured readiness and liveness probes and explained the difference between the two.

**Key files:**

| File | Description |
|------|-------------|
| `Dockerfile.basic` / `Dockerfile.multistage` | Single-stage and multi-stage image builds |
| `app.py` + `requirements.txt` | Simple Flask app used in the Kubernetes deployment |
| `deployment.yaml` | Kubernetes Deployment manifest |
| `service.yaml` | Kubernetes Service manifest |
| `probe-deployment.yaml` | Deployment with readiness and liveness probes |
| `screenshots/` | Pod listings, service output, self-healing evidence |
| `reflection.md` | Answers to namespace/cgroup and scheduling questions |

---

### Lab 4 — Microservices and Cloud-Native Design
**Topic:** Building a two-service cloud-native backend using Python Flask and Docker Compose, with service-to-service communication, health endpoints, and failure simulation.

**What was done:**
- Implemented `product-service`: a stateless Flask API that returns product data from an in-memory catalog and exposes a `/health` endpoint.
- Implemented `order-service`: a Flask service that accepts order requests, calls `product-service` synchronously over HTTP, and returns an order response. Uses environment variables for service discovery and includes timeout/retry resilience.
- Packaged each service in its own Dockerfile and wired both together with Docker Compose.
- Verified successful end-to-end API calls with `curl` and simulated failure by stopping `product-service`, observing how `order-service` degrades gracefully.

**Key files:**

| File | Description |
|------|-------------|
| `product-service/app.py` | Product lookup service |
| `order-service/app.py` | Order creation service with inter-service HTTP call |
| `*/Dockerfile` | Container image definitions for each service |
| `docker-compose.yml` | Orchestrates both services together |
| `screenshots/` | Successful API calls and failure simulation output |
| `report.md` | Reflection on monolith vs. microservices trade-offs |

---

### Lab 5 — Local Serverless Computing and Event-Driven Image Processing Pipeline
**Topic:** Simulating FaaS and event-driven architecture locally using Redis Streams, containerized functions, and a folder-watching event source.

**What was done:**
- Implemented a folder watcher (`watcher.py`) as the event source — detects new images dropped into `/data/input/` and publishes `image.uploaded` events to a Redis Stream.
- Built an event router (`event_router.py`) that reads from the Redis Stream and fans out each event to two function endpoints simultaneously.
- Implemented `image-resizer`: a Flask function that resizes the incoming image and saves the output to `/data/output/`.
- Implemented `notifier`: a Flask function that logs a notification for each processed event, demonstrating event fan-out.
- Conducted a cold-start mini-experiment by measuring and comparing response time before and after restarting a function container.

**Key files:**

| File | Description |
|------|-------------|
| `docker-compose.yml` | Orchestrates Redis, event-source, router, and both functions |
| `event_source/watcher.py` | Watches input folder and publishes events to Redis Stream |
| `router/event_router.py` | Reads events from Redis and routes them to function endpoints |
| `functions/image_resizer/app.py` | Resizes image and saves result to `/data/output/` |
| `functions/notifier/app.py` | Logs a notification for each received event |
| `screenshots/` | Running containers, event logs, output image, cold-start results |
| `reflection.md` | Answers to serverless/event-driven architecture questions |

---

## How to Run

Each lab folder is self-contained. General steps:

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Lab 2 — start distributed environment
cd Lab_02
docker compose up

# Lab 3 — create local Kubernetes cluster
cd Lab_03
kind create cluster
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Lab 4 — start microservices
cd Lab_04
docker compose up --build

# Lab 5 — start serverless pipeline
cd Lab_05
docker compose up --build
```

---

## Notes

- All work in this repository is original and was completed individually.
- Screenshots and terminal outputs were captured during actual lab execution.
- The GitHub repository is organized using clearly named folders (`Lab_01` through `Lab_05`) and is accessible for review.
