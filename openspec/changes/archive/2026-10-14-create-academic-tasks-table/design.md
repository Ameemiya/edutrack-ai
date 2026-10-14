## Context

EduTrack AI organizes student coursework around subjects and tasks. Following the creation of the `subjects` table, students need an `academic_tasks` table to track assignments, tests, and deadlines associated with each subject. Per `AGENTS.md`, the scope of this change is strictly focused on creating the table definition.

## Goals / Non-Goals

**Goals:**
- Define the XanoScript schema for the `academic_tasks` table in `table/academic_tasks.xs`.
- Include requested fields: `title` (text), `description` (text), `due_date` (date), `status` (text), and `subject_id` (foreign key to `subjects`).
- Include standard tracking fields: `id` (int primary), `created_at` (timestamp), and `user_id` (FK to `users`).
- Configure primary and foreign key indexes for query optimization.

**Non-Goals:**
- Creating CRUD APIs (`GET`, `POST`, etc.) - out of scope per `AGENTS.md`.
- Modifying frontend views or creating automated tests - out of scope per `AGENTS.md`.

## Decisions

### 1. File Location and Table Identifier
- **Decision**: Define table `academic_tasks` in `table/academic_tasks.xs`.
- **Rationale**: Aligns with project convention of storing table definitions under the `table/` directory.

### 2. Schema Structure and Field Options
- `id`: integer auto-increment primary key
- `created_at`: timestamp, default `now`, private visibility
- `title`: text with `filters=trim`, required
- `description`: text with `filters=trim`, optional
- `due_date`: date field for deadlines, optional
- `status`: text with default value `"pending"`, optional
- `subject_id`: integer referencing `table = "subjects"`
- `user_id`: integer referencing `table = "users"` to bind records to authenticated users

### 3. Indexes
- `primary` on `id`
- `btree` on `created_at` (descending)
- `btree` on `subject_id`
- `btree` on `user_id`
- `btree` on `due_date`

## Risks / Trade-offs

- **[Risk] Cascade deletion of tasks when a subject is deleted**
  → **Mitigation**: Foreign key relation `subject_id` establishes referential integrity; cascading actions can be handled in backend business logic or triggers when APIs are built.

