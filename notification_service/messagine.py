from celery import Celery
from config import CELERY_BROKER_URL

celery = Celery("notification_service", broker=CELERY_BROKER_URL, backend="rpc://")

@celery.task(name="tasks.send_notification")
def send_notification(notification_data):
    """ Tâche Celery pour envoyer la notification au client """
    
    client_id = notification_data["client_id"]
    status = notification_data["status"]
    reason = notification_data.get("reason", "Aucune raison précisée")
    montant = notification_data.get("montant_demande", 0)

    print(f"📢 Notification envoyée : Client {client_id} - {status}")

