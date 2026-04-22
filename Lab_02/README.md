# Lab 2 — Distributed Consistency and Consensus in the Cloud

**Course:** Cloud and Mobile Computing
**Instructor:** Dr. Youssef Senousy
**Student Name:** joy george

---

## Overview

This lab explores how distributed systems maintain consistency, handle availability trade-offs, and reach consensus under failure conditions. Two tools are used:

- **Redis** — to simulate eventual consistency and observe CAP theorem behavior under a network partition
- **etcd** — to experiment with the Raft consensus protocol, including leader election and failover

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- Docker Compose

---


## How to Run

**Start the environment:**
```bash
docker-compose up
```

**Stop and clean up:**
```bash
docker-compose down
```

---

## Task 1 — Redis Replication and CAP Theorem

### What was done

Connected to both Redis nodes and demonstrated eventual consistency by writing to one replica and immediately reading from the other. Then simulated a network partition by stopping `redis-node2` to observe how the cluster handles availability vs. consistency.

### Commands used

```bash
# Connect to Redis nodes
docker exec -it redis-node1 redis-cli
docker exec -it redis-node2 redis-cli

# Write a key on node1
SET mykey "hello"

# Read from node2 (immediately — may not yet be replicated)
GET mykey

# Simulate partition — stop node2
docker stop redis-node2

# Attempt writes on node1 while node2 is down
SET anotherkey "world"

# Bring node2 back and check if it caught up
docker start redis-node2
docker exec -it redis-node2 redis-cli GET anotherkey
```

### Observations

> *(Fill in: Did the read on node2 reflect the write immediately? What happened to writes during the partition? Did node2 sync after restarting?)*

---

## Task 2 — Raft Consensus with etcd

### What was done

Used `etcdctl` to write and read key-value pairs from the etcd cluster, inspected which node was the current leader, then stopped the leader container to trigger an automatic leader re-election and observed the outcome.

### Commands used

```bash
# Write a key-value pair
docker exec -it etcd etcdctl put foo bar

# Read it back
docker exec -it etcd etcdctl get foo

# Check cluster status and identify the leader
docker exec -it etcd etcdctl endpoint status

# Stop the leader to trigger re-election
docker stop <leader-container-name>

# Check status again — a new leader should be elected
docker exec -it etcd etcdctl endpoint status
```

### Observations

> *(Fill in: Which node was the initial leader? How long did re-election take? Was the cluster available during the transition?)*

---

## Reflection

> *(Answer these in `reflection.md` — summarized here for quick reference)*

**1. How does Redis demonstrate the CAP theorem?**
Redis in a replicated setup prioritizes availability over strong consistency — it stays writable during a partition, accepting the risk of stale reads on replicas. This makes it an AP system under the CAP model.

**2. What is the role of the Raft protocol in etcd?**
Raft ensures that all nodes in the etcd cluster agree on the same sequence of writes, even when nodes fail. It does this by electing a single leader responsible for coordinating all writes, and replicating the log to a majority of nodes before committing.

**3. What trade-offs did you observe between Redis and etcd?**
> *(Fill in your own comparison based on what you saw.)*

---

## Key Concepts Covered

| Concept | Tool Used |
|--------|-----------|
| Eventual consistency | Redis replication |
| Network partition simulation | Docker (`docker stop`) |
| CAP theorem (AP vs CP) | Redis vs etcd comparison |
| Raft leader election | etcd cluster |
| Consensus and failover | etcd + `etcdctl` |
