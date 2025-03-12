from celery import Celery
from messagine import send_to_next_service
from config import CELERY_BROKER_URL, DECISION_QUEUE, NOTIFICATION_QUEUE

# Initialisation de Celery
celery = Celery("property_service", broker=CELERY_BROKER_URL, backend="rpc://")
celery.conf.task_queues = {
    
    "property_queue": {"exchange": "default", "routing_key": "property_queue"}
}

celery.conf.task_routes = {
    "tasks.evaluate_property": {"queue": "property_queue"}
}

@celery.task(name="tasks.evaluate_property")
def evaluate_property(property_data):
    """ Tâche Celery pour vérifier la valeur du bien et le Loan-to-Value (LTV) """
    
    client_id = property_data["client_id"]
    montant_demande = property_data["montant_demande"]
    valeur_bien = property_data["valeur_bien"]
    
    # Calcul du Loan-to-Value (LTV)
    loan_to_value = (montant_demande / valeur_bien) * 100
    
    print(f"🏡 [Client {client_id}] Loan-to-Value: {loan_to_value:.2f}%")

    # Critères de validation
    if loan_to_value > 85:
        decision = "REJETÉ"
        reason = "Loan-to-Value ratio trop élevé (>85%)"
        send_to_next_service(NOTIFICATION_QUEUE, {"client_id": client_id, "status": "REJETÉ", "reason": reason})
        return f"🔴 [Client {client_id}] Rejeté: {reason}"

    # Si validé, envoyer les infos à Decision Service
    decision = "APPROUVÉ"
    send_to_next_service(DECISION_QUEUE, "tasks.make_decision", {
    "client_id": client_id,
    "loan_to_value": round(loan_to_value, 2),
    "evaluation_bien": decision
    })


    return f"✅ [Client {client_id}] Évaluation du bien approuvée et envoyée au Decision Service."
