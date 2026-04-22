# Lab 1 — Exploring Cloud Virtualization and Data Center Architecture

**Course:** Cloud and Mobile Computing
**Instructor:** Dr. Youssef Senousy
**Student Name:** joy george

---

## Overview

This lab explores the practical differences between Virtual Machines and containers, investigates cloud infrastructure through AWS, and simulates tail latency behavior in distributed systems. It covers three hands-on parts: local VM vs. container comparison, cloud infrastructure exploration on EC2, and a Flask-based latency simulation.

---


## What Was Done

### Part A — VMs vs. Containers (Local)

- Launched a local Ubuntu VM using Multipass and an Ubuntu container using Docker.
- Measured and compared resource usage (memory, processes, disk) using `free -h`, `ps aux`, and `df -h`.
- Observed differences in startup time, memory footprint, and process isolation between the two environments.

### Part B — Cloud Infrastructure Exploration (AWS EC2)

- Launched a free-tier EC2 `t2.micro` instance on AWS.
- Ran `dmesg | grep -i nitro` and `dmidecode` to inspect the AWS Nitro Hypervisor from inside the instance.
- Observed that Nitro components are visible in system info but not directly accessible — demonstrating how AWS enforces hardware-level security boundaries.
- Used `htop` to inspect running processes on the instance.

### Part C — Tail Latency Simulation

- Built a Flask app (`app.py`) that introduces an artificial exponential delay on every request to mimic real-world tail latency behavior.
- Benchmarked the app using Apache Bench: `ab -n 100 -c 10 http://localhost:5000/`
- Plotted a histogram of the 100 response times to visualize the long tail distribution.

---

## How to Run Part C

```bash
pip install flask
python app.py
```

In a separate terminal:

```bash
ab -n 100 -c 10 http://localhost:5000/
```

---

## Key Findings

- **Containers** start faster and use significantly less memory than VMs because they share the host kernel instead of running a full OS.
- **VMs** provide stronger isolation and are better suited to running different operating systems or untrusted workloads.
- **For microservices**, containers are generally the better choice due to their low overhead, fast startup, and ease of orchestration.
- **Tail latency** increases noticeably with concurrency — a small fraction of requests can take many times longer than the median, which compounds in systems with many parallel service calls.
- **AWS Nitro** splits hypervisor responsibilities across dedicated hardware (NitroCards) to reduce overhead and improve security — visible from inside a guest instance but not exploitable.

---

## Discussion Responses

**Why does AWS split Nitro into hardware components?**
To offload virtualization tasks (networking, storage, security) from the main CPU to dedicated hardware cards. This reduces overhead, improves performance, and strengthens the security boundary between the hypervisor and guest instances.

**In which scenarios would you use VMs over containers?**
When you need full OS isolation (e.g., running Windows on a Linux host), stricter security boundaries for untrusted code, or when the application requires kernel-level customization that containers can't provide.

**How does tail latency change with the number of parallel calls?**
It gets worse. When a request depends on multiple parallel downstream calls, the total response time is determined by the slowest one. As the fan-out increases, the probability of hitting a slow tail response grows, making high-percentile latency (P99, P999) a critical concern in distributed systems.
