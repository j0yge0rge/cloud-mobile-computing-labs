# Cloud and Mobile Computing — Labs 1–4

**Course:** Cloud and Mobile Computing
**Instructor:** Dr. Youssef Senousy
**Student Name:joy george

---


## Lab Summaries

### Lab 1 — Cloud Virtualization and Data Center Architecture

**Topic:** Comparing VMs vs. containers, exploring cloud infrastructure, and simulating tail latency.

**What was done:**
- Launched a local Ubuntu VM using Multipass and a container using Docker, then compared their startup time, memory usage, and process count.
- Explored the AWS Nitro Hypervisor on an EC2 `t2.micro` instance — observed that Nitro components are visible but not directly accessible, demonstrating security enforcement.
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

## How to Run

Each lab folder is self-contained. General steps:

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Lab 2 — start distributed environment
cd Lab_02
docker-compose up

# Lab 3 — create local Kubernetes cluster
cd Lab_03
kind create cluster
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Lab 4 — start microservices
cd Lab_04
docker compose up --build
```

## Notes

- All work in this repository is original and was completed individually.
- Screenshots and terminal outputs were captured during actual lab execution.
