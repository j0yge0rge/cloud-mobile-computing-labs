from flask import Flask, jsonify

app = Flask(__name__)

# In-memory product catalog (stateless - no database needed)
PRODUCTS = {
    1: {"id": 1, "name": "Laptop", "price": 1200},
    2: {"id": 2, "name": "Phone", "price": 650},
    3: {"id": 3, "name": "Headphones", "price": 120}
}

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint used by Docker Compose and orchestrators."""
    return jsonify({"service": "product-service", "status": "up"}), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Return a product by ID, or 404 if not found."""
    product = PRODUCTS.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
