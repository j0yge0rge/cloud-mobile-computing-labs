# Lab 5 — Local Serverless Computing and Event-Driven Image Processing Pipeline

**Course:** Cloud and Mobile Computing  
**Student Name:** *(Your name here)*

---

## Overview

This lab simulates a serverless, event-driven architecture entirely on your local machine — no AWS, Azure, or GCP required. An image dropped into a local folder triggers an event that flows through a Redis Stream, gets routed to two functions (image resizer + notifier), and produces a resized output image.

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  /data/input/   │────>│  event-source   │────>│  Redis Stream   │
│  (local folder) │     │  watcher.py     │     │     "events"    │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  event-router   │
                                                 │ event_router.py │
                                                 └────────┬────────┘
                                                    /           \
                                                   ▼             ▼
                                        ┌──────────────┐  ┌──────────────┐
                                        │image-resizer │  │   notifier   │
                                        │/resize :5001 │  │/notify :5002 │
                                        └──────┬───────┘  └──────────────┘
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │ /data/output │
                                        │resized_*.png │
                                        └──────────────┘
```

| Concept | Local Implementation |
|---------|---------------------|
| Event source | `watcher.py` — detects new images in `/data/input/` |
| Event bus | Redis Streams |
| Event router | `event_router.py` — reads from Redis, forwards to functions |
| FaaS functions | Containerized Flask services (`image-resizer`, `notifier`) |
| Event fan-out | One event triggers both functions simultaneously |
| Cold start | Observed by restarting a function container |

---

## Project Structure

```
lecture5-local-serverless-lab/
├── docker-compose.yml
├── data/
│   ├── input/               # Drop images here to trigger the pipeline
│   └── output/              # Resized images appear here
├── event_source/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── watcher.py
├── router/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── event_router.py
└── functions/
    ├── image_resizer/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app.py
    └── notifier/
        ├── Dockerfile
        ├── requirements.txt
        └── app.py
```

---

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- No cloud account needed — everything runs locally

---

## How to Run

```bash
# 1. Clone the repo and navigate to this lab
git clone <your-repo-url>
cd Lab_05

# 2. Build and start all services
docker compose up --build

# 3. In a second terminal, create a test image inside the container
docker compose exec image-resizer python - <<'PY'
from PIL import Image, ImageDraw
img = Image.new("RGB", (1200, 800), (240, 240, 240))
draw = ImageDraw.Draw(img)
draw.text((50, 50), "Lecture 5 Local Serverless Lab", fill=(0, 0, 0))
img.save("/data/input/test_image.png")
print("Created /data/input/test_image.png")
PY
```

After a few seconds, check `data/output/` — you should see `resized_test_image.png`.

---

## Testing

### Check running containers
```bash
docker compose ps
```

### Test the image-resizer function directly

**Linux/macOS/Git Bash:**
```bash
curl -X POST http://localhost:5001/resize \
  -H "Content-Type: application/json" \
  -d '{"file_path":"/data/input/test_image.png","file_name":"test_image.png","width":200}'
```

**Windows PowerShell:**
```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:5001/resize `
  -ContentType "application/json" `
  -Body '{"file_path":"/data/input/test_image.png","file_name":"test_image.png","width":200}'
```

### Check logs
```bash
docker compose logs event-source    # shows published events
docker compose logs event-router    # shows routing decisions
docker compose logs image-resizer   # shows resize results
docker compose logs notifier        # shows notification logs
```

---

## Cold Start Experiment

```bash
# 1. Send a warm request and record the time
curl -w "\nTotal time: %{time_total}s\n" -X POST http://localhost:5001/resize \
  -H "Content-Type: application/json" \
  -d '{"file_path":"/data/input/test_image.png","file_name":"test_image.png","width":200}'

# 2. Restart the function container
docker compose restart image-resizer

# 3. Immediately send the same request and record the time
curl -w "\nTotal time: %{time_total}s\n" -X POST http://localhost:5001/resize \
  -H "Content-Type: application/json" \
  -d '{"file_path":"/data/input/test_image.png","file_name":"test_image.png","width":200}'
```

| Measurement | Value |
|-------------|-------|
| Warm request time | *(fill in)* |
| First request after restart | *(fill in)* |
| Difference | *(fill in)* |
| Explanation | *(fill in)* |

---

## Teardown

```bash
docker compose down

# Remove output images (Linux/macOS)
rm -rf data/output/*

# Remove output images (Windows PowerShell)
Remove-Item data/output/* -Force
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Port already in use | Another app uses 5001, 5002, or 6379 | Stop the other service or change the port in `docker-compose.yml` |
| No output image | Event not detected or router not running | Check `docker compose logs event-source` and `event-router` |
| Function returns "file does not exist" | Wrong file path | Use `/data/input/test_image.png` not a Windows local path |
| Image not re-triggering | File already processed by watcher | Rename the image or restart `event-source` |
| `curl` not working on PowerShell | PowerShell aliases curl differently | Use `Invoke-RestMethod` instead |

---

## Reflection

See `reflection.md` for answers to the discussion questions:
1. What is the event source in this lab?
2. What is the event router?
3. What are the event destinations?
4. Why is this pipeline loosely coupled?
5. What happened after restarting the image-resizer container?
6. How is this similar to serverless cold start?
7. What is missing compared with real cloud serverless platforms?
8. How could this pipeline be extended (e.g. OCR, image moderation, ML enrichment)?
