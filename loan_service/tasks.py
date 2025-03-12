from celery import Celery
from config import CELERY_BROKER_URL, CREDIT_QUEUE

celery = Celery("loan_service", broker=CELERY_BROKER_URL, backend="rpc://")
celery.conf.task_queues = {
    "loan_queue": {"exchange": "default", "routing_key": "loan_queue"},
}

# 🔹 Explicitly link tasks to the correct queue
celery.conf.task_routes = {
    "tasks.process_loan_request": {"queue": "loan_queue"}
}

@celery.task(name="tasks.process_loan_request")
def process_loan_request(loan_data):
    """ Tâche Celery pour envoyer la demande de prêt au Credit Service via Celery """
    celery.send_task("tasks.evaluate_credit", args=[loan_data], queue="credit_queue")  # ✅ Use Celery instead of RabbitMQ directly
