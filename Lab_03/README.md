# Lab 03 – Containerization and Cluster Orchestration

**Student Name:** joy george  
**Course:** Cloud & Mobile Computing (CMC)

---

## What This Lab Covers

| Part | Topic | Tool |
|------|-------|------|
| A | Namespaces & cgroups (container isolation) | Docker |
| B | Image layering & multi-stage builds | Docker |
| C | Kubernetes cluster, deployments, services | kind + kubectl |
| D | Scheduling and node placement | kubectl |
| E | Self-healing and health probes | kubectl |

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `app.py` | Simple Flask web app with `/` and `/health` routes |
| `requirements.txt` | Python dependencies (Flask 3.0.0) |
| `Dockerfile.basic` | Single-stage Docker image |
| `Dockerfile.multistage` | Optimised two-stage Docker image |
| `deployment.yaml` | Kubernetes Deployment (3 replicas, with nodeSelector) |
| `service.yaml` | Kubernetes ClusterIP Service |
| `probe-deployment.yaml` | Deployment with readiness + liveness probes |
| `commands_and_results.txt` | Full step-by-step commands guide |

---

## Quick Start Order

```
# 1. Build images
docker build -f Dockerfile.basic -t lab3-basic .
docker build -f Dockerfile.multistage -t lab3-multi .

# 2. Create cluster
kind create cluster --name lab3-cluster

# 3. Load images
kind load docker-image lab3-basic --name lab3-cluster
kind load docker-image lab3-multi --name lab3-cluster

# 4. Label node
kubectl label nodes --all node-role=general

# 5. Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 6. Access
kubectl port-forward service/lab3-web-svc 8080:80
# Then open http://localhost:8080/

# 7. Cleanup
kind delete cluster --name lab3-cluster
```

---

## Key Concepts

**Namespaces** → isolate what a process can SEE (PIDs, network, filesystem)  
**cgroups** → limit how much CPU/memory a process can USE  
**Image layers** → each Dockerfile instruction = one cached layer  
**Multi-stage build** → keeps final image small by discarding build tools  
**Deployment** → tells Kubernetes the desired state (e.g. 3 replicas)  
**Self-healing** → Kubernetes auto-replaces failed pods to match desired state  
**Readiness probe** → gates traffic (don't send requests if not ready)  
**Liveness probe** → gates existence (restart if the container is stuck/dead)
