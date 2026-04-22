\# Lab 1 – Discussion Prompts \& Reflection

\*\*Student Name:\*\* Joy  

\*\*Course:\*\* Cloud and Mobile Computing  

\*\*Lecturer:\*\* Dr. Youssef Senousy  

\*\*Lab Title:\*\* Exploring Cloud Virtualization and Data Center Architecture



\---



\## Discussion Prompt 1: Why does AWS split Nitro into hardware components?



AWS splits the Nitro hypervisor into dedicated hardware components (Nitro Cards for networking, storage, and security, plus the Nitro Security Chip) for two main reasons: \*\*performance\*\* and \*\*security\*\*.



Traditionally, a hypervisor runs on the same CPU as the guest VMs, meaning it consumes some of the host's compute resources. By offloading networking and storage functions to separate physical Nitro Cards, AWS frees up nearly 100% of the server's CPU for the customer's workload — nothing is "stolen" by the hypervisor itself.



From a security perspective, splitting Nitro into isolated hardware components means there is no privileged software layer that an attacker could compromise to access other customers' data. Each component has a minimal, well-defined function with no administrative access — not even AWS employees can log into the underlying host. This is visible when running `dmesg | grep -i nitro` on an EC2 instance: you can \*see\* the Nitro layer is there, but you cannot interact with or modify it, demonstrating strong security enforcement by design.



\---



\## Discussion Prompt 2: In which scenarios would you use VMs over containers?



While containers are lightweight and fast, there are scenarios where Virtual Machines are the better choice:



\- \*\*Strong isolation is required:\*\* VMs run a full separate OS kernel, making them much harder to escape from. For running untrusted or third-party code (e.g., a cloud IDE or a code judge platform), VMs provide a stronger security boundary than containers which share the host kernel.



\- \*\*Different operating systems are needed:\*\* If you need to run a Windows workload alongside a Linux host, or an older kernel version, you need a VM — containers cannot run a different OS kernel than the host.



\- \*\*Legacy applications:\*\* Older software that was built to run on a full OS (with specific system services, drivers, or configurations) often cannot be easily containerized and works better inside a VM.



\- \*\*Compliance and regulatory requirements:\*\* Some industries (banking, healthcare) require full OS-level isolation between workloads for compliance reasons, which VMs provide more reliably.



In contrast, \*\*containers are preferred for microservices\*\* because they are lightweight, start in milliseconds, consume far less memory, and are easy to scale horizontally — making them ideal when running many small, independent services.



\---



\## Discussion Prompt 3: How does tail latency change with the number of parallel calls?



Tail latency refers to the response times at the high end of the distribution — typically the slowest 1% or 5% of requests (P99, P95). As the number of parallel calls increases, tail latency gets significantly worse due to a phenomenon sometimes called the \*\*"weakest link" effect\*\*.



Here is why: if a single request has a 1% chance of being slow, and you make 1 request, you probably get a fast response. But if your application makes 100 parallel sub-requests (for example, a search engine querying 100 servers at once and waiting for all of them), the chance that \*at least one\* of those is slow becomes much higher — and since you have to wait for all of them to finish, the overall response time is dominated by the slowest one.



This was observed in our tail latency simulation using the Flask app with exponential random delays. As concurrency (`-c 10` in `ab`, or parallel threads in our Python test) increased, the maximum and P99 latency values rose sharply, even though the median stayed relatively stable. This demonstrates why warehouse-scale systems (like Google and AWS) invest heavily in techniques such as \*\*hedged requests\*\* (sending a duplicate request if the first is slow) and \*\*load shedding\*\* to keep tail latency under control at scale.



\---



\## Tools Used

\- Python 3 (Flask, requests, matplotlib)

\- Docker (container simulation)

\- Multipass (VM simulation)

\- Windows PowerShell (latency\_test.py, histogram.py as replacements for Linux `ab` tool)



\---



