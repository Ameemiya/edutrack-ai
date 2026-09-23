# subjects-table Specification

## Purpose
Defines the database schema for the subjects table in XanoScript, enabling structured storage of academic subjects linked to authenticated users.

## Requirements

### Requirement: Subjects Table Schema Definition
The system SHALL define the schema for the `subjects` table in XanoScript containing `id` as an auto-incrementing primary integer, `name` as text, `teacher` as text, `hours` as integer, and `user_id` as an integer foreign key referencing the `user` table.

#### Scenario: Table schema contains all specified fields
- **WHEN** the `subjects` table schema is evaluated
- **THEN** the schema contains `id` (int), `created_at` (timestamp), `name` (text), `teacher` (text), `hours` (int), and `user_id` (int referencing table "user")

#### Scenario: User relationship configuration
- **WHEN** a record is created in the `subjects` table
- **THEN** the `user_id` field links the subject to the authenticated user record in the Xano user table

### Requirement: Primary and Foreign Key Indexes
The system SHALL define indexes on `subjects` to optimize queries by primary key, creation date, and user reference.

#### Scenario: Table indexes are defined
- **WHEN** the table configuration is compiled
- **THEN** indexes include a primary key on `id`, a btree index on `created_at` (descending), and a btree index on `user_id`
