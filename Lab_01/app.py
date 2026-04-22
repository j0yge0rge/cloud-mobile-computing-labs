from flask import Flask
import time, random

app = Flask(__name__)

@app.route('/')
def hello():
    delay = random.expovariate(1/0.1)
    time.sleep(delay)
    return f"Response after {delay:.2f} seconds"

app.run(host='0.0.0.0', port=5000)