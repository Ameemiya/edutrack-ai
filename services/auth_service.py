import os
from typing import Tuple, Dict, Any, Optional
import requests

try:
    import streamlit as st
    from streamlit.runtime import exists as _st_runtime_exists
except ImportError:
    st = None
    _st_runtime_exists = lambda: False


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


def get_auth_api_url() -> str:
    """Obtém a URL base dos endpoints de autenticação a partir de .env, os.environ ou st.secrets."""
    _load_env_file()
    
    url = os.environ.get("XANO_AUTH_API_URL") or os.environ.get("XANO_API_URL")
    if not url and st is not None and _st_runtime_exists():
        try:
            if hasattr(st, "secrets"):
                url = st.secrets.get("XANO_AUTH_API_URL") or st.secrets.get("XANO_API_URL")
        except Exception:
            pass
            
    if not url:
        url = "https://x8ki-letl-twmt.n7.xano.io/api:Authentication"
        
    return url.rstrip("/")


def signup(name: str, email: str, password: str) -> Tuple[bool, Any]:
    """
    Cadastra um novo usuário no Xano via endpoint auth/signup.
    Retorna (True, {'authToken': ...}) ou (False, mensagem_de_erro).
    """
    base_url = get_auth_api_url()
    name_clean = name.strip() if name else ""
    email_clean = email.strip().lower() if email else ""
    
    if not name_clean:
        return False, "O nome é obrigatório."
    if not email_clean:
        return False, "O e-mail é obrigatório."
    if not password:
        return False, "A senha é obrigatória."
        
    endpoint = f"{base_url}/auth/signup"
    payload = {
        "name": name_clean,
        "email": email_clean,
        "password": password
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json() if response.content else {}
        
        if response.status_code in (200, 201) and "authToken" in data:
            return True, data
        else:
            msg = data.get("message") or data.get("error") or f"Erro {response.status_code} ao cadastrar."
            return False, msg
    except requests.exceptions.RequestException as e:
        return False, f"Falha de conexão com o servidor de autenticação: {e}"


def login(email: str, password: str) -> Tuple[bool, Any]:
    """
    Autentica o usuário no Xano via endpoint auth/login.
    Retorna (True, {'authToken': ...}) ou (False, mensagem_de_erro).
    """
    base_url = get_auth_api_url()
    email_clean = email.strip().lower() if email else ""
    
    if not email_clean:
        return False, "Informe o e-mail."
    if not password:
        return False, "Informe a senha."
        
    endpoint = f"{base_url}/auth/login"
    payload = {
        "email": email_clean,
        "password": password
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=10)
        data = response.json() if response.content else {}
        
        if response.status_code == 200 and "authToken" in data:
            return True, data
        else:
            msg = data.get("message") or data.get("error") or "Credenciais inválidas."
            return False, msg
    except requests.exceptions.RequestException as e:
        return False, f"Falha de conexão com o servidor de autenticação: {e}"


def get_me(auth_token: str) -> Tuple[bool, Any]:
    """
    Recupera os dados do perfil do usuário autenticado no Xano via endpoint auth/me.
    Retorna (True, dict_do_usuario) ou (False, mensagem_de_erro).
    """
    if not auth_token:
        return False, "Token de autenticação ausente."
        
    base_url = get_auth_api_url()
    endpoint = f"{base_url}/auth/me"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        data = response.json() if response.content else {}
        
        if response.status_code == 200:
            return True, data
        elif response.status_code == 401:
            return False, "Sessão expirada. Faça login novamente."
        else:
            msg = data.get("message") or data.get("error") or f"Erro {response.status_code} ao buscar perfil."
            return False, msg
    except requests.exceptions.RequestException as e:
        return False, f"Falha ao conectar para obter perfil: {e}"


def logout() -> None:
    """Encerra a sessão do usuário no Streamlit."""
    if st is not None and _st_runtime_exists():
        if "auth_token" in st.session_state:
            del st.session_state["auth_token"]
        if "user" in st.session_state:
            del st.session_state["user"]


def is_authenticated() -> bool:
    """Verifica se há um usuário autenticado na sessão atual do Streamlit."""
    if st is not None and _st_runtime_exists():
        return bool(st.session_state.get("auth_token"))
    return False

