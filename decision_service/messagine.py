from celery import Celery
from config import CELERY_BROKER_URL

celery = Celery("decision_service", broker=CELERY_BROKER_URL, backend="rpc://")

def send_to_next_service(queue_name, task_name, message_data):
    """ Envoie les résultats via Celery en spécifiant la tâche correcte """
    celery.send_task(task_name, args=[message_data], queue=queue_name)
