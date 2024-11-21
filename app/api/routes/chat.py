# app/api/routes/chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import List, Dict, Optional
import json
from app.services.es_rag_service import RAGService
from app.services.azure_llm_service import LLMService

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.rag_service = RAGService()
        self.llm_service = LLMService()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def process_message(self, message: str) -> str:
        """Process incoming message through RAG pipeline."""
        try:
            # Get relevant context
            context = await self.rag_service.get_relevant_context(message)

            # Generate response using LLM
            response = await self.llm_service.generate_response(message, context)

            return json.dumps({
                "status": "success",
                "response": response
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })

    async def broadcast(self, message: str):
        """Broadcast message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for chat functionality."""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                # Parse the message
                message_data = json.loads(data)
                user_message = message_data.get("message", "")

                # Process through RAG pipeline
                response = await manager.process_message(user_message)

                # Send response back to client
                await websocket.send_text(response)

            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": "Invalid JSON format"
                }))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await websocket.send_text(json.dumps({
            "status": "error",
            "message": str(e)
        }))
        manager.disconnect(websocket)


# REST endpoint for chat (alternative to WebSocket)
@router.post("/message")
async def send_message(message: str) -> Dict:
    """REST endpoint for sending chat messages."""
    try:
        response = await manager.process_message(message)
        return json.loads(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Additional endpoints for chat management
@router.get("/active_connections")
async def get_active_connections() -> Dict:
    """Get count of active WebSocket connections."""
    return {
        "active_connections": len(manager.active_connections)
    }
