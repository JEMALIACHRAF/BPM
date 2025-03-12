# RabbitMQ Connection
RABBITMQ_URL = "pyamqp://guest@rabbitmq//"

# Celery Configuration
CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = "rpc://"

# Queues
PROPERTY_QUEUE = "property_queue"
DECISION_QUEUE = "decision_queue"
NOTIFICATION_QUEUE = "notification_queue"

# ✅ Fix for Celery 6.0 Broker Connection Retry Warning
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# ✅ Explicit Queue Configurations
CELERY_TASK_QUEUES = {
    "property_queue": {"exchange": "default", "routing_key": "property_queue"},
    "decision_queue": {"exchange": "default", "routing_key": "decision_queue"},
    "notification_queue": {"exchange": "default", "routing_key": "notification_queue"},
}

# ✅ Default Queue
CELERY_TASK_DEFAULT_QUEUE = "property_queue"
