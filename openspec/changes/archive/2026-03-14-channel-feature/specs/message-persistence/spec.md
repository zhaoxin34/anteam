# Message Persistence

## ADDED Requirements

### Requirement: Messages are stored in database

The system SHALL persist all messages to the database.

#### Scenario: Save message to database
- **WHEN** a user sends a message to a channel
- **THEN** the system stores the message in the database
- **AND** returns the saved message with ID and timestamp

#### Scenario: Message includes required fields
- **WHEN** a message is saved
- **THEN** the system stores: channel_id, user_id, content, created_at
- **AND** generates a unique message ID

### Requirement: User can retrieve message history

The system SHALL allow users to retrieve message history for a channel.

#### Scenario: Get channel messages
- **WHEN** a user requests message history for a channel
- **AND** the user is a member of that channel
- **THEN** the system returns messages sorted by created_at (newest first)

#### Scenario: Paginated message history
- **WHEN** a user requests message history with limit/offset
- **THEN** the system returns limited messages
- **AND** includes pagination metadata (has_more, next_offset)

### Requirement: User can edit their own messages

The system SHALL allow message authors to edit their messages.

#### Scenario: Edit message content
- **WHEN** a message author provides new content
- **THEN** the system updates the message content
- **AND** marks the message as edited
- **AND** preserves original timestamp

### Requirement: User can delete their own messages

The system SHALL allow message authors to delete their messages.

#### Scenario: Delete message
- **WHEN** a message author requests to delete the message
- **THEN** the system marks the message as deleted
- **AND** hides the message content (soft delete)

### Requirement: System maintains message integrity

The system SHALL ensure message data integrity.

#### Scenario: Foreign key constraint
- **WHEN** a message references non-existent channel
- **THEN** the system rejects the message with validation error

#### Scenario: Content validation
- **WHEN** a user sends empty message
- **THEN** the system rejects the message with validation error
