## Why

Students using EduTrack AI need a structured way to register, organize, and manage academic obligations such as homework, exams, and projects associated with their enrolled subjects. Defining a dedicated `academic_tasks` database table enables persistent storage and relational mapping to subjects.

## What Changes

- Define the schema for the `academic_tasks` table in XanoScript (`table/academic_tasks.xs`).
- Specify required and optional fields:
  - `id` (int, auto-increment primary key)
  - `created_at` (timestamp, private)
  - `title` (text, task title)
  - `description` (text, task details/instructions)
  - `due_date` (date, deadline for task completion)
  - `status` (text, status of task such as pending, in_progress, completed)
  - `subject_id` (int, foreign key referencing the `subjects` table)
  - `user_id` (int, foreign key referencing the authenticated `users` table)
- Follow strict task scoping per `AGENTS.md` by restricting this change to table schema definition, omitting unrequested APIs, frontend changes, or tests.

## Capabilities

### New Capabilities
- `academic-tasks`: Defines data model and storage schema for student academic obligations linked to specific subjects.

### Modified Capabilities
*(None)*

## Impact

- **Backend**: Adds `table/academic_tasks.xs` in XanoScript.
- **Data Model**: Introduces foreign key relationships linking academic tasks to `subjects` (`subject_id`) and `users` (`user_id`).

