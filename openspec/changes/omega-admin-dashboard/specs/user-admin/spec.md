## ADDED Requirements

### Requirement: Admin can view user list
The system SHALL allow administrators to view a paginated list of all users.

#### Scenario: View user list
- **WHEN** admin navigates to `/admin/users`
- **THEN** system displays a table with user id, username, email, is_active, is_superuser

#### Scenario: View user list with pagination
- **WHEN** admin views user list
- **THEN** system returns paginated results (default 20 per page)

### Requirement: Admin can view user details
The system SHALL allow administrators to view detailed information of a specific user.

#### Scenario: View single user
- **WHEN** admin clicks on a user row
- **THEN** system displays user details (id, username, email, full_name, is_active, is_superuser, created_at)

### Requirement: Admin can create new user
The system SHALL allow administrators to create new user accounts.

#### Scenario: Create user with valid data
- **WHEN** admin fills in username, email, password and clicks "Create"
- **THEN** system creates the user and displays success message

#### Scenario: Create user with duplicate email
- **WHEN** admin attempts to create user with existing email
- **THEN** system displays error "Email already registered"

### Requirement: Admin can update existing user
The system SHALL allow administrators to update user information.

#### Scenario: Update user fields
- **WHEN** admin modifies user fields and clicks "Save"
- **THEN** system updates the user and displays success message

#### Scenario: Toggle user active status
- **WHEN** admin toggles is_active switch
- **THEN** system updates user active status immediately

### Requirement: Admin can delete user
The system SHALL allow administrators to delete user accounts.

#### Scenario: Delete user with confirmation
- **WHEN** admin clicks delete and confirms
- **THEN** system permanently removes the user from database

### Requirement: Only superuser can access admin panel
The system SHALL restrict admin panel access to users with is_superuser=True.

#### Scenario: Non-superuser attempts to access admin
- **WHEN** non-superuser user visits `/admin`
- **THEN** system returns 403 Forbidden

#### Scenario: Superuser accesses admin
- **WHEN** superuser user visits `/admin`
- **THEN** system displays admin panel
