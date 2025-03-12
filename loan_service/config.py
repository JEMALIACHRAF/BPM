# RabbitMQ Connection
RABBITMQ_URL = "pyamqp://guest@rabbitmq//"

# Celery Configuration
CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = "rpc://"

# Queues
CREDIT_QUEUE = "credit_queue"
LOAN_QUEUE = "loan_queue"

# ✅ Fix for Celery 6.0 Broker Connection Retry Warning
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# ✅ Explicit Queue Configurations
CELERY_TASK_QUEUES = {
    "loan_queue": {"exchange": "default", "routing_key": "loan_queue"},
    "credit_queue": {"exchange": "default", "routing_key": "credit_queue"},
}

# ✅ Default Queue
CELERY_TASK_DEFAULT_QUEUE = "loan_queue"
