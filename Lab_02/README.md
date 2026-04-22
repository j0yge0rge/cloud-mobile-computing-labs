Here’s a clean, professional **README.md** you can put in your GitHub repo (especially for **Lab 02**) that includes your reflection answers and aligns with your lecturer’s requirements.

---

# 📘 Distributed Systems Labs Repository

## 👤 Student Information

* **Name:** [Your Name]
* **Course:** [Course Name]
* **Instructor:** [Instructor Name]
* **Submission Deadline:** 26 April

---

## 📂 Repository Structure

```
Lab_01/
Lab_02/
Lab_03/
Lab_04/
GitHub_Link.txt
```

Each folder contains:

* Source files
* Configuration files
* Screenshots / outputs
* Reflection answers

---

# 🧪 Lab 02: Distributed Consistency and Consensus

## 📌 Overview

This lab explores how distributed systems handle:

* Consistency
* Availability
* Partition tolerance (CAP theorem)
* Consensus using the Raft algorithm

We used:

* **Redis** → to demonstrate replication and eventual consistency
* **etcd** → to demonstrate consensus and leader election

---

## ⚙️ Setup

Run the following command to start the environment:

```bash
docker-compose up
```

To stop:

```bash
docker-compose down
```

---

## 🧪 Tasks Performed

### 🔹 Task 1: Redis Replication

* Connected to `redis-node1` (master) and `redis-node2` (replica)
* Wrote data to master
* Observed delayed replication on replica
* Simulated network partition by stopping replica

### 🔹 Task 2: Raft Consensus with etcd

* Inserted key-value pairs using `etcdctl`
* Identified the leader node
* Simulated failure by stopping leader
* Observed automatic leader re-election

---

## 📊 Key Observations

* Redis replication is **asynchronous**
* Temporary inconsistency occurs during network issues
* etcd maintains **strong consistency** using Raft
* Leader election ensures system reliability

---

## 📝 Reflection Questions

### Q1. What does "eventual consistency" mean, and how did Redis demonstrate it?

Eventual consistency means that updates made to a system are not immediately visible on all nodes, but given enough time, all nodes will become consistent.

In Redis, this was demonstrated through replication between the master (redis-node1) and the replica (redis-node2). When a key was written to the master, it did not instantly appear on the replica. However, after a short delay, the replica synchronized and reflected the updated data. Additionally, when a network partition was simulated, writes made during the disconnection were later synchronized once the replica reconnected.

---

### Q2. How does the CAP theorem apply to Redis?

The CAP theorem states that a distributed system can only guarantee two out of three properties:

* Consistency
* Availability
* Partition Tolerance

Redis replication mode follows the **AP (Availability + Partition Tolerance)** model. It continues accepting writes on the master even during network partitions, ensuring availability. However, this may lead to temporary inconsistency, as replicas can serve outdated data until synchronization occurs.

---

### Q3. What is the Raft consensus algorithm and what problem does it solve?

Raft is a consensus algorithm designed to ensure that multiple nodes in a distributed system agree on the same state.

It works by electing a **leader node**, which is responsible for handling all write requests. The leader replicates changes to follower nodes and ensures that only committed entries are applied.

Raft solves the problem of maintaining consistency across distributed systems, even in the presence of node failures, by ensuring that all nodes agree on the same sequence of operations.

---

### Q4. What happened when you stopped the etcd leader?

When the etcd leader node was stopped, the remaining nodes in the cluster detected the failure.

They initiated a new leader election process using the Raft algorithm. Since the cluster had three nodes, the remaining two formed a quorum and successfully elected a new leader.

The system continued functioning without interruption, demonstrating fault tolerance and high availability.

---




