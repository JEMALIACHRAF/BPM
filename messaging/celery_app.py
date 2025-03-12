from celery import Celery

CELERY_BROKER_URL = "pyamqp://guest@rabbitmq//"
CELERY_RESULT_BACKEND = "rpc://"


celery = Celery(
    "bpm-loan-evaluation",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)
Celery.conf.broker_connection_retry_on_startup = True

# Définition des routes des tâches pour chaque service
celery.conf.task_routes = {
    "loan_service.tasks.process_loan_request": {"queue": "loan_queue"},
    "credit_service.tasks.evaluate_credit": {"queue": "credit_queue"},
    "property_service.tasks.evaluate_property": {"queue": "property_queue"},
    "decision_service.tasks.evaluate_loan_decision": {"queue": "decision_queue"},
    "notification_service.tasks.send_notification": {"queue": "notification_queue"},
}

celery.conf.task_default_queue = "default"
