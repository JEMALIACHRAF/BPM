import os
# RabbitMQ Connection
RABBITMQ_URL = "pyamqp://guest@rabbitmq//"

# Celery Configuration
CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = "rpc://"

# Queues
NOTIFICATION_QUEUE = "notification_queue"

# Keep the existing broker retry setting
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# 🔹 NEW: Increase the number of retries (default is low)
CELERY_BROKER_CONNECTION_MAX_RETRIES = 100  

# 🔹 NEW: Increase delay between retries (default is too fast)
CELERY_BROKER_CONNECTION_RETRY_DELAY = 5.0  # 5 seconds between retries


#  Explicit Queue Configurations
CELERY_TASK_QUEUES = {
    "notification_queue": {"exchange": "default", "routing_key": "notification_queue"},
}

# ✅ Default Queue
CELERY_TASK_DEFAULT_QUEUE = "notification_queue"

