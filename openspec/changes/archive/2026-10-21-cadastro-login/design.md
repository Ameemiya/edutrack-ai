## Context

EduTrack AI currently has an empty profile page (`pages/3_👤_Perfil.py`). The Xano backend already defines the authentication query endpoints `auth/login`, `auth/signup`, and `auth/me` mapped to the `user` table in `api/authentication/auth/`. To enable end-to-end authentication in the Streamlit frontend, a client service and interactive profile UI are needed, with the API base URL configured in `.env`.

## Goals / Non-Goals

**Goals:**
- Create `.env` in the project root to store `XANO_AUTH_API_URL`.
- Implement `services/auth_service.py` to handle network requests to `auth/signup`, `auth/login`, and `auth/me`.
- Implement `pages/3_👤_Perfil.py` with signup, login, session state token management, and authenticated profile display.

**Non-Goals:**
- Altering the backend Xano authentication queries or database schema.
- Password reset, magic link logins, or social OAuth integration (out of requested scope).

## Decisions

### 1. Environment Configuration Loading
- **Decision**: Store `XANO_AUTH_API_URL` in `.env` at the project root.
- **Rationale**: Keeps API endpoint URLs configurable across local development and production without committing credentials or endpoints to git (`.env` is already listed in `.gitignore`). `auth_service.py` will read `.env` and fallback to `st.secrets` or `os.environ`.

### 2. Dedicated Authentication Service (`services/auth_service.py`)
- **Decision**: Encapsulate API communication in a dedicated service module.
- **Methods**:
  - `signup(name, email, password)`: calls `POST /auth/signup`, returns auth token or error message.
  - `login(email, password)`: calls `POST /auth/login`, returns auth token or error message.
  - `get_me(token)`: calls `GET /auth/me` with `Authorization: Bearer <token>`, returns user profile record.
  - `logout()`: clears session state.
- **Rationale**: Isolates network logic, headers, and error handling from the Streamlit UI presentation.

### 3. Streamlit Profile Page UI (`pages/3_👤_Perfil.py`)
- **Decision**: Conditional rendering based on `st.session_state.get("auth_token")`:
  - **Unauthenticated State**: Tabbed view with "Entrar" (Login) and "Criar Conta" (Signup) forms.
  - **Authenticated State**: Card showing student profile details (`name`, `email`, `id`, `created_at`) retrieved from `auth/me`, with a "Sair" (Logout) button.

## Risks / Trade-offs

- **[Risk] Unreachable Xano base URL during local offline testing**
  → **Mitigation**: Provide clear validation and warning banners in `pages/3_👤_Perfil.py` when `.env` is unconfigured or connection times out.
- **[Risk] Token expiration**
  → **Mitigation**: If `auth/me` returns 401/Unauthorized, automatically clear invalid token and prompt user to log in again.

