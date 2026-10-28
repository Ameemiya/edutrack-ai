import os
import datetime
from typing import List, Dict, Optional, Any, Tuple
import requests

try:
    import streamlit as st
    from streamlit.runtime import exists as _st_runtime_exists
except ImportError:
    st = None
    _st_runtime_exists = lambda: False

# Allowed statuses
VALID_STATUSES = ["Ativa", "Concluída", "Trancada"]

# In-memory storage fallback for standalone / testing usage outside Streamlit runtime
_in_memory_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": "Innovation Lab",
        "code": "ILAB-2025",
        "teacher": "Prof. Coordenador",
        "professor": "Prof. Coordenador",
        "hours": 60,
        "semester": "2025/1",
        "status": "Ativa",
        "color": "#4F46E5",
        "notes": "Desenvolvimento do projeto EduTrack AI",
    }
]
_id_counter = 2


def _load_env_file() -> None:
    """Carrega as variáveis do arquivo .env na raiz do projeto."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass


def _get_api_url() -> str:
    """Retrieve the Xano API base URL for subjects."""
    _load_env_file()
    url = os.environ.get("XANO_SUBJECTS_API_URL") or os.environ.get("XANO_API_URL")
    if not url and st is not None and _st_runtime_exists():
        try:
            if hasattr(st, "secrets"):
                url = st.secrets.get("XANO_SUBJECTS_API_URL") or st.secrets.get("XANO_API_URL")
        except Exception:
            pass
    if not url:
        url = "https://x8ki-letl-twmt.n7.xano.io/api:4ZzBuB4S"
    return url.rstrip("/")


def _get_auth_token(token: Optional[str] = None) -> Optional[str]:
    """Retrieve auth token from argument or session state."""
    if token:
        return token
    if st is not None and _st_runtime_exists():
        try:
            return st.session_state.get("auth_token")
        except Exception:
            pass
    return None


def _get_local_store() -> List[Dict[str, Any]]:
    """Get the local list of subjects stored in session_state or memory."""
    global _in_memory_db
    if st is not None and _st_runtime_exists():
        try:
            if "subjects" not in st.session_state:
                st.session_state.subjects = [
                    {
                        "id": 1,
                        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "name": "Innovation Lab",
                        "code": "ILAB-2025",
                        "teacher": "Prof. Coordenador",
                        "professor": "Prof. Coordenador",
                        "hours": 60,
                        "semester": "2025/1",
                        "status": "Ativa",
                        "color": "#4F46E5",
                        "notes": "Desenvolvimento do projeto EduTrack AI",
                    }
                ]
                st.session_state.subject_next_id = 2
            return st.session_state.subjects
        except Exception:
            pass
    return _in_memory_db


def is_connected_to_xano() -> bool:
    """Check if remote Xano backend endpoint is configured."""
    return bool(_get_api_url())


def validate_subject(name: str, status: Optional[str] = "Ativa") -> None:
    """Validate subject fields."""
    if not name or not name.strip():
        raise ValueError("O nome da disciplina é obrigatório.")
    if status and status not in VALID_STATUSES:
        raise ValueError(f"Status inválido: '{status}'. Deve ser um de: {', '.join(VALID_STATUSES)}.")


def fetch_subjects(auth_token: Optional[str] = None) -> Tuple[bool, Any]:
    """
    Busca disciplinas diretamente do endpoint GET /subjects do Xano usando o token de autenticação.
    Retorna (True, lista_de_disciplinas) ou (False, mensagem_de_erro).
    """
    token = _get_auth_token(auth_token)
    if not token:
        return False, "Usuário não autenticado. Faça login para visualizar suas disciplinas."

    api_url = _get_api_url()
    endpoint = f"{api_url}/subjects"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(endpoint, headers=headers, timeout=10)
        data = resp.json() if resp.content else []

        if resp.status_code == 200 and isinstance(data, list):
            return True, data
        elif resp.status_code == 401:
            return False, "Sessão expirada ou não autorizada. Faça login novamente."
        else:
            msg = data.get("message") if isinstance(data, dict) else f"Erro HTTP {resp.status_code} ao buscar disciplinas."
            return False, msg
    except requests.exceptions.RequestException as e:
        return False, f"Falha de conexão com a API de disciplinas: {e}"


def list_subjects(auth_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all academic subjects, querying remote Xano if auth token exists."""
    token = _get_auth_token(auth_token)
    if token:
        success, data = fetch_subjects(token)
        if success and isinstance(data, list):
            return data
    return list(_get_local_store())


def get_subject(subject_id: int, auth_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieve a single subject by ID."""
    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.get(f"{api_url}/subjects/{subject_id}", headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
    store = _get_local_store()
    for s in store:
        if s.get("id") == subject_id:
            return s
    return None


def create_subject(
    name: str,
    code: Optional[str] = None,
    professor: Optional[str] = None,
    teacher: Optional[str] = None,
    hours: Optional[int] = None,
    semester: Optional[str] = None,
    status: str = "Ativa",
    color: Optional[str] = None,
    notes: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new academic subject."""
    name_clean = name.strip() if name else ""
    validate_subject(name_clean, status)

    instructor = teacher or professor or ""
    payload = {
        "name": name_clean,
        "code": code.strip() if code else "",
        "professor": instructor.strip(),
        "teacher": instructor.strip(),
        "hours": hours,
        "semester": semester.strip() if semester else "",
        "status": status or "Ativa",
        "color": color.strip() if color else "#4F46E5",
        "notes": notes.strip() if notes else "",
    }

    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.post(f"{api_url}/subjects", json=payload, headers=headers, timeout=5)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception:
            pass

    # Local store fallback
    global _id_counter, _in_memory_db
    if st is not None and _st_runtime_exists():
        try:
            store = _get_local_store()
            next_id = st.session_state.get("subject_next_id", len(store) + 1)
            new_item = {
                "id": next_id,
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                **payload,
            }
            store.append(new_item)
            st.session_state.subject_next_id = next_id + 1
            return new_item
        except Exception:
            pass

    new_item = {
        "id": _id_counter,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        **payload,
    }
    _id_counter += 1
    _in_memory_db.append(new_item)
    return new_item


def update_subject(
    subject_id: int,
    name: Optional[str] = None,
    code: Optional[str] = None,
    professor: Optional[str] = None,
    teacher: Optional[str] = None,
    hours: Optional[int] = None,
    semester: Optional[str] = None,
    status: Optional[str] = None,
    color: Optional[str] = None,
    notes: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Update an existing academic subject."""
    if name is not None:
        validate_subject(name, status)
    elif status is not None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Status inválido: '{status}'. Deve ser um de: {', '.join(VALID_STATUSES)}.")

    payload = {}
    if name is not None:
        payload["name"] = name.strip()
    if code is not None:
        payload["code"] = code.strip()
    instructor = teacher or professor
    if instructor is not None:
        payload["professor"] = instructor.strip()
        payload["teacher"] = instructor.strip()
    if hours is not None:
        payload["hours"] = hours
    if semester is not None:
        payload["semester"] = semester.strip()
    if status is not None:
        payload["status"] = status
    if color is not None:
        payload["color"] = color.strip()
    if notes is not None:
        payload["notes"] = notes.strip()

    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.patch(f"{api_url}/subjects/{subject_id}", json=payload, headers=headers, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

    store = _get_local_store()
    for item in store:
        if item.get("id") == subject_id:
            item.update(payload)
            return item
    return None


def delete_subject(subject_id: int, auth_token: Optional[str] = None) -> bool:
    """Delete an academic subject by ID."""
    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.delete(f"{api_url}/subjects/{subject_id}", headers=headers, timeout=5)
            if resp.status_code in (200, 204):
                store = _get_local_store()
                store[:] = [s for s in store if s.get("id") != subject_id]
                return True
        except Exception:
            pass

    store = _get_local_store()
    initial_len = len(store)
    store[:] = [s for s in store if s.get("id") != subject_id]
    return len(store) < initial_len


def count_active_subjects(auth_token: Optional[str] = None) -> int:
    """Count total active subjects."""
    subjects = list_subjects(auth_token)
    return sum(1 for s in subjects if s.get("status") == "Ativa")
