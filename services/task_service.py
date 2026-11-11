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

VALID_STATUSES = ["pending", "in_progress", "completed"]

# In-memory storage fallback for standalone / testing usage
_in_memory_tasks: List[Dict[str, Any]] = [
    {
        "id": 1,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title": "Configuração do Ambiente",
        "description": "Configuração do ambiente de desenvolvimento Streamlit e Xano",
        "due_date": "2026-02-20",
        "status": "completed",
        "subject_id": 1,
        "user_id": 1,
    }
]
_task_id_counter = 2


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
    """Retrieve the Xano API base URL for academic tasks prioritizing st.secrets with os.environ fallback."""
    url = None
    if st is not None and _st_runtime_exists():
        try:
            if hasattr(st, "secrets"):
                url = st.secrets.get("XANO_TASKS_API_URL") or st.secrets.get("XANO_API_URL")
        except Exception:
            pass

    if not url:
        url = os.environ.get("XANO_TASKS_API_URL") or os.environ.get("XANO_API_URL")

    if not url:
        _load_env_file()
        url = os.environ.get("XANO_TASKS_API_URL") or os.environ.get("XANO_API_URL")

    if not url:
        url = "https://x8ki-letl-twmt.n7.xano.io/api:ngSiNEPC"
    return url.rstrip("/")


def _get_auth_token(token: Optional[str] = None) -> Optional[str]:
    """Retrieve auth token prioritizing direct arg, st.session_state, st.secrets, then os.environ."""
    if token:
        return token
    if st is not None and _st_runtime_exists():
        try:
            if "auth_token" in st.session_state and st.session_state.auth_token:
                return st.session_state.auth_token
            if hasattr(st, "secrets"):
                sec_token = st.secrets.get("XANO_AUTH_TOKEN") or st.secrets.get("AUTH_TOKEN")
                if sec_token:
                    return sec_token
        except Exception:
            pass

    env_token = os.environ.get("XANO_AUTH_TOKEN") or os.environ.get("AUTH_TOKEN")
    if env_token:
        return env_token

    _load_env_file()
    return os.environ.get("XANO_AUTH_TOKEN") or os.environ.get("AUTH_TOKEN")


def _get_local_store() -> List[Dict[str, Any]]:
    """Get the local list of tasks stored in session_state or memory."""
    global _in_memory_tasks
    if st is not None and _st_runtime_exists():
        try:
            if "academic_tasks" not in st.session_state:
                st.session_state.academic_tasks = list(_in_memory_tasks)
            return st.session_state.academic_tasks
        except Exception:
            pass
    return _in_memory_tasks


def fetch_tasks(auth_token: Optional[str] = None) -> Tuple[bool, Any]:
    """
    Busca tarefas acadêmicas diretamente do endpoint GET /academic_tasks do Xano usando o token de autenticação.
    Retorna (True, lista_de_tarefas) ou (False, mensagem_de_erro).
    """
    token = _get_auth_token(auth_token)
    if not token:
        return False, "Usuário não autenticado. Faça login para visualizar suas tarefas."

    api_url = _get_api_url()
    endpoint = f"{api_url}/academic_tasks"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(endpoint, headers=headers, timeout=10)
        data = resp.json() if resp.content else []

        if resp.status_code == 200 and isinstance(data, list):
            return True, data
        elif resp.status_code == 401:
            return False, "Sessão expirada ou não autorizada. Faça login novamente."
        else:
            msg = data.get("message") if isinstance(data, dict) else f"Erro HTTP {resp.status_code} ao buscar tarefas."
            return False, msg
    except requests.exceptions.RequestException as e:
        return False, f"Falha de conexão com a API de tarefas acadêmicas: {e}"


def list_tasks(auth_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all academic tasks, querying remote Xano if auth token exists."""
    token = _get_auth_token(auth_token)
    if token:
        success, data = fetch_tasks(token)
        if success and isinstance(data, list):
            return data
    return list(_get_local_store())


_UNSET = object()


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Any = _UNSET,
    status: Optional[str] = None,
    subject_id: Any = _UNSET,
    auth_token: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Update an existing academic task via PATCH /academic_tasks/{id}."""
    if status is not None and status not in VALID_STATUSES:
        raise ValueError(f"Status inválido: '{status}'. Deve ser um de: {', '.join(VALID_STATUSES)}.")

    payload: Dict[str, Any] = {}
    if title is not None:
        payload["title"] = title.strip()
    if description is not None:
        payload["description"] = description.strip()
    if due_date is not _UNSET:
        payload["due_date"] = due_date
    if status is not None:
        payload["status"] = status
    if subject_id is not _UNSET:
        payload["subject_id"] = subject_id

    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.patch(
                f"{api_url}/academic_tasks/{task_id}",
                json=payload,
                headers=headers,
                timeout=5,
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

    # Local fallback
    store = _get_local_store()
    for item in store:
        if item.get("id") == task_id:
            item.update(payload)
            return item
    return None


def delete_task(task_id: int, auth_token: Optional[str] = None) -> bool:
    """Delete an academic task by ID via DELETE /academic_tasks/{id}."""
    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.delete(
                f"{api_url}/academic_tasks/{task_id}",
                headers=headers,
                timeout=5,
            )
            if resp.status_code in (200, 204):
                store = _get_local_store()
                store[:] = [t for t in store if t.get("id") != task_id]
                return True
        except Exception:
            pass

    # Local fallback
    store = _get_local_store()
    initial_len = len(store)
    store[:] = [t for t in store if t.get("id") != task_id]
    return len(store) < initial_len


def create_task(
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    status: str = "pending",
    subject_id: Optional[int] = None,
    auth_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new academic task."""
    title_clean = title.strip() if title else ""
    if not title_clean:
        raise ValueError("O título da tarefa é obrigatório.")

    payload = {
        "title": title_clean,
        "description": description.strip() if description else "",
        "due_date": due_date,
        "status": status or "pending",
        "subject_id": subject_id,
    }

    token = _get_auth_token(auth_token)
    api_url = _get_api_url()
    if token and api_url:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            resp = requests.post(f"{api_url}/academic_tasks", json=payload, headers=headers, timeout=5)
            if resp.status_code in (200, 201):
                return resp.json()
        except Exception:
            pass

    # Local fallback
    global _task_id_counter, _in_memory_tasks
    new_item = {
        "id": _task_id_counter,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        **payload,
    }
    _task_id_counter += 1
    store = _get_local_store()
    store.append(new_item)
    return new_item

