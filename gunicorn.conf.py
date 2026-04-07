# Gunicorn configuration for DigitalOcean Basic Droplet (1 vCPU / 1–2 GB RAM)
import multiprocessing

# Server socket
bind = "unix:/run/portfolio/gunicorn.sock"
backlog = 64

# Workers — formula: (2 × CPU cores) + 1
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = "sync"
worker_connections = 100
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/portfolio/gunicorn-access.log"
errorlog  = "/var/log/portfolio/gunicorn-error.log"
loglevel  = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "portfolio"

# Security
forwarded_allow_ips = "127.0.0.1"
secure_scheme_headers = {"X-FORWARDED-PROTO": "https"}

# Graceful timeout
graceful_timeout = 20
