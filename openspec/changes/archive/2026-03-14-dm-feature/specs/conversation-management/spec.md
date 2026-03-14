# Conversation Management

## ADDED Requirements

### Requirement: System creates conversation automatically

The system SHALL automatically create a conversation when users first message each other.

#### Scenario: First message creates conversation
- **WHEN** User A sends first message to User B
- **AND** no conversation exists between them
- **THEN** the system creates a conversation record
- **AND** links the message to that conversation

### Requirement: User can view their conversation list

The system SHALL display all DM conversations for a user.

#### Scenario: List all conversations
- **WHEN** a user requests their conversation list
- **THEN** the system returns all conversations the user participates in
- **AND** includes last message preview and timestamp

#### Scenario: Conversations ordered by recent activity
- **WHEN** a user views their conversation list
- **THEN** conversations are sorted by updated_at (most recent first)

### Requirement: Conversation shows other participant info

The system SHALL display conversation details including the other user.

#### Scenario: View conversation details
- **WHEN** a user views a specific conversation
- **THEN** the system returns conversation with other user's info
- **AND** includes username, avatar (if any)

### Requirement: System prevents duplicate conversations

The system SHALL ensure users have only one conversation with each other.

#### Scenario: Same conversation returned
- **WHEN** User A messages User B multiple times
- **THEN** all messages are linked to the same conversation
- **AND** the conversation list shows single entry

### Requirement: Conversation updates on new message

The system SHALL update conversation timestamp when new messages are sent.

#### Scenario: Conversation timestamp updates
- **WHEN** a new message is sent in a conversation
- **THEN** the conversation's updated_at is set to message time
- **AND** conversation moves to top of list
