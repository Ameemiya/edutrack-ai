# api-crud Specification

## Purpose

Provides secure, authenticated CRUD API endpoints for subjects and academic tasks, enforcing multi-tenant isolation so users can only access their own records.

## Requirements

### Requirement: Subjects CRUD Operations
The system SHALL provide authenticated RESTful endpoints (`GET /subjects`, `POST /subjects`, `PATCH /subjects/{subjects_id}`, `DELETE /subjects/{subjects_id}`) to manage subjects scoped to the authenticated user.

#### Scenario: List subjects scoped to user
- **WHEN** an authenticated user calls `GET /subjects`
- **THEN** the system returns only subjects where `user_id` equals the authenticated user ID

#### Scenario: Create subject with user ownership
- **WHEN** an authenticated user submits subject information to `POST /subjects`
- **THEN** the system creates the subject record automatically bound to the authenticated user ID

#### Scenario: Update own subject
- **WHEN** an authenticated user sends updated details to `PATCH /subjects/{subjects_id}` for a subject they own
- **THEN** the system updates the record and returns the updated subject data

#### Scenario: Delete own subject
- **WHEN** an authenticated user requests `DELETE /subjects/{subjects_id}` for a subject they own
- **THEN** the system removes the subject record

### Requirement: Academic Tasks CRUD Operations
The system SHALL provide authenticated RESTful endpoints (`GET /academic_tasks`, `POST /academic_tasks`, `PATCH /academic_tasks/{academic_tasks_id}`, `DELETE /academic_tasks/{academic_tasks_id}`) to manage academic tasks scoped to the authenticated user.

#### Scenario: List academic tasks scoped to user
- **WHEN** an authenticated user calls `GET /academic_tasks`
- **THEN** the system returns only tasks where `user_id` equals the authenticated user ID

#### Scenario: Create academic task with user ownership
- **WHEN** an authenticated user submits task details to `POST /academic_tasks`
- **THEN** the system creates the task record automatically bound to the authenticated user ID and associated subject

#### Scenario: Update own academic task
- **WHEN** an authenticated user sends updated details to `PATCH /academic_tasks/{academic_tasks_id}` for a task they own
- **THEN** the system updates the record and returns the updated task data

#### Scenario: Delete own academic task
- **WHEN** an authenticated user requests `DELETE /academic_tasks/{academic_tasks_id}` for a task they own
- **THEN** the system removes the academic task record

### Requirement: User Isolation and Access Control
The system SHALL enforce user isolation across all CRUD queries and mutations, preventing access to records owned by other users.

#### Scenario: Unauthenticated request rejected
- **WHEN** a request is made to any CRUD endpoint without a valid authentication token
- **THEN** the system rejects the request with an unauthorized error

#### Scenario: Accessing another user's record is blocked
- **WHEN** an authenticated user attempts to access, modify, or delete a record with a different `user_id`
- **THEN** the system SHALL reject the operation without modifying or exposing the record

