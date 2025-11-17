# Gunicorn configuration for long-running AI tasks

# Worker timeout - set to 5 minutes for AI processing
timeout = 300

# Number of workers
workers = 1

# Worker class
worker_class = 'sync'

# Binding
bind = '0.0.0.0:5000'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Graceful timeout
graceful_timeout = 300

# Keep alive
keepalive = 5
