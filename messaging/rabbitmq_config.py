import pika

RABBITMQ_URL = "pyamqp://guest@rabbitmq//"

def get_rabbitmq_connection():
    """Établit une connexion à RabbitMQ."""
    return pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))

def setup_queues():
    """Crée les files de messages pour chaque service."""
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    queues = [
        "loan_queue",
        "credit_queue",
        "property_queue",
        "decision_queue",
        "notification_queue"
    ]

    for queue in queues:
        channel.queue_declare(queue=queue, durable=True)

    print("✅ RabbitMQ queues configurées.")
    connection.close()
