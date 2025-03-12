from celery import Celery
from messagine import send_to_next_service
from config import CELERY_BROKER_URL, PROPERTY_QUEUE, NOTIFICATION_QUEUE

# Initialisation de Celery
celery = Celery("credit_service", broker=CELERY_BROKER_URL, backend="rpc://")

# Configurer Celery pour écouter la bonne queue
celery.conf.task_queues = {
    "credit_queue": {"exchange": "default", "routing_key": "credit_queue"}
}
celery.conf.task_routes = {
    "tasks.evaluate_credit": {"queue": "credit_queue"}
}

@celery.task(name="tasks.evaluate_credit")
def evaluate_credit(loan_data):
    """ Tâche Celery pour vérifier la solvabilité du client """
    
    client_id = loan_data["client_id"]
    revenu_annuel = loan_data["revenu_annuel"]
    credits_en_cours = loan_data["credits_en_cours"]
    montant_demande = loan_data["montant_demande"]
    
    # Simuler un score de crédit (ex. appel à une base externe)
    credit_score = 720  # Valeur simulée
    taux_endettement = ((montant_demande / (loan_data["duree"] * 12)) + credits_en_cours) / (revenu_annuel / 12) * 100
    
    print(f"📊 [Client {client_id}] Score de crédit: {credit_score}, Taux d'endettement: {taux_endettement:.2f}%")

    # Critères de validation
    if credit_score < 650 or taux_endettement > 40:
        decision = "REJETÉ"
        reason = "Score de crédit insuffisant" if credit_score < 650 else "Taux d'endettement trop élevé"
        send_to_next_service(NOTIFICATION_QUEUE, "tasks.send_notification", {
            "client_id": client_id,
            "status": "REJETÉ",
            "reason": reason
            })


        return f"🔴 [Client {client_id}] Rejeté: {reason}"

    # Si validé, envoyer les infos à Property Service
    decision = "APPROUVÉ"
    send_to_next_service(PROPERTY_QUEUE, "tasks.evaluate_property", {
    "client_id": client_id,
    "credit_score": credit_score,
    "taux_endettement": round(taux_endettement, 2),
    "decision_credit": decision,
    "montant_demande": montant_demande
    })


    return f"✅ [Client {client_id}] Crédit approuvé et envoyé au Property Service."
