## ADDED Requirements

### Requirement: User can create a workspace
The system SHALL allow authenticated users to create a new workspace. The creating user SHALL become the workspace owner.

#### Scenario: Successful workspace creation
- **WHEN** authenticated user submits workspace name
- **THEN** system creates workspace with user as owner and returns workspace details

#### Scenario: Creating workspace with duplicate name
- **WHEN** user creates workspace with same name as existing workspace
- **THEN** system creates workspace (duplicate names allowed)

### Requirement: User can list their workspaces
The system SHALL return a list of workspaces where the user is a member.

#### Scenario: User has multiple workspaces
- **WHEN** user requests their workspace list
- **THEN** system returns all workspaces the user belongs to with role information

#### Scenario: User has no workspaces
- **WHEN** user requests their workspace list
- **THEN** system returns empty list

### Requirement: User can join a workspace
The system SHALL allow users to join an existing workspace as a member.

#### Scenario: Successfully join workspace
- **WHEN** authenticated user requests to join a workspace
- **THEN** system adds user as member and returns updated workspace

#### Scenario: User already member
- **WHEN** user requests to join a workspace they already belong to
- **THEN** system returns existing membership (idempotent)

### Requirement: User can leave a workspace
The system SHALL allow users to leave a workspace they belong to.

#### Scenario: Successfully leave workspace
- **WHEN** authenticated user requests to leave a workspace
- **THEN** system removes user from workspace members

#### Scenario: Owner cannot leave workspace
- **WHEN** workspace owner requests to leave their workspace
- **THEN** system returns error indicating owner cannot leave

### Requirement: Workspace owner can remove members
The system SHALL allow workspace owners to remove other members from their workspace.

#### Scenario: Owner removes member
- **WHEN** workspace owner requests to remove a member
- **THEN** system removes the member from workspace

#### Scenario: Non-owner cannot remove members
- **WHEN** non-owner member requests to remove another member
- **THEN** system returns forbidden error

### Requirement: User can view workspace details
The system SHALL return workspace details including member count.

#### Scenario: View workspace details
- **WHEN** workspace member requests workspace details
- **THEN** system returns workspace information

### Requirement: Workspace owner can update workspace
The system SHALL allow workspace owners to update workspace name and description.

#### Scenario: Update workspace name
- **WHEN** owner updates workspace name
- **THEN** system returns updated workspace

### Requirement: Workspace owner can delete workspace
The system SHALL allow workspace owners to delete their workspace.

#### Scenario: Delete workspace
- **WHEN** owner deletes workspace
- **THEN** system deletes workspace and all memberships
