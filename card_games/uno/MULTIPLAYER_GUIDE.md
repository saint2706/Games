# Uno Online Multiplayer Architecture Guide

## Overview

This document outlines the architecture and implementation strategy for adding online multiplayer capability to the Uno game. The design follows a client-server model with support for real-time gameplay.

## Architecture Components

### 1. Network Protocol

The multiplayer system uses a message-based protocol over WebSockets for real-time communication.

#### Message Types

- **CONNECT**: Client connects to server
- **JOIN_GAME**: Player joins a game lobby
- **START_GAME**: Host starts the game
- **PLAY_CARD**: Player plays a card
- **DRAW_CARD**: Player draws a card
- **CHOOSE_COLOR**: Player chooses color after wild
- **CALL_UNO**: Player declares UNO
- **CHALLENGE**: Player challenges a +4
- **GAME_STATE**: Server broadcasts current game state
- **PLAYER_ACTION**: Server broadcasts player actions
- **DISCONNECT**: Player leaves the game

#### Message Format

```python
{
    "type": "PLAY_CARD",
    "player_id": "uuid-string",
    "game_id": "game-uuid",
    "data": {
        "card_index": 3,
        "declare_uno": true,
        "chosen_color": "red"  # optional
    },
    "timestamp": 1234567890
}
```

### 2. Server Architecture

#### Components

1. **Game Server**
   - Manages multiple game instances
   - Routes messages between clients
   - Enforces game rules
   - Handles disconnections and reconnections

2. **Lobby System**
   - Create/join game lobbies
   - Player matchmaking
   - Game configuration (house rules, player count)

3. **Authentication** (optional)
   - User accounts
   - Session management
   - Player statistics

#### Technology Stack Options

- **WebSocket Server**: `websockets` library or `socket.io`
- **Web Framework**: Flask or FastAPI for REST endpoints
- **Database**: SQLite for simple games, PostgreSQL for production
- **Serialization**: JSON for messages

### 3. Client Architecture

#### Network Interface

Create a new `NetworkUnoInterface` class that implements `UnoInterface`:

```python
class NetworkUnoInterface(UnoInterface):
    """Interface for networked multiplayer games."""
    
    def __init__(self, websocket_url: str, player_id: str):
        self.ws = connect_to_server(websocket_url)
        self.player_id = player_id
        self.game_state_queue = Queue()
    
    def choose_action(self, game, player, playable, penalty_active):
        # Get player's decision
        decision = self._get_local_decision(game, player, playable, penalty_active)
        
        # Send to server
        self._send_action(decision)
        
        # Wait for server confirmation
        return self._wait_for_confirmation()
    
    def update_status(self, game):
        # Receive game state from server
        state = self._receive_game_state()
        self._apply_state(game, state)
```

#### Client-Side Prediction

To reduce latency, implement client-side prediction:
- Show card play immediately
- Roll back if server rejects the action

### 4. Synchronization

#### State Management

- Server is authoritative for game state
- Clients send actions, not state changes
- Server validates and broadcasts state updates

#### Handling Latency

- Buffer actions during network delays
- Show "waiting for player" indicators
- Implement turn timers

#### Disconnection Handling

- Save game state periodically
- Allow reconnection within timeout window
- Bot takes over for disconnected player option

## Implementation Steps

### Phase 1: Local Multiplayer Testing
1. Refactor `UnoGame` to support networked interface
2. Add event serialization/deserialization
3. Create mock network interface for testing

### Phase 2: Server Development
1. Implement WebSocket server
2. Create lobby system
3. Add game state management
4. Implement message routing

### Phase 3: Client Integration
1. Create `NetworkUnoInterface`
2. Add connection management
3. Implement state synchronization
4. Add reconnection logic

### Phase 4: Features & Polish
1. Add chat functionality
2. Implement spectator mode
3. Add player statistics
4. Create leaderboard system

## Example Server Code (Pseudocode)

```python
# server.py
import asyncio
import websockets
import json
from typing import Dict, Set
from uno import UnoGame, build_players

class GameServer:
    def __init__(self):
        self.games: Dict[str, UnoGame] = {}
        self.lobbies: Dict[str, Set[str]] = {}
        self.connections: Dict[str, websockets.WebSocketServerProtocol] = {}
    
    async def handle_client(self, websocket, path):
        player_id = await self.authenticate(websocket)
        self.connections[player_id] = websocket
        
        try:
            async for message in websocket:
                await self.handle_message(player_id, json.loads(message))
        finally:
            await self.handle_disconnect(player_id)
    
    async def handle_message(self, player_id: str, message: dict):
        msg_type = message["type"]
        
        if msg_type == "JOIN_GAME":
            await self.join_game(player_id, message["game_id"])
        elif msg_type == "PLAY_CARD":
            await self.play_card(player_id, message)
        # ... handle other message types
    
    async def broadcast_state(self, game_id: str):
        game = self.games[game_id]
        state = self.serialize_game_state(game)
        
        for player_id in game.player_ids:
            if player_id in self.connections:
                await self.connections[player_id].send(
                    json.dumps({"type": "GAME_STATE", "data": state})
                )

# Run server
async def main():
    server = GameServer()
    async with websockets.serve(server.handle_client, "localhost", 8765):
        await asyncio.Future()  # Run forever

asyncio.run(main())
```

## Example Client Code (Pseudocode)

```python
# client.py
import asyncio
import websockets
import json

class UnoClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.ws = None
        self.player_id = None
    
    async def connect(self):
        self.ws = await websockets.connect(self.server_url)
        response = await self.ws.recv()
        self.player_id = json.loads(response)["player_id"]
    
    async def join_game(self, game_id: str):
        await self.ws.send(json.dumps({
            "type": "JOIN_GAME",
            "player_id": self.player_id,
            "game_id": game_id
        }))
    
    async def play_card(self, card_index: int, declare_uno: bool = False):
        await self.ws.send(json.dumps({
            "type": "PLAY_CARD",
            "player_id": self.player_id,
            "data": {
                "card_index": card_index,
                "declare_uno": declare_uno
            }
        }))
    
    async def receive_updates(self):
        async for message in self.ws:
            data = json.loads(message)
            if data["type"] == "GAME_STATE":
                self.update_game_state(data["data"])
            elif data["type"] == "PLAYER_ACTION":
                self.show_player_action(data["data"])
```

## Security Considerations

1. **Input Validation**: Validate all client actions server-side
2. **Rate Limiting**: Prevent message spam
3. **Cheat Prevention**: Server validates all moves
4. **Authentication**: Use tokens or session IDs
5. **Encryption**: Use WSS (WebSocket Secure) for production

## Testing Strategy

1. **Unit Tests**: Test message serialization/deserialization
2. **Integration Tests**: Test client-server communication
3. **Load Tests**: Test with multiple concurrent games
4. **Latency Tests**: Simulate network delays
5. **Disconnection Tests**: Test reconnection logic

## Future Enhancements

- Voice chat integration
- Replay system
- Tournament mode
- Cross-platform mobile clients
- Regional matchmaking
- ELO rating system
- Achievements and rewards
