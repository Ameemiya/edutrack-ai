## Why

Currently, EduTrack AI services (`auth_service`, `subject_service`, `task_service`, `report_service`) and helper scripts manually load environment variables from `.env` via a custom `_load_env_file()` function and `os.environ`. Streamlit provides native, secure secrets management via `st.secrets` (configured in `.streamlit/secrets.toml` and encrypted/injected on Streamlit Community Cloud). Migrating to Streamlit secrets modernizes configuration management, eliminates custom `.env` parsing overhead, prevents credential leaks, and simplifies deployments.

## What Changes

- Migrate configuration loading across services (`auth_service.py`, `subject_service.py`, `task_service.py`, `report_service.py`, `pages/3_👤_Perfil.py`, and `scripts/calculate_progress.py`) to prioritize `st.secrets`.
- Retain environment variable fallback (`os.environ`) for headless execution and unit tests that run outside the Streamlit runtime.
- Deprecate custom manual `.env` file reading routines in favor of `st.secrets` and native environment lookups.
- Maintain `.streamlit/secrets.toml` as the primary local configuration store and ensure it is strictly ignored by `.gitignore`.

## Capabilities

### New Capabilities
- `secrets-configuration`: Manages application configuration and credentials using Streamlit `st.secrets` with graceful fallback to system environment variables.

### Modified Capabilities
*(None)*

## Impact

- **Affected Code**: `services/auth_service.py`, `services/subject_service.py`, `services/task_service.py`, `services/report_service.py`, `scripts/calculate_progress.py`, `pages/3_👤_Perfil.py`.
- **Configuration**: Uses `.streamlit/secrets.toml` for local secrets.
- **Git**: `.streamlit/` is maintained in `.gitignore`.

