import os
from typing import Optional, Tuple, Any, Dict
import requests

try:
    import streamlit as st
    from streamlit.runtime import exists as _st_runtime_exists
except ImportError:
    st = None
    _st_runtime_exists = lambda: False

from scripts.generate_performance_report_pdf import generate_performance_report_pdf


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


def get_reports_api_url() -> str:
    """Retorna a URL base do endpoint de relatórios no Xano."""
    _load_env_file()
    url = os.environ.get("XANO_REPORTS_API_URL") or os.environ.get("XANO_API_URL")
    if not url and st is not None and _st_runtime_exists():
        try:
            if hasattr(st, "secrets"):
                url = st.secrets.get("XANO_REPORTS_API_URL") or st.secrets.get("XANO_API_URL")
        except Exception:
            pass
    if not url:
        url = "https://x8ki-letl-twmt.n7.xano.io/api:VFzwkOgb"
    return url.rstrip("/")


def fetch_report_data_from_xano(auth_token: Optional[str] = None) -> Tuple[bool, Any]:
    """
    Busca os dados do relatório diretamente do endpoint GET /download_pdf?format=json do Xano.
    Retorna (True, dict_do_relatorio) ou (False, mensagem_de_erro).
    """
    if not auth_token:
        return False, "Usuário não autenticado."

    api_url = get_reports_api_url()
    endpoint = f"{api_url}/download_pdf"
    headers = {"Authorization": f"Bearer {auth_token}"}
    params = {"format": "json"}

    try:
        resp = requests.get(endpoint, headers=headers, params=params, timeout=10)
        data = resp.json() if resp.content else {}
        if resp.status_code == 200:
            return True, data
        elif resp.status_code == 401:
            return False, "Sessão expirada ou não autorizada."
        else:
            return False, data.get("message") or f"Erro HTTP {resp.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Falha de conexão com a API de relatórios: {e}"


def generate_student_pdf_report(
    output_path: str = "relatorio_desempenho.pdf",
    auth_token: Optional[str] = None,
    user_data: Optional[Dict[str, Any]] = None,
    subjects: Optional[Any] = None,
    tasks: Optional[Any] = None,
) -> bytes:
    """
    Gera o relatório de desempenho em PDF e retorna os bytes do arquivo para download.
    Permite passar diretamente dados do aluno, disciplinas e tarefas para performance ideal.
    """
    pdf_path = generate_performance_report_pdf(
        output_path=output_path,
        auth_token=auth_token,
        user_data=user_data,
        subjects=subjects,
        tasks=tasks,
    )
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes

