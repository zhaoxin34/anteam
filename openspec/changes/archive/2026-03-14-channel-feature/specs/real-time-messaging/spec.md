# Real-Time Messaging

## ADDED Requirements

### Requirement: User can connect via WebSocket

The system SHALL allow authenticated users to connect to a WebSocket endpoint for real-time messaging.

#### Scenario: User connects to workspace WebSocket
- **WHEN** an authenticated user connects to /ws/{workspace_id}
- **AND** the user is a member of the workspace
- **THEN** the system establishes a WebSocket connection
- **AND** subscribes the user to the workspace room

#### Scenario: User disconnects from WebSocket
- **WHEN** a user disconnects from the WebSocket
- **THEN** the system removes the user from the workspace room

### Requirement: User can send messages in real-time

The system SHALL allow channel members to send messages via WebSocket.

#### Scenario: Send message to channel
- **WHEN** a channel member sends a message via WebSocket
- **THEN** the system broadcasts the message to all users in that channel
- **AND** the message includes sender info, timestamp, content

#### Scenario: Send message to invalid channel
- **WHEN** a user sends a message to a channel they don't belong to
- **THEN** the system rejects the message with an error

### Requirement: User receives real-time messages

The system SHALL push messages to connected clients in real-time.

#### Scenario: Receive message in channel
- **WHEN** a user is connected to a channel
- **AND** another user sends a message to that channel
- **THEN** the system pushes the message to the connected user

#### Scenario: Receive message notification
- **WHEN** a user is connected but not viewing the channel
- **THEN** the system sends a notification with channel_id and message preview

### Requirement: System handles connection errors

The system SHALL handle WebSocket connection errors gracefully.

#### Scenario: Connection timeout
- **WHEN** WebSocket connection times out
- **THEN** the system closes the connection gracefully
- **AND** logs the disconnection event

#### Scenario: Invalid token
- **WHEN** a user attempts to connect with invalid credentials
- **THEN** the system rejects the connection
- **AND** returns appropriate error code
