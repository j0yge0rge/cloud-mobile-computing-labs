import csv
import matplotlib.pyplot as plt

latencies = []

with open("results.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        latencies.append(float(row["Latency_ms"]))

plt.figure(figsize=(10, 6))
plt.hist(latencies, bins=20, color='steelblue', edgecolor='black')
plt.title("Tail Latency Histogram - Lab 1")
plt.xlabel("Response Time (ms)")
plt.ylabel("Number of Requests")

# Mark the tail
p95 = sorted(latencies)[int(0.95 * len(latencies))]
plt.axvline(p95, color='red', linestyle='--', label=f'P95 = {p95:.1f} ms')
plt.legend()

plt.savefig("latency_histogram.png")
plt.show()
print("Saved as latency_histogram.png")