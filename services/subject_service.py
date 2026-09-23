import os
import datetime
from typing import List, Dict, Optional, Any
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
        "professor": "Prof. Coordenador",
        "semester": "2025/1",
        "status": "Ativa",
        "color": "#4F46E5",
        "notes": "Desenvolvimento do projeto EduTrack AI",
    }
]
_id_counter = 2


def _get_api_url() -> Optional[str]:
    """Retrieve the Xano API base URL from env or streamlit secrets."""
    if "XANO_API_URL" in os.environ:
        return os.environ["XANO_API_URL"].rstrip("/")
    if st is not None and _st_runtime_exists():
        try:
            if hasattr(st, "secrets") and "XANO_API_URL" in st.secrets:
                return str(st.secrets["XANO_API_URL"]).rstrip("/")
        except Exception:
            pass
    return None


def _get_local_store() -> List[Dict[str, Any]]:
    """Get the local list of subjects stored in session_state or memory."""
    global _in_memory_db
    if st is not None and _st_runtime_exists():
        try:
            if "subjects" not in st.session_state:
                # Seed with initial helpful sample if completely empty
                st.session_state.subjects = [
                    {
                        "id": 1,
                        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "name": "Innovation Lab",
                        "code": "ILAB-2025",
                        "professor": "Prof. Coordenador",
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
    return _get_api_url() is not None


def validate_subject(name: str, status: Optional[str] = "Ativa") -> None:
    """Validate subject fields."""
    if not name or not name.strip():
        raise ValueError("O nome da disciplina é obrigatório.")
    if status and status not in VALID_STATUSES:
        raise ValueError(f"Status inválido: '{status}'. Deve ser um de: {', '.join(VALID_STATUSES)}.")


def list_subjects() -> List[Dict[str, Any]]:
    """Retrieve all academic subjects."""
    api_url = _get_api_url()
    if api_url:
        try:
            resp = requests.get(f"{api_url}/subject", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return list(_get_local_store())


def get_subject(subject_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single subject by ID."""
    api_url = _get_api_url()
    if api_url:
        try:
            resp = requests.get(f"{api_url}/subject/{subject_id}", timeout=5)
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
    semester: Optional[str] = None,
    status: str = "Ativa",
    color: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new academic subject."""
    name_clean = name.strip() if name else ""
    validate_subject(name_clean, status)

    payload = {
        "name": name_clean,
        "code": code.strip() if code else "",
        "professor": professor.strip() if professor else "",
        "semester": semester.strip() if semester else "",
        "status": status or "Ativa",
        "color": color.strip() if color else "#4F46E5",
        "notes": notes.strip() if notes else "",
    }

    api_url = _get_api_url()
    if api_url:
        try:
            resp = requests.post(f"{api_url}/subject", json=payload, timeout=5)
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
    semester: Optional[str] = None,
    status: Optional[str] = None,
    color: Optional[str] = None,
    notes: Optional[str] = None,
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
    if professor is not None:
        payload["professor"] = professor.strip()
    if semester is not None:
        payload["semester"] = semester.strip()
    if status is not None:
        payload["status"] = status
    if color is not None:
        payload["color"] = color.strip()
    if notes is not None:
        payload["notes"] = notes.strip()

    api_url = _get_api_url()
    if api_url:
        try:
            resp = requests.patch(f"{api_url}/subject/{subject_id}", json=payload, timeout=5)
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


def delete_subject(subject_id: int) -> bool:
    """Delete an academic subject by ID."""
    api_url = _get_api_url()
    if api_url:
        try:
            resp = requests.delete(f"{api_url}/subject/{subject_id}", timeout=5)
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


def count_active_subjects() -> int:
    """Count total active subjects."""
    subjects = list_subjects()
    return sum(1 for s in subjects if s.get("status") == "Ativa")

