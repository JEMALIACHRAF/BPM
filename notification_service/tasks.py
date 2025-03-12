from celery import Celery
import json
import websockets
import asyncio
from config import CELERY_BROKER_URL
import threading

# ✅ Initialize Celery
celery = Celery("notification_service", broker=CELERY_BROKER_URL, backend="rpc://")

# ✅ Configure Celery Task Queue
celery.conf.task_queues = {
    "notification_queue": {"exchange": "default", "routing_key": "notification_queue"},
}
celery.conf.task_routes = {
    "tasks.send_notification": {"queue": "notification_queue"}
}

# ✅ Create an async event loop in a separate thread
loop = asyncio.new_event_loop()

def start_async_loop():
    """Runs the asyncio event loop in a separate thread."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

# ✅ Start the event loop thread only once
asyncio_thread = threading.Thread(target=start_async_loop, daemon=True)
asyncio_thread.start()

@celery.task(name="tasks.send_notification")
def send_notification(notification_data):
    """ 🚀 Celery task to send a WebSocket notification to the client """

    client_id = notification_data["client_id"]
    status = notification_data["status"]
    reason = notification_data.get("reason", "Aucune raison précisée")
    montant = notification_data.get("montant_demande", 0)

    print(f"📢 Notification envoyée : Client {client_id} - {status}")

    # ✅ Submit WebSocket coroutine to the running asyncio event loop
    future = asyncio.run_coroutine_threadsafe(
        send_websocket_notification(client_id, status, reason, montant), loop
    )
    future.result()  # ✅ Wait for completion before continuing

async def send_websocket_notification(client_id, status, reason, montant):
    """ 📡 Sends a real-time notification via WebSocket """

    uri = f"ws://notification_service:8005/ws/{client_id}"  # ✅ Ensure it points to the correct service
    message = json.dumps({"status": status, "reason": reason, "montant": montant})

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            print(f"📡 WebSocket envoyé au client {client_id}")
    except Exception as e:
        print(f"❌ Erreur WebSocket: {e}")
