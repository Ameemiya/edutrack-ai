## Context

The project currently provides CRUD services (`subject_service.py` and `task_service.py`) that communicate with Xano endpoints. A standalone script is needed in `scripts/calculate_progress.py` to evaluate the academic progress of a specific subject by fetching its tasks and computing the percentage of completed tasks.

## Goals / Non-Goals

**Goals:**
- Implement `scripts/calculate_progress.py` with a reusable function `calculate_subject_progress(subject_id: int, auth_token: Optional[str] = None) -> Dict[str, Any]`.
- Calculate `progress_percentage = (completed_tasks / total_tasks) * 100` rounded to 2 decimal places, or `0.0` when `total_tasks == 0`.
- Return a JSON object with: `subject_id`, `subject_name`, `total_tasks`, `completed_tasks`, `pending_tasks`, `progress_percentage`, and `status`.
- Provide a CLI interface (`python scripts/calculate_progress.py --subject-id <ID>`) outputting standard JSON to stdout.

**Non-Goals:**
- Do not create new database tables or Xano backend endpoints.
- Do not deploy or push to Xano.
- Do not rewrite existing Streamlit page interfaces.

## Decisions

- **Decision 1: Use existing CRUD services and fallback**: The script will leverage `task_service.list_tasks(auth_token)` and `subject_service.get_subject(subject_id, auth_token)` or direct requests to Xano endpoints using `.env` credentials, enabling both CLI standalone runs and unit testing.
- **Decision 2: Safe zero division**: If a subject has no tasks, `progress_percentage` is set to `0.0` rather than raising a ZeroDivisionError.
- **Decision 3: Status criteria**: Tasks with `status == "completed"` are counted as completed; all other statuses (`pending`, `in_progress`) count as pending.

## Risks / Trade-offs

- [Risk] Running CLI without auth token against private Xano endpoints → [Mitigation] Script supports reading auth token from optional arguments, `.env`, or testing mode with local mock store.
- [Risk] Subject not found → [Mitigation] Return a structured JSON with error message and appropriate status code/flag.

