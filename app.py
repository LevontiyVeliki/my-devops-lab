from flask import Flask
import random
import time
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import logging

app = Flask(__name__)

# Метрики Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.route('/')
def hello():
    start = time.time()
    REQUEST_COUNT.inc()
    time.sleep(random.uniform(0.1, 0.5))
    end = time.time()
    REQUEST_LATENCY.observe(end - start)
    return "Приложение работает! Перейди на /metrics для Prometheus."

@app.route('/crash')
def crash():
    # Искусственная ошибка
    raise Exception("Искусственная ошибка для тестирования мониторинга!")

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)
