# Direct Messaging

## ADDED Requirements

### Requirement: User can send direct message to another user

The system SHALL allow authenticated users to send private messages to other users.

#### Scenario: Send DM to another user
- **WHEN** a user sends a message to another user
- **AND** a conversation exists between them
- **THEN** the system stores the message
- **AND** delivers it via WebSocket to the recipient

#### Scenario: Start new DM conversation
- **WHEN** a user sends a message to another user with no existing conversation
- **THEN** the system creates a new conversation
- **AND** stores and delivers the message

### Requirement: User can receive direct messages in real-time

The system SHALL push DM messages to connected recipients.

#### Scenario: Receive DM when online
- **WHEN** a user is connected via WebSocket
- **AND** another user sends them a DM
- **THEN** the system pushes the message in real-time

#### Scenario: Receive DM notification when offline
- **WHEN** a user is offline
- **AND** they receive a DM
- **THEN** the message is persisted
- **AND** delivered when they next connect

### Requirement: User can view DM history

The system SHALL allow users to view their DM conversation history.

#### Scenario: Get DM messages
- **WHEN** a user requests messages for a conversation
- **AND** the user is a participant
- **THEN** the system returns all messages in that conversation

#### Scenario: DM messages are chronologically ordered
- **WHEN** a user views DM history
- **THEN** messages are sorted by created_at (newest first)

### Requirement: User can edit their DM

The system SHALL allow message authors to edit DM messages.

#### Scenario: Edit DM
- **WHEN** a DM author edits their message
- **THEN** the system updates the message content
- **AND** marks it as edited

### Requirement: User can delete their DM

The system SHALL allow message authors to delete DM messages.

#### Scenario: Delete DM
- **WHEN** a DM author deletes their message
- **THEN** the system marks the message as deleted
- **AND** hides the content
