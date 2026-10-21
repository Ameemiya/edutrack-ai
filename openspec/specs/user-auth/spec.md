# user-auth Specification

## Purpose
Enables students and educators to register accounts, authenticate securely, and manage their profiles in EduTrack AI using Xano authentication endpoints.

## Requirements

### Requirement: User Registration (Signup)
The system SHALL allow new users to register by submitting their name, email address, and password to the `auth/signup` endpoint.

#### Scenario: Successful user registration
- **WHEN** a user submits a valid name, an unused email address, and a password
- **THEN** the system registers the user in the `user` table and receives an authentication token

#### Scenario: Registration rejected for duplicate email
- **WHEN** a user attempts to sign up with an email address already registered
- **THEN** the system displays a clear error indicating the account already exists

### Requirement: User Authentication (Login)
The system SHALL authenticate existing users via the `auth/login` endpoint using their email and password credentials.

#### Scenario: Successful login
- **WHEN** a user submits valid registered email and password credentials
- **THEN** the system authenticates the user, obtains an auth token, and initializes the authenticated session

#### Scenario: Failed login with invalid credentials
- **WHEN** a user submits incorrect email or password credentials
- **THEN** the system rejects authentication and displays an invalid credentials error

### Requirement: Profile Information Retrieval (Auth Me)
The system SHALL retrieve and display authenticated user profile data from the `auth/me` endpoint using the active session auth token.

#### Scenario: View authenticated profile
- **WHEN** an authenticated user visits `pages/3_👤_Perfil.py`
- **THEN** the system displays the user's name, email, user ID, and registration date

#### Scenario: User logout
- **WHEN** an authenticated user clicks the logout button
- **THEN** the system clears the session token and displays the login/signup interface

### Requirement: Environment Configuration
The system SHALL load the base endpoint URL for authentication from a `.env` file located at the project root.

#### Scenario: Load URL from .env
- **WHEN** the authentication service initializes
- **THEN** it reads the Xano base authentication API URL from the root `.env` file
