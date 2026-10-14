# academic-tasks Specification

## Purpose
Enables students to record and manage academic obligations, homework, exams, and projects linked to subjects in EduTrack AI.

## Requirements

### Requirement: Academic Tasks Table Schema
The system SHALL define the schema for the `academic_tasks` table in XanoScript containing `id` as auto-incrementing primary integer, `title` as text, `description` as text, `due_date` as date, `status` as text, `subject_id` as foreign key referencing `subjects`, and `user_id` as foreign key referencing `users`.

#### Scenario: Table schema contains all specified fields
- **WHEN** the `academic_tasks` table schema is evaluated
- **THEN** the schema contains `id` (int), `created_at` (timestamp), `title` (text), `description` (text), `due_date` (date), `status` (text), `subject_id` (int referencing "subjects"), and `user_id` (int referencing "users")

#### Scenario: Subject relationship configuration
- **WHEN** a task record is linked to a subject via `subject_id`
- **THEN** the system references the corresponding subject record in the `subjects` table

### Requirement: Index Configuration for Performance
The system SHALL configure indexes on `academic_tasks` to optimize filtering by subject, authenticated user, and task deadlines.

#### Scenario: Table indexes are defined
- **WHEN** the table indexes are compiled
- **THEN** indexes include a primary key on `id`, a btree index on `created_at` (descending), a btree index on `subject_id`, a btree index on `user_id`, and a btree index on `due_date`
