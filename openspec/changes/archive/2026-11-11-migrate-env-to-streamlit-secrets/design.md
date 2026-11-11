## Context

Currently, EduTrack AI defines helper functions `_load_env_file()` in each service module to parse key-value lines from `.env` and populate `os.environ`. Streamlit apps running locally or deployed to Streamlit Community Cloud should utilize `st.secrets` (`.streamlit/secrets.toml`). See `proposal.md` for motivation.

## Goals / Non-Goals

**Goals:**
- Replace manual `.env` file parsing in service modules (`services/auth_service.py`, `services/subject_service.py`, `services/task_service.py`, `services/report_service.py`) and scripts with a standardized configuration helper that checks `st.secrets` first.
- Maintain seamless backwards compatibility with `os.environ` for headless execution, automated tests, and CLI usage.
- Ensure development secrets are stored in `.streamlit/secrets.toml` and kept safely out of version control via `.gitignore`.

**Non-Goals:**
- Removing `os.environ` completely (needed when running Python scripts or `unittest` outside of Streamlit runtime).
- Implementing dynamic secret rotation or third-party vault integrations.

## Decisions

### 1. Configuration Resolution Precedence
- **Rationale**: 
  1. Check `st.secrets` if Streamlit is imported and runtime exists (`_st_runtime_exists()`).
  2. Check `os.environ` for existing environment variables.
  3. Fall back to hardcoded default endpoints or graceful degradation.
- **Alternatives Considered**: Direct dependence exclusively on `st.secrets` (would break `unittest discover tests` and CLI scripts when executed directly via `python`).

### 2. Centralized or Uniform Helper Resolution
- **Rationale**: Ensure all services inspect `st.secrets` directly and safely using `st.secrets.get(...)` wrapped in try/except blocks, avoiding `FileNotFoundError` when `secrets.toml` is not present during unit testing.

## Risks / Trade-offs

- **[Risk] Tests running outside Streamlit throw AttributeError/FileNotFoundError on `st.secrets`**
  → **Mitigation**: Guard access with `if st is not None and _st_runtime_exists() and hasattr(st, "secrets")`.
- **[Risk] Accidental commit of `.streamlit/secrets.toml`**
  → **Mitigation**: Confirm `.streamlit/` is explicitly listed in `.gitignore`.

