## Why

Users of EduTrack AI need an authentication mechanism to register personal accounts, log in securely, and view their user profile. Currently, the profile page `pages/3_👤_Perfil.py` is empty and students cannot authenticate against the Xano backend.

## What Changes

- Store the Xano authentication base API URL in a root `.env` configuration file.
- Implement an authentication service (`services/auth_service.py`) that integrates with Xano's `auth/signup`, `auth/login`, and `auth/me` endpoints against the `user` table.
- Implement the Streamlit profile and authentication interface in `pages/3_👤_Perfil.py` allowing users to register, sign in, maintain their session token in `st.session_state`, and display their profile data from `auth/me`.

## Capabilities

### New Capabilities
- `user-auth`: User authentication and profile management including signup, login, session token storage, and profile details retrieval.

### Modified Capabilities
*(None)*

## Impact

- **Configuration**: Adds `.env` to the project root with the Xano authentication API URL.
- **Frontend / UI**: Implements `pages/3_👤_Perfil.py` for user registration, login, and profile view.
- **Service Layer**: Adds `services/auth_service.py` to handle HTTP requests to Xano authentication endpoints.

