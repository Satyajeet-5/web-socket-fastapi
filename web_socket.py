from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
