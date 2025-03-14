from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import uuid
import os

app = FastAPI()

@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())
    print(f"Client {client_id} connected")
    await websocket.send_text(f"Welcome Client {client_id} to the FastAPI WebSocket Server!")

    try:
        while True:
            message = await websocket.receive_text()
            print(f"Client {client_id} sent: {message}")
            await websocket.send_text(f"Server received from {client_id}: {message}")
    except Exception:
        print(f"Client {client_id} disconnected")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port
    uvicorn.run(app, host="0.0.0.0", port=port)

'''from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import List

app = FastAPI()

# List to store active connections
active_connections: List[WebSocket] = []
@app.get("/")
async def get():
    return FileResponse("index.html")  # Ensure index.html is in the same folder
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()  # Receive message from client
            print(f"Received: {message}")

            # Send the message to all connected clients
            for connection in active_connections:
                await connection.send_text(f"Server says: {message}")

    except WebSocketDisconnect:
        print("Client disconnected")
        active_connections.remove(websocket)  # Remove disconnected clients
'''
