# Lab 3 — Containerization and Cluster Orchestration

**Course:** Cloud and Mobile Computing — Week 3
**Instructor:** Dr. Youssef Senousy
**Student Name:** joy george

---

## Overview

This lab moves from container theory into hands-on systems work. It covers Linux isolation mechanisms (namespaces and cgroups), Docker image layering and multi-stage builds, local Kubernetes cluster orchestration using `kind`, scheduling with node selectors, and self-healing behavior through pod deletion and health probes.

---

## Prerequisites

- Docker Desktop or Docker Engine
- [`kind`](https://kind.sigs.k8s.io/) (Kubernetes in Docker)
- `kubectl`
- A terminal and text editor
- Minimum 8 GB RAM recommended

---

## How to Run

### 1. Build Docker images

```bash
# Basic image
docker build -f Dockerfile.basic -t lab3-basic .

# Multi-stage image
docker build -f Dockerfile.multistage -t lab3-multi .

# Compare sizes
docker image ls
```

### 2. Create the local Kubernetes cluster

```bash
kind create cluster --name lab3-cluster

# Load images into the cluster
kind load docker-image lab3-basic --name lab3-cluster
kind load docker-image lab3-multi --name lab3-cluster

# Verify
kubectl cluster-info
kubectl get nodes -o wide
```

### 3. Deploy the application

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Check status
kubectl get pods -o wide
kubectl describe deployment lab3-web
```

### 4. Access the service

```bash
kubectl port-forward service/lab3-web-svc 8080:80

# In a separate terminal
curl http://localhost:8080/
curl http://localhost:8080/health
```

### 5. Apply node selector (scheduling)

```bash
kubectl label nodes --all node-role=general
kubectl get nodes --show-labels
# Then re-apply deployment.yaml after adding the nodeSelector field
```

### 6. Test self-healing

```bash
# Delete a pod and watch it get recreated
kubectl get pods
kubectl delete pod <POD_NAME>
kubectl get pods -w
```

### 7. Deploy with health probes

```bash
kubectl apply -f probe-deployment.yaml
kubectl describe pod <POD_NAME>
```

### 8. Cleanup

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f probe-deployment.yaml
kind delete cluster --name lab3-cluster
```

---

## Deliverables Summary

| # | Deliverable | What's included |
|---|-------------|-----------------|
| D1 | Namespace and cgroup observations | Screenshots from Tasks A1–A3 |
| D2 | Image size comparison table | Output of `docker image ls` and `docker history` for both images |
| D3 | Kubernetes deployment evidence | Pod listings, service access via `curl` |
| D4 | Self-healing evidence | `kubectl get pods -w` output showing pod recreation |
| D5 | Reflection answers | See `reflection.md` |

---

## Key Concepts Demonstrated

- **Namespaces** isolate what a container process can see (PID, network, mount, hostname).
- **cgroups** limit how much CPU and memory a container can consume.
- **Multi-stage builds** reduce final image size by separating the build environment from the runtime environment.
- **Kubernetes Deployments** manage desired state — if a Pod dies, the controller reconciles it back.
- **Readiness probes** gate traffic to a Pod; **liveness probes** restart a Pod if it becomes unhealthy. They are not interchangeable.
- **Node selectors** allow declarative scheduling constraints without hard-coding machine names.
