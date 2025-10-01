# Gunicorn configuration file for Render deployment
import os

bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120  # Increased timeout for startup
keepalive = 2
preload_app = True

# Logging configuration
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "pravaah-api"

# Graceful shutdown
graceful_timeout = 30