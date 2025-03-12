from fastapi import FastAPI, WebSocket, WebSocketDisconnect  # ✅ Fixed import
from fastapi.staticfiles import StaticFiles
import asyncio
import os

# ✅ Get the absolute path to the "static" directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ✅ Ensure the "static" directory exists
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app = FastAPI(title="Notification Service API")

# ✅ Correct way to mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Store active WebSocket connections
connected_clients = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """ 🚀 WebSocket for real-time notifications """

    await websocket.accept()
    connected_clients[client_id] = websocket  # ✅ Store the client
    print(f"📡 Client {client_id} connected")

    try:
        while True:
            # ✅ Keep the WebSocket alive by receiving messages
            message = await websocket.receive_text()
            print(f"📩 Received from client {client_id}: {message}")
    except WebSocketDisconnect:  # ✅ Fix: WebSocketDisconnect is now imported
        print(f"🔌 Client {client_id} disconnected")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        # ✅ Ensure client is removed when disconnected
        connected_clients.pop(client_id, None)

@app.get("/")
def read_root():
    return {"message": "✅ Notification Service is running"}
