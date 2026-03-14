# Message Thread

## ADDED Requirements

### Requirement: User can reply to a message

The system SHALL allow users to reply to existing messages, creating a thread.

#### Scenario: Reply to a message
- **WHEN** a user provides content and parent message ID
- **THEN** the system creates a reply message
- **AND** links it to the parent message via parent_id

#### Scenario: Reply creates thread
- **WHEN** the first reply is created for a message
- **THEN** the system marks the parent message as having a thread
- **AND** the reply appears in the thread view

### Requirement: User can view message thread

The system SHALL allow users to view all replies to a message.

#### Scenario: View thread for a message
- **WHEN** a user requests thread for a message
- **AND** the user is a member of the channel
- **THEN** the system returns all replies to that message
- **AND** orders them chronologically (oldest first)

#### Scenario: Thread shows reply count
- **WHEN** a user views a message with replies
- **THEN** the system displays the reply count
- **AND** shows "X replies" indicator

### Requirement: Thread replies are real-time

The system SHALL push thread replies to connected users.

#### Scenario: Receive reply in real-time
- **WHEN** a user is viewing a thread
- **AND** another user posts a reply
- **THEN** the system pushes the reply to connected users

### Requirement: Thread maintains parent-child relationship

The system SHALL ensure thread relationships are maintained correctly.

#### Scenario: Nested replies
- **WHEN** a user replies to a reply
- **THEN** the system creates a nested reply
- **AND** all replies share the same root ancestor

#### Scenario: Thread replies belong to same channel
- **WHEN** a reply is created
- **THEN** the system ensures reply is in the same channel as parent
