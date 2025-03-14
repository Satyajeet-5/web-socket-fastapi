from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import uuid  # For generating unique client IDs

app = FastAPI()

# Step 1: Serve the HTML file
@app.get("/")
async def get():
    return HTMLResponse(open("index.html").read())

# Step 2-9: WebSocket Connection Handling
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = str(uuid.uuid4())  # Generate a unique ID for the client
    print(f"Client {client_id} connected")  # Step 3: Server accepts connection
    await websocket.send_text(f"Welcome Client {client_id} to the FastAPI WebSocket Server!")  # Step 4: Server sends response

    try:
        while True:
            message = await websocket.receive_text()  # Step 5: Server receives message
            print(f"Client {client_id} sent: {message}")  # Print message with client ID
            await websocket.send_text(f"Server received from {client_id}: {message}")  # Step 7: Server sends response
    except Exception:
        print(f"Client {client_id} disconnected")  # Step 9: Server handles disconnection

# Step 10: Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

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
