## Why

Students and teachers need visibility into academic progress per subject based on task completions. Providing a standalone Python script in `scripts/calculate_progress.py` allows automated calculation of completion percentage (completed / total) per discipline and returns structured JSON for consumption by services, CLI, or automations using existing CRUD endpoints.

## What Changes

- Add a Python script `scripts/calculate_progress.py` that connects to existing CRUD endpoints to fetch tasks and subjects.
- Calculate subject-level academic progress as the percentage of completed tasks over total tasks associated with that subject.
- Return structured JSON containing subject ID, subject name, total tasks, completed tasks, pending tasks, and percentage of progress (0.0 to 100.0%).
- Handle edge cases, such as subjects with 0 tasks (0.0% progress) and non-existent subjects.

## Capabilities

### New Capabilities
- `progress-calculation`: Calculation of academic progress percentage for a subject based on its tasks via CRUD endpoints, returning structured JSON output.

### Modified Capabilities

## Impact

- New script: `scripts/calculate_progress.py`.
- Consumes existing Xano CRUD endpoints or service client methods for `subjects` and `academic_tasks`.
- No database schema or breaking changes.

