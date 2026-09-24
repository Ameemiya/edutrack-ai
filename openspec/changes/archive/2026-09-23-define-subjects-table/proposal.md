## Why

To support academic subject tracking associated with authenticated users in EduTrack AI, a dedicated database table `subjects` is required in Xano with fields for name, teacher, course hours, and a foreign key referencing the authenticated user.

## What Changes

- Define the XanoScript schema for table `subjects` in `tables/subjects.xs`.
- Include fields:
  - `id` (int, auto-increment / primary key)
  - `created_at` (timestamp)
  - `name` (text, subject name)
  - `teacher` (text, teacher name)
  - `hours` (int, course workload hours)
  - `user_id` (int, foreign key referencing the Xano authentication table `user`)
- Per `AGENTS.md`, scope is strictly focused on creating the table definition, without generating CRUD APIs, frontend code, or tests.

## Capabilities

### New Capabilities
- `subjects-table`: Defines the database table schema for `subjects` in XanoScript with fields for identification, subject name, teacher, hours, and user foreign key.

### Modified Capabilities
*(None)*

## Impact

- **Backend**: Adds `tables/subjects.xs` defining the Xano table schema.
- **Dependencies**: References the existing authentication table (`user`).

