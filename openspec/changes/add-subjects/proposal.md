## Why

Students using EduTrack AI need a centralized way to track and manage their academic subjects (disciplinas) to organize coursework, grades, and associated tasks. Currently, the "Disciplinas" section in the application is a placeholder and the dashboard metric is hardcoded, preventing students from managing real academic data.

## What Changes

- Introduce the `subjects` capability allowing users to create, read, update, and delete academic subjects.
- Define data model and schema for academic subjects (name, code, professor, semester, workload/credits, color/tag, and status).
- Provide CRUD API endpoints to manage subjects.
- Update the Streamlit frontend (`app.py`) to list subjects, register new subjects, edit/delete existing ones, and reflect active subjects in the dashboard metrics.

## Capabilities

### New Capabilities
- `subjects`: Covers academic subject management including creating, viewing, updating, deleting subjects, and tracking their active status.

### Modified Capabilities
*(None - this is a new capability in the project)*

## Impact

- **Backend / Database**: Adds a new table (e.g., `subject`) and REST API endpoints for subject CRUD operations.
- **Frontend**: Updates `app.py` under the "Disciplinas" and "Dashboard" views to interact with subject data.
- **Dependencies**: Uses existing project dependencies (`streamlit`, `requests`).

