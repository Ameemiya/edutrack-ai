## Context

EduTrack AI combines a Streamlit client interface (`app.py`) with a Xano backend architecture (`tables/`, `apis/`). Currently, the "Disciplinas" view is a static placeholder and dashboard counters are hardcoded. See `proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**
- Provide a database schema and API contract for subjects (`subject`) in Xano.
- Implement a client service layer (`services/subject_service.py`) to manage API communication and data retrieval.
- Build an interactive UI in Streamlit (`app.py`) under "Disciplinas" to list, create, edit, and delete subjects.
- Dynamically calculate and display the active subjects count on the Dashboard.

**Non-Goals:**
- Grading calculations or assignment tracking linked to subjects (to be covered in dedicated grading/tasks changes).
- Complex role-based permissions for university administrators (assumes single-user student profile context for current phase).

## Decisions

### 1. Dedicated Service Layer (`services/subject_service.py`)
- **Rationale**: Isolates HTTP network calls and error handling from the Streamlit UI components. Provides support for environment configuration (`XANO_API_URL`) and an in-memory/session fallback when working offline or before remote backend deployment.
- **Alternatives Considered**: Inlining `requests` calls directly into `app.py` (leads to duplicate logic and brittle error handling).

### 2. Standardized Field Schema (English schema, Portuguese UI)
- **Rationale**: Keeps backend data models consistent with existing codebase conventions (`name`, `code`, `professor`, `semester`, `status`, `created_at`), while presenting localized Portuguese labels in Streamlit ("Nome", "Código", "Professor", "Semestre", "Status").
- **Alternatives Considered**: Using Portuguese identifiers in database schema (deviates from project's Xano standard schemas).

### 3. Subject Status Lifecycle
- **Rationale**: Support statuses `"Ativa"` (active), `"Concluída"` (completed), and `"Trancada"` (dropped). The dashboard "Disciplinas Ativas" metric will filter strictly for active subjects.
- **Alternatives Considered**: Boolean `is_active` flag (lacks fidelity for academic progress tracking).

## Risks / Trade-offs

- **[Risk] Remote Xano backend endpoint not configured in local environment**
  → **Mitigation**: Implement graceful fallback in `subject_service.py` utilizing Streamlit `st.session_state` storage when `XANO_API_URL` is absent, displaying an informational banner.
- **[Risk] Streamlit page re-render resets form state**
  → **Mitigation**: Use `st.form` with clear submission callbacks and state re-fetching.

