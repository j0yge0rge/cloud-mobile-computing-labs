import requests
import time
import statistics
import csv

NUM_REQUESTS = 100
results = []

print("Sending 100 requests... please wait\n")

for i in range(NUM_REQUESTS):
    start = time.time()
    try:
        requests.get("http://localhost:5000/", timeout=30)
    except:
        pass
    elapsed = (time.time() - start) * 1000  # convert to milliseconds
    results.append(elapsed)
    print(f"Request {i+1}: {elapsed:.1f} ms")

# Stats
results.sort()
print("\n========= RESULTS =========")
print(f"Min:    {min(results):.1f} ms")
print(f"Mean:   {statistics.mean(results):.1f} ms")
print(f"Median: {statistics.median(results):.1f} ms")
print(f"P90:    {results[int(0.90 * len(results))]:.1f} ms")
print(f"P95:    {results[int(0.95 * len(results))]:.1f} ms")
print(f"P99:    {results[int(0.99 * len(results))]:.1f} ms")
print(f"Max:    {max(results):.1f} ms")

# Save to CSV
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Request", "Latency_ms"])
    for idx, val in enumerate(results):
        writer.writerow([idx+1, round(val, 2)])

print("\nSaved to results.csv")