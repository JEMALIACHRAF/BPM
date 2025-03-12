from celery import Celery
from messagine import send_to_next_service
from config import CELERY_BROKER_URL, NOTIFICATION_QUEUE

# Initialisation de Celery
celery = Celery("decision_service", broker=CELERY_BROKER_URL, backend="rpc://")
celery.conf.task_queues = {
    "decision_queue": {"exchange": "default", "routing_key": "decision_queue"}
}
celery.conf.task_routes = {
    "tasks.make_decision": {"queue": "decision_queue"}
}

@celery.task
def evaluate_loan_decision(decision_data):
    """ Tâche Celery pour prendre la décision finale du prêt """
    
    client_id = decision_data["client_id"]
    credit_score = decision_data["credit_score"]
    taux_endettement = decision_data["taux_endettement"]
    loan_to_value = decision_data["loan_to_value"]
    montant_demande = decision_data["montant_demande"]

    print(f"📝 [Client {client_id}] Analyse de la décision en cours...")

    # Critères de validation
    if credit_score < 650:
        decision = "REJETÉ"
        reason = "Score de crédit trop bas"
    elif taux_endettement > 40:
        decision = "REJETÉ"
        reason = "Taux d'endettement trop élevé"
    elif loan_to_value > 85:
        decision = "REJETÉ"
        reason = "Loan-to-Value trop élevé"
    else:
        decision = "APPROUVÉ"
        reason = "Tous les critères sont satisfaits"

    # Envoi au Notification Service
    send_to_next_service(NOTIFICATION_QUEUE, "tasks.send_notification", {
    "client_id": client_id,
    "status": decision,
    "reason": reason,
    "montant_demande": montant_demande
    })
    return f"✅ [Client {client_id}] Décision prise: {decision} ({reason})"
