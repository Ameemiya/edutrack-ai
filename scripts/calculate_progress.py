import os
import sys
import json
import argparse
from typing import Dict, Any, Optional, Union, List

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services import subject_service, task_service, auth_service


def resolve_auth_token(
    token: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> Optional[str]:
    """
    Resolves auth token in order:
    1. Direct argument token
    2. Streamlit session_state or st.secrets if running within Streamlit
    3. Environment variables (XANO_AUTH_TOKEN, AUTH_TOKEN)
    4. Login via provided email & password or secrets/env credentials (XANO_USER_EMAIL, XANO_USER_PASSWORD)
    """
    if token:
        return token

    # Check Streamlit runtime session / secrets
    if subject_service.st is not None and subject_service._st_runtime_exists():
        try:
            sess_token = subject_service.st.session_state.get("auth_token")
            if sess_token:
                return sess_token
            if hasattr(subject_service.st, "secrets"):
                sec_token = subject_service.st.secrets.get("XANO_AUTH_TOKEN") or subject_service.st.secrets.get("AUTH_TOKEN")
                if sec_token:
                    return sec_token
        except Exception:
            pass

    # Check env variables
    env_token = os.environ.get("XANO_AUTH_TOKEN") or os.environ.get("AUTH_TOKEN")
    if env_token:
        return env_token

    subject_service._load_env_file()
    env_token = os.environ.get("XANO_AUTH_TOKEN") or os.environ.get("AUTH_TOKEN")
    if env_token:
        return env_token

    # Check email/password credentials to auto-login (checking st.secrets then os.environ)
    user_email = email
    user_password = password
    if subject_service.st is not None and subject_service._st_runtime_exists():
        try:
            if hasattr(subject_service.st, "secrets"):
                user_email = user_email or subject_service.st.secrets.get("XANO_USER_EMAIL")
                user_password = user_password or subject_service.st.secrets.get("XANO_USER_PASSWORD")
        except Exception:
            pass

    user_email = user_email or os.environ.get("XANO_USER_EMAIL")
    user_password = user_password or os.environ.get("XANO_USER_PASSWORD")

    if user_email and user_password:
        ok, res = auth_service.login(user_email, user_password)
        if ok and isinstance(res, dict) and "authToken" in res:
            return res["authToken"]

    return None


def calculate_subject_progress(
    subject_id: int,
    auth_token: Optional[str] = None,
    as_json: bool = False,
) -> Union[Dict[str, Any], str]:
    """
    Calculates progress for a single subject from Xano CRUD endpoints.
    Formula: (completed_tasks / total_tasks) * 100
    """
    token = resolve_auth_token(auth_token)

    # 1. Fetch subjects from Xano or fallback
    subjects_list: List[Dict[str, Any]] = []
    if token:
        ok, data = subject_service.fetch_subjects(token)
        if ok and isinstance(data, list):
            subjects_list = data
        else:
            result = {
                "error": f"Falha ao carregar disciplinas do Xano: {data}",
                "status": "error",
            }
            return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result
    else:
        # Fallback to local store
        subjects_list = subject_service.list_subjects()

    # Find target subject
    target_subject = next((s for s in subjects_list if s.get("id") == subject_id), None)

    if not target_subject:
        result = {
            "error": f"Disciplina com ID {subject_id} não encontrada no Xano.",
            "subject_id": subject_id,
            "subject_name": None,
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "progress_percentage": 0.0,
            "status": "not_found",
        }
        return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result

    subject_name = target_subject.get("name", f"Disciplina #{subject_id}")
    teacher_name = (
        target_subject.get("teacher")
        or target_subject.get("professor")
        or target_subject.get("docente")
        or target_subject.get("instructor")
        or target_subject.get("prof")
    )
    subject_hours = target_subject.get("hours") or target_subject.get("carga_horaria")

    # 2. Fetch tasks from Xano or fallback
    tasks_list: List[Dict[str, Any]] = []
    if token:
        ok_t, data_t = task_service.fetch_tasks(token)
        if ok_t and isinstance(data_t, list):
            tasks_list = data_t
        else:
            result = {
                "error": f"Falha ao carregar tarefas do Xano: {data_t}",
                "status": "error",
            }
            return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result
    else:
        tasks_list = task_service.list_tasks()

    # Filter tasks for this subject
    subject_tasks = [t for t in tasks_list if t.get("subject_id") == subject_id]
    total_tasks = len(subject_tasks)
    completed_tasks = sum(1 for t in subject_tasks if t.get("status") == "completed")
    pending_tasks = total_tasks - completed_tasks

    progress_pct = round((completed_tasks / total_tasks) * 100.0, 2) if total_tasks > 0 else 0.0

    result = {
        "subject_id": subject_id,
        "subject_name": subject_name,
        "teacher": teacher_name,
        "professor": teacher_name,
        "hours": subject_hours,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress_percentage": progress_pct,
        "status": "success",
    }

    return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result


def get_subject_progress_json(
    subject_id: int,
    auth_token: Optional[str] = None,
) -> str:
    """Convenience helper returning the progress directly as a formatted JSON string."""
    return calculate_subject_progress(subject_id, auth_token=auth_token, as_json=True)  # type: ignore


def calculate_all_subjects_progress(
    auth_token: Optional[str] = None,
    as_json: bool = False,
) -> Union[Dict[str, Any], str]:
    """
    Calculates progress for ALL subjects registered in Xano.
    Returns a list of subjects with their individual completion percentage
    and an overall summary.
    """
    token = resolve_auth_token(auth_token)

    # Fetch subjects from Xano or fallback
    if token:
        ok_s, subjects_data = subject_service.fetch_subjects(token)
        if not ok_s:
            result = {
                "error": f"Falha ao carregar disciplinas do Xano: {subjects_data}",
                "status": "error",
            }
            return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result
        subjects_list = subjects_data if isinstance(subjects_data, list) else []
    else:
        subjects_list = subject_service.list_subjects()

    # Fetch tasks from Xano or fallback
    if token:
        ok_t, tasks_data = task_service.fetch_tasks(token)
        if not ok_t:
            result = {
                "error": f"Falha ao carregar tarefas do Xano: {tasks_data}",
                "status": "error",
            }
            return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result
        tasks_list = tasks_data if isinstance(tasks_data, list) else []
    else:
        tasks_list = task_service.list_tasks()

    progress_by_subject = []
    total_all_tasks = 0
    total_all_completed = 0

    for subj in subjects_list:
        sub_id = subj.get("id")
        sub_name = subj.get("name", f"Disciplina #{sub_id}")
        teacher_name = (
            subj.get("teacher")
            or subj.get("professor")
            or subj.get("docente")
            or subj.get("instructor")
            or subj.get("prof")
        )
        subject_hours = subj.get("hours") or subj.get("carga_horaria")

        subj_tasks = [t for t in tasks_list if t.get("subject_id") == sub_id]
        tot = len(subj_tasks)
        comp = sum(1 for t in subj_tasks if t.get("status") == "completed")
        pend = tot - comp
        pct = round((comp / tot) * 100.0, 2) if tot > 0 else 0.0

        total_all_tasks += tot
        total_all_completed += comp

        progress_by_subject.append({
            "subject_id": sub_id,
            "subject_name": sub_name,
            "teacher": teacher_name,
            "professor": teacher_name,
            "hours": subject_hours,
            "total_tasks": tot,
            "completed_tasks": comp,
            "pending_tasks": pend,
            "progress_percentage": pct,
        })

    overall_pct = (
        round((total_all_completed / total_all_tasks) * 100.0, 2)
        if total_all_tasks > 0
        else 0.0
    )

    result = {
        "status": "success",
        "total_subjects": len(subjects_list),
        "total_tasks": total_all_tasks,
        "total_completed_tasks": total_all_completed,
        "overall_progress_percentage": overall_pct,
        "subjects": progress_by_subject,
        "subjects_progress": progress_by_subject,
    }

    return json.dumps(result, indent=2, ensure_ascii=False) if as_json else result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calcula o progresso de disciplinas com base nas tarefas cadastradas no Xano."
    )
    parser.add_argument(
        "subject_id",
        type=int,
        nargs="?",
        default=None,
        help="ID opcional da disciplina (se omitido, calcula para todas as disciplinas cadastradas no Xano).",
    )
    parser.add_argument(
        "--subject-id",
        dest="opt_subject_id",
        type=int,
        default=None,
        help="ID da disciplina específica.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Calcula o progresso de todas as disciplinas cadastradas no Xano.",
    )
    parser.add_argument(
        "--token",
        dest="token",
        type=str,
        default=None,
        help="Token de autenticação do Xano (Bearer). Se não informado, busca em XANO_AUTH_TOKEN ou faz login com credenciais.",
    )
    parser.add_argument(
        "--email",
        type=str,
        default=None,
        help="E-mail para login no Xano.",
    )
    parser.add_argument(
        "--password",
        type=str,
        default=None,
        help="Senha para login no Xano.",
    )

    args = parser.parse_args()
    target_id = args.subject_id if args.subject_id is not None else args.opt_subject_id

    # Resolve token (incluindo login via email/password se fornecido)
    auth_tok = resolve_auth_token(args.token, email=args.email, password=args.password)

    if target_id is not None and not args.all:
        output = calculate_subject_progress(target_id, auth_token=auth_tok, as_json=True)
    else:
        # Se nenhum ID for passado ou flag --all, calcula de todas as disciplinas cadastradas
        output = calculate_all_subjects_progress(auth_token=auth_tok, as_json=True)

    print(output)
