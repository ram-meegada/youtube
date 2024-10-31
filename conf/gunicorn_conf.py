bind = '127.0.0.1:8000'  # Bind to localhost on port 8000
workers = 3               # Number of worker processes
worker_class = 'sync'     # Type of worker (sync, gevent, eventlet, etc.)
timeout = 30              # Workers silent for more than this many seconds are killed and restarted
loglevel = 'info'         # Logging level (debug, info, warning, error, critical)
accesslog = '-'           # Access log file, '-' means stdout
errorlog = '-'   
