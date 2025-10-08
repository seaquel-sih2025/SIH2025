# Gunicorn configuration file for Render deployment - Memory Optimized
import os

bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
workers = 1  # Reduced from 4 to 1 for memory optimization
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 500  # Reduced from 1000
max_requests = 500  # Reduced to prevent memory leaks
max_requests_jitter = 50
timeout = 120  # Increased timeout for startup
keepalive = 2
preload_app = True

# Memory optimization
max_worker_memory = 400 * 1024 * 1024  # 400MB per worker
worker_tmp_dir = "/dev/shm"  # Use shared memory for temp files

# Logging configuration
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "warning"  # Changed from info to warning to reduce log overhead
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(D)s'  # Simplified log format

# Process naming
proc_name = "pravaah-api"

# Graceful shutdown
graceful_timeout = 30