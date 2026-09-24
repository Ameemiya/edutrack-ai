## Context

EduTrack AI utilizes Xano as its backend database and API platform. To store course subject information tied to student users, a database table definition `subjects` is required. Per `AGENTS.md`, the scope of this proposal is restricted strictly to table definition.

## Goals / Non-Goals

**Goals:**
- Define the XanoScript schema for the `subjects` table in `tables/subjects.xs`.
- Include fields: `id`, `name`, `teacher`, `hours`, and `user_id` as foreign key to `user`.
- Configure primary and relationship indexes (`id`, `created_at`, `user_id`).

**Non-Goals:**
- Creating CRUD API endpoints (out of scope per `AGENTS.md`).
- Creating frontend Streamlit components or tests (out of scope per `AGENTS.md`).

## Decisions

### 1. File Location and Table Identifier
- **Decision**: Define table `subjects` in `tables/subjects.xs`.
- **Rationale**: Aligns with project standard of placing Xano table definitions under `tables/`.

### 2. Foreign Key Syntax
- **Decision**: Use `int user_id? { table = "user" }` to establish the relationship to the standard Xano authentication table `user`.
- **Rationale**: Follows standard XanoScript foreign key declaration pattern seen across existing project tables (e.g., `account_id` in `757724_event_log.xs`).

### 3. Field Types and Constraints
- `id`: integer, auto-increment primary key
- `created_at`: timestamp, default `now`, private visibility
- `name`: text with `filters=trim`, required
- `teacher`: text with `filters=trim`, optional
- `hours`: integer, course duration / credits, optional
- `user_id`: integer referencing `table = "user"`, optional foreign key

## Risks / Trade-offs

- **[Risk] User table name discrepancy (`user` vs `users`)**
  → **Mitigation**: Xano default authentication table identifier is `user` (as reflected in existing endpoints like `apis/event_logs/3648748_user_GET.xs`). Using `table = "user"` ensures compatibility with Xano's auth schema.

