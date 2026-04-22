# Lab 4 – Microservices and Cloud-Native Design

**Student:** [Your Name Here]  
**Course:** Cloud and Mobile Computing – Dr. Youssef Senousy

---

## Project Structure

```
week4-lab/
├── docker-compose.yml          # Orchestrates both services
├── report.md                   # Reflection report (Part I answers)
├── GitHub_Link.txt             # GitHub repository URL
├── product-service/
│   ├── app.py                  # Flask app: /health and /products/<id>
│   ├── requirements.txt        # flask==3.0.3
│   └── Dockerfile              # Container image for product-service
└── order-service/
    ├── app.py                  # Flask app: /health and /orders (POST)
    ├── requirements.txt        # flask + requests
    └── Dockerfile              # Container image for order-service
```

---

## How to Run

```bash
# From inside the week4-lab folder:
docker compose up --build -d
docker compose ps
```

---

## How to Test

```bash
# Health checks
curl http://localhost:5001/health
curl http://localhost:5002/health

# Product lookup
curl http://localhost:5001/products/1
curl http://localhost:5001/products/99   # should return 404

# Create an order
curl -X POST http://localhost:5002/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

## Failure Simulation

```bash
# Stop product-service and observe 503 from order-service
docker stop product-service

curl -X POST http://localhost:5002/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 2, "quantity": 1}'

# Restart
docker start product-service
```
