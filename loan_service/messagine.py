import pika
import json
from config import RABBITMQ_URL, CREDIT_QUEUE

def send_to_credit_service(loan_data):
    """ Envoie la demande de prêt au Credit Service via RabbitMQ """
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    # 🔹 Vérifie que la queue est déclarée correctement
    channel.queue_declare(queue=CREDIT_QUEUE, durable=True)
    
    # 🔹 Convertir les données en JSON
    message = json.dumps(loan_data)
    
    # 🔹 Envoyer le message à RabbitMQ
    channel.basic_publish(exchange='', routing_key=CREDIT_QUEUE, body=message)

    print(f"📨 Loan request sent to Credit Service: {message}")
    connection.close()
