"""WebSocket API routes."""

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from ..db.database import get_session
from ..repository.user_repository import UserRepository
from ..service.auth_service import verify_token

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    """WebSocket connection manager."""

    def __init__(self):
        # workspace_id -> set of WebSockets
        self.active_connections: dict[int, set[WebSocket]] = {}
        # websocket -> user_id
        self.user_connections: dict[WebSocket, int] = {}
        # websocket -> workspace_id
        self.workspace_connections: dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, workspace_id: int, user_id: int):
        """Connect a WebSocket to a workspace room."""
        await websocket.accept()
        if workspace_id not in self.active_connections:
            self.active_connections[workspace_id] = set()
        self.active_connections[workspace_id].add(websocket)
        self.user_connections[websocket] = user_id
        self.workspace_connections[websocket] = workspace_id

    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket."""
        workspace_id = self.workspace_connections.get(websocket)
        if workspace_id and workspace_id in self.active_connections:
            self.active_connections[workspace_id].discard(websocket)
        self.user_connections.pop(websocket, None)
        self.workspace_connections.pop(websocket, None)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket."""
        await websocket.send_text(json.dumps(message))

    async def broadcast_to_workspace(self, message: dict, workspace_id: int, exclude_user: int | None = None):
        """Broadcast a message to all connections in a workspace."""
        if workspace_id not in self.active_connections:
            return
        for connection in self.active_connections[workspace_id].copy():
            user_id = self.user_connections.get(connection)
            if user_id != exclude_user:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception:
                    self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/{workspace_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    workspace_id: int,
    token: str | None = None,
):
    """WebSocket endpoint for real-time messaging in a workspace."""
    # Validate token
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing token")
        return

    token_data = verify_token(token)
    if token_data is None or token_data.username is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return

    # Get user from token
    session = next(get_session())
    repository = UserRepository(session)
    user = repository.get_user_by_username(token_data.username)
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User not found")
        return

    user_id = user.id

    await manager.connect(websocket, workspace_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Handle different message types
            msg_type = message_data.get("type")

            if msg_type == "message":
                # Broadcast message to workspace
                await manager.broadcast_to_workspace(
                    {
                        "type": "message",
                        "channel_id": message_data.get("channel_id"),
                        "user_id": user_id,
                        "content": message_data.get("content"),
                    },
                    workspace_id,
                    exclude_user=user_id,
                )
            elif msg_type == "typing":
                # Broadcast typing indicator
                await manager.broadcast_to_workspace(
                    {
                        "type": "typing",
                        "channel_id": message_data.get("channel_id"),
                        "user_id": user_id,
                    },
                    workspace_id,
                    exclude_user=None,
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
