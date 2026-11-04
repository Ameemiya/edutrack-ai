import os
import sys
import datetime
import argparse
import unicodedata
from typing import Dict, Any, Optional, List, Tuple

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services import subject_service, task_service, auth_service
from scripts.calculate_progress import resolve_auth_token, calculate_all_subjects_progress


def clean_display_text(text: Any) -> str:
    """
    Cleans text by removing emojis and UI symbols that cause visual artifacts in PDF.
    """
    if text is None:
        return ""
    s = str(text)
    # Remove common UI emojis used in Streamlit badges
    replacements = {
        "✅": "",
        "⏳": "",
        "📌": "",
        "📚": "",
        "📝": "",
        "🎓": "",
        "👤": "",
        "✏️": "",
        "🗑️": "",
        "📊": "",
        "ℹ️": "",
        "⚠️": "",
        "🎉": "",
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }
    for emo, rep in replacements.items():
        s = s.replace(emo, rep)

    # Strip any remaining 4-byte UTF-8 emojis or surrogate pairs
    filtered_chars = [ch for ch in s if ord(ch) <= 0xFFFF]
    return "".join(filtered_chars).strip()


class SimplePDFBuilder:
    """
    Standard PDF 1.4 canvas builder in pure Python with WinAnsiEncoding support.
    Renders clean, professional text with proper Portuguese accented characters.
    """
    def __init__(self, page_width: float = 595.28, page_height: float = 841.89):  # A4 size in points
        self.width = page_width
        self.height = page_height
        self.pages: List[str] = []
        self.current_commands: List[str] = []
        self.current_y = page_height - 50

    def add_page(self):
        if self.current_commands:
            self.pages.append("\n".join(self.current_commands))
            self.current_commands = []
        self.current_y = self.height - 50

    def check_page_break(self, needed_space: float = 40):
        if self.current_y - needed_space < 50:
            self.add_page()

    def escape_pdf_text(self, text: str) -> str:
        r"""
        Escapes text for PDF literal strings with WinAnsiEncoding:
        - Accented characters (e.g. á, é, í, ó, ú, ã, õ, ç, ê, ô) use octal escapes (\ddd)
        - Special PDF literal characters (, ), \ are properly escaped
        """
        cleaned = clean_display_text(text)
        normalized = unicodedata.normalize("NFC", cleaned)
        escaped = []
        for char in normalized:
            try:
                b = char.encode("cp1252")[0]
                if char == "\\":
                    escaped.append("\\\\")
                elif char == "(":
                    escaped.append("\\(")
                elif char == ")":
                    escaped.append("\\)")
                elif 32 <= b <= 126:
                    escaped.append(char)
                else:
                    escaped.append(f"\\{b:03o}")
            except UnicodeEncodeError:
                decomposed = unicodedata.normalize("NFKD", char).encode("ascii", "ignore").decode("ascii")
                escaped.append(decomposed if decomposed else "")
        return "".join(escaped)

    def draw_text(self, text: str, x: float, y: float, font_size: float = 10, bold: bool = False, color: Tuple[float, float, float] = (0, 0, 0)):
        clean = self.escape_pdf_text(text)
        r, g, b = color
        font_name = "/F2" if bold else "/F1"
        cmd = f"""q
{r:.2f} {g:.2f} {b:.2f} rg
BT
{font_name} {font_size} Tf
{x:.2f} {y:.2f} Td
({clean}) Tj
ET
Q"""
        self.current_commands.append(cmd)

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, line_width: float = 1, color: Tuple[float, float, float] = (0.7, 0.7, 0.7)):
        r, g, b = color
        cmd = f"""q
{r:.2f} {g:.2f} {b:.2f} RG
{line_width:.2f} w
{x1:.2f} {y1:.2f} m
{x2:.2f} {y2:.2f} l
S
Q"""
        self.current_commands.append(cmd)

    def draw_rect(self, x: float, y: float, w: float, h: float, fill_color: Optional[Tuple[float, float, float]] = None, border_color: Optional[Tuple[float, float, float]] = None):
        cmd = "q\n"
        if fill_color:
            r, g, b = fill_color
            cmd += f"{r:.2f} {g:.2f} {b:.2f} rg\n"
        if border_color:
            r, g, b = border_color
            cmd += f"{r:.2f} {g:.2f} {b:.2f} RG\n1 w\n"
        
        cmd += f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re\n"
        if fill_color and border_color:
            cmd += "B\n"
        elif fill_color:
            cmd += "f\n"
        else:
            cmd += "S\n"
        cmd += "Q"
        self.current_commands.append(cmd)

    def build(self) -> bytes:
        if self.current_commands or not self.pages:
            self.pages.append("\n".join(self.current_commands))

        page_count = len(self.pages)
        objects: List[bytes] = []

        page_obj_ids = [3 + i for i in range(page_count)]
        content_obj_ids = [3 + page_count + i for i in range(page_count)]
        font1_id = 3 + 2 * page_count
        font2_id = 4 + 2 * page_count

        catalog = f"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        objects.append(catalog.encode("ascii"))

        kids_str = " ".join([f"{pid} 0 R" for pid in page_obj_ids])
        pages_root = f"2 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {page_count} >>\nendobj\n"
        objects.append(pages_root.encode("ascii"))

        for i in range(page_count):
            p_obj = (
                f"{page_obj_ids[i]} 0 obj\n"
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
                f"/Contents {content_obj_ids[i]} 0 R "
                f"/Resources << /Font << /F1 {font1_id} 0 R /F2 {font2_id} 0 R >> >> >>\n"
                f"endobj\n"
            )
            objects.append(p_obj.encode("ascii"))

        for i in range(page_count):
            content_bytes = self.pages[i].encode("ascii")
            stream_obj = (
                f"{content_obj_ids[i]} 0 obj\n"
                f"<< /Length {len(content_bytes)} >>\n"
                f"stream\n"
            ).encode("ascii") + content_bytes + b"\nendstream\nendobj\n"
            objects.append(stream_obj)

        # Standard Type 1 fonts with explicit WinAnsiEncoding for correct Portuguese accents
        font1 = f"{font1_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n"
        objects.append(font1.encode("ascii"))

        font2 = f"{font2_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n"
        objects.append(font2.encode("ascii"))

        output = b"%PDF-1.4\n"
        offsets = [0]
        for obj in objects:
            offsets.append(len(output))
            output += obj

        xref_offset = len(output)
        total_objs = len(objects) + 1
        output += f"xref\n0 {total_objs}\n".encode("ascii")
        output += b"0000000000 65535 f \n"
        for off in offsets[1:]:
            output += f"{off:010d} 00000 n \n".encode("ascii")

        trailer = (
            f"trailer\n"
            f"<< /Size {total_objs} /Root 1 0 R >>\n"
            f"startxref\n"
            f"{xref_offset}\n"
            f"%%EOF\n"
        )
        output += trailer.encode("ascii")
        return output


def get_subject_teacher_name(s: Any) -> str:
    """
    Extracts the professor / teacher name from a subject record,
    checking standard aliases used in Xano and the frontend.
    """
    if not isinstance(s, dict):
        return ""
    for k in ("teacher", "professor", "docente", "instructor", "prof", "teacher_name", "professor_name"):
        v = s.get(k)
        if v and str(v).strip():
            cleaned = str(v).strip()
            if cleaned.lower() not in ("none", "null", "undefined", "não informado", "nao informado", "n/d", "-"):
                return cleaned
    return ""


def generate_performance_report_pdf(
    output_path: str = "relatorio_desempenho.pdf",
    auth_token: Optional[str] = None,
    user_data: Optional[Dict[str, Any]] = None,
    subjects: Optional[List[Dict[str, Any]]] = None,
    tasks: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Generates a structured PDF report summarizing student academic performance.
    Correctly formats Portuguese accents and removes visual emoji artifacts.
    Returns the absolute path of the generated PDF file.
    """
    token = resolve_auth_token(auth_token)

    # 1. Fetch / resolve student user data
    user_name = "Estudante EduTrack AI"
    user_email = "estudante@edutrack.ai"
    user_id_str = "Local / Visitante"

    if user_data and isinstance(user_data, dict):
        user_name = user_data.get("name") or user_name
        user_email = user_data.get("email") or user_email
        if user_data.get("id"):
            user_id_str = str(user_data.get("id"))
    else:
        # Check Streamlit session state if running in web context
        try:
            import streamlit as _st
            if hasattr(_st, "session_state") and "user" in _st.session_state and isinstance(_st.session_state["user"], dict):
                st_u = _st.session_state["user"]
                user_name = st_u.get("name") or user_name
                user_email = st_u.get("email") or user_email
                if st_u.get("id"):
                    user_id_str = str(st_u.get("id"))
        except Exception:
            pass

        # If still default and token is available, query auth_service.get_me
        if user_id_str == "Local / Visitante" and token:
            ok_u, user_info = auth_service.get_me(token)
            if ok_u and isinstance(user_info, dict):
                user_name = user_info.get("name") or user_name
                user_email = user_info.get("email") or user_email
                if user_info.get("id"):
                    user_id_str = str(user_info.get("id"))

    user_name = clean_display_text(user_name)
    user_email = clean_display_text(user_email)
    user_id_str = clean_display_text(user_id_str)

    # 2. Gather progress and task data for this student
    if subjects is not None:
        all_subjects = subjects if isinstance(subjects, list) else []
    elif token:
        ok_s, s_list = subject_service.fetch_subjects(token)
        all_subjects = s_list if ok_s and isinstance(s_list, list) else []
    else:
        all_subjects = subject_service.list_subjects()

    if tasks is not None:
        all_tasks = tasks if isinstance(tasks, list) else []
    elif token:
        ok_t, t_list = task_service.fetch_tasks(token)
        all_tasks = t_list if ok_t and isinstance(t_list, list) else []
    else:
        all_tasks = task_service.list_tasks()

    # Deduplicate tasks by ID to ensure each task appears exactly once
    unique_tasks = []
    seen_ids = set()
    for t in all_tasks:
        tid = t.get("id")
        if tid is not None:
            if tid in seen_ids:
                continue
            seen_ids.add(tid)
        unique_tasks.append(t)
    all_tasks = unique_tasks

    subj_lookup = {s["id"]: s for s in all_subjects if isinstance(s, dict) and "id" in s}
    subj_map = {s["id"]: clean_display_text(s.get("name", f"Disciplina #{s['id']}")) for s in all_subjects if isinstance(s, dict) and "id" in s}

    total_subjects = len(all_subjects)
    total_tasks = len(all_tasks)
    total_completed = sum(1 for t in all_tasks if str(t.get("status", "")).lower() == "completed")
    overall_progress = round((total_completed / total_tasks * 100.0), 2) if total_tasks > 0 else 0.0

    subjects_summary = []
    for s in all_subjects:
        sid = s.get("id")
        s_name = s.get("name", f"Disciplina #{sid}")
        teacher = get_subject_teacher_name(s)
        hours = s.get("hours") or s.get("workload") or s.get("carga_horaria")

        s_tasks = [t for t in all_tasks if t.get("subject_id") == sid]
        s_tot = len(s_tasks)
        s_comp = sum(1 for t in s_tasks if str(t.get("status", "")).lower() == "completed")
        s_prog = round((s_comp / s_tot * 100.0), 2) if s_tot > 0 else 0.0

        subjects_summary.append({
            "subject_id": sid,
            "subject_name": s_name,
            "teacher": teacher,
            "professor": teacher,
            "hours": hours,
            "total_tasks": s_tot,
            "completed_tasks": s_comp,
            "pending_tasks": s_tot - s_comp,
            "progress_percentage": s_prog,
        })

    # 3. Build PDF layout
    pdf = SimplePDFBuilder()
    now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Header banner
    pdf.draw_rect(40, 750, 515, 55, fill_color=(0.18, 0.25, 0.45))
    pdf.draw_text("EduTrack AI - Relatório de Desempenho Acadêmico", 55, 780, font_size=15, bold=True, color=(1, 1, 1))
    pdf.draw_text("Acompanhamento Individual de Desempenho e Metas Acadêmicas", 55, 762, font_size=9, bold=False, color=(0.85, 0.88, 0.95))

    # Student metadata box with ID and Name
    pdf.draw_rect(40, 675, 515, 62, fill_color=(0.96, 0.97, 0.99), border_color=(0.85, 0.88, 0.92))
    pdf.draw_text("IDENTIFICAÇÃO DO ALUNO", 55, 720, font_size=9, bold=True, color=(0.3, 0.35, 0.45))
    pdf.draw_text(f"Aluno(a): {user_name}", 55, 703, font_size=10.5, bold=True, color=(0.1, 0.1, 0.1))
    pdf.draw_text(f"E-mail: {user_email}", 55, 688, font_size=9, bold=False, color=(0.35, 0.35, 0.35))
    pdf.draw_text(f"Matrícula / ID: {user_id_str}", 360, 703, font_size=9.5, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text(f"Data de Emissão: {now_str}", 360, 688, font_size=9, bold=False, color=(0.4, 0.4, 0.4))

    # Summary metrics cards
    pdf.draw_text("VISÃO GERAL DO DESEMPENHO", 40, 650, font_size=11, bold=True, color=(0.15, 0.2, 0.3))
    pdf.draw_line(40, 642, 555, 642, line_width=1, color=(0.8, 0.82, 0.85))

    metrics = [
        ("Disciplinas", str(total_subjects)),
        ("Tarefas Totais", str(total_tasks)),
        ("Concluídas", str(total_completed)),
        ("Pendentes", str(total_tasks - total_completed)),
        ("Progresso Geral", f"{overall_progress:.1f}%"),
    ]

    col_w = 98
    for i, (label, val) in enumerate(metrics):
        box_x = 40 + i * (col_w + 6)
        pdf.draw_rect(box_x, 590, col_w, 42, fill_color=(0.97, 0.98, 0.99), border_color=(0.85, 0.88, 0.92))
        pdf.draw_text(label, box_x + 8, 617, font_size=8, bold=False, color=(0.45, 0.48, 0.55))
        pdf.draw_text(val, box_x + 8, 599, font_size=12, bold=True, color=(0.15, 0.22, 0.4))

    # Progress Bar visual & Performance Classification
    pdf.draw_text("Percentual de Conclusão Global:", 40, 570, font_size=9, bold=True, color=(0.25, 0.3, 0.38))
    pdf.draw_rect(40, 550, 515, 12, fill_color=(0.9, 0.92, 0.94))
    fill_w = max(0.0, min(515.0, (overall_progress / 100.0) * 515.0))
    if fill_w > 0:
        pdf.draw_rect(40, 550, fill_w, 12, fill_color=(0.2, 0.6, 0.35))

    # Performance Diagnosis
    if total_tasks == 0:
        perf_status = "Sem tarefas cadastradas no momento"
        perf_color = (0.45, 0.45, 0.45)
    elif overall_progress >= 75.0:
        perf_status = "Desempenho Excelente - Alto índice de conclusão acadêmica"
        perf_color = (0.12, 0.55, 0.25)
    elif overall_progress >= 50.0:
        perf_status = "Desempenho Regular - Bom andamento e entregas em dia"
        perf_color = (0.15, 0.40, 0.70)
    else:
        perf_status = "Atenção Recomendada - Volume significativo de tarefas pendentes"
        perf_color = (0.75, 0.35, 0.10)

    pdf.draw_text(f"Diagnóstico: {perf_status}", 40, 532, font_size=9, bold=True, color=perf_color)

    # Section: Subjects Performance Table
    current_y = 505
    pdf.draw_text("DESEMPENHO POR DISCIPLINA", 40, current_y, font_size=11, bold=True, color=(0.15, 0.2, 0.3))
    current_y -= 8
    pdf.draw_line(40, current_y, 555, current_y, line_width=1, color=(0.8, 0.82, 0.85))
    current_y -= 18

    # Table Header
    pdf.draw_rect(40, current_y, 515, 18, fill_color=(0.92, 0.94, 0.97))
    pdf.draw_text("Disciplina", 50, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text("Professor(a) / Carga", 215, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text("Concluídas / Total", 375, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text("Progresso (%)", 475, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    current_y -= 16

    if subjects_summary:
        for s in subjects_summary:
            pdf.draw_line(40, current_y + 14, 555, current_y + 14, line_width=0.5, color=(0.9, 0.9, 0.9))
            s_name = clean_display_text(s.get("subject_name", "-"))[:24]

            # Look up teacher name directly from item or from subj_lookup
            t_name = get_subject_teacher_name(s)
            sid = s.get("subject_id") or s.get("id")
            if not t_name and sid in subj_lookup:
                t_name = get_subject_teacher_name(subj_lookup[sid])

            prof_str = t_name if t_name else "Não informado"
            h_val = s.get("hours") or (subj_lookup.get(sid, {}).get("hours") if sid in subj_lookup else None)
            if h_val:
                prof_str += f" ({h_val}h)"

            prof_info = clean_display_text(prof_str)[:28]

            tot_tasks_s = s.get("total_tasks", 0)
            comp_tasks_s = s.get("completed_tasks", 0)
            ratio_str = f"{comp_tasks_s} / {tot_tasks_s}"

            pdf.draw_text(s_name, 50, current_y + 2, font_size=9, bold=False, color=(0.1, 0.1, 0.1))
            pdf.draw_text(prof_info, 215, current_y + 2, font_size=8.5, bold=False, color=(0.35, 0.35, 0.35))
            pdf.draw_text(ratio_str, 395, current_y + 2, font_size=9, bold=False, color=(0.1, 0.1, 0.1))
            pct_val = s.get("progress_percentage", 0.0)
            pdf.draw_text(f"{pct_val:.1f}%", 485, current_y + 2, font_size=9, bold=True, color=(0.15, 0.45, 0.25))
            current_y -= 16
    else:
        pdf.draw_text("Nenhuma disciplina cadastrada no período.", 50, current_y + 2, font_size=9, bold=False, color=(0.5, 0.5, 0.5))
        current_y -= 16

    # Section: Task List Breakdown
    current_y -= 12
    pdf.draw_text("LISTAGEM GERAL DE TAREFAS ACADÊMICAS", 40, current_y, font_size=11, bold=True, color=(0.15, 0.2, 0.3))
    current_y -= 8
    pdf.draw_line(40, current_y, 555, current_y, line_width=1, color=(0.8, 0.82, 0.85))
    current_y -= 18

    # Table Header for tasks
    pdf.draw_rect(40, current_y, 515, 18, fill_color=(0.92, 0.94, 0.97))
    pdf.draw_text("Título da Tarefa", 50, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text("Disciplina", 260, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text("Prazo", 380, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    pdf.draw_text("Status", 470, current_y + 5, font_size=9, bold=True, color=(0.2, 0.25, 0.35))
    current_y -= 16

    status_labels = {
        "completed": "Concluída",
        "in_progress": "Em Andamento",
        "pending": "Pendente",
    }

    if all_tasks:
        for t in all_tasks[:15]:  # List tasks on page
            if current_y < 60:
                break
            pdf.draw_line(40, current_y + 14, 555, current_y + 14, line_width=0.5, color=(0.9, 0.9, 0.9))
            task_title = clean_display_text(t.get("title", "Sem Título"))[:32]
            
            sub_id = t.get("subject_id")
            disc_name = subj_map.get(sub_id, "Geral")[:18]

            due_raw = t.get("due_date")
            task_due = str(due_raw)[:10] if due_raw else "Não definida"

            st_key = str(t.get("status", "pending")).lower()
            st_text = status_labels.get(st_key, st_key.title())

            st_color = (0.1, 0.5, 0.2) if st_key == "completed" else ((0.8, 0.5, 0.1) if st_key == "in_progress" else (0.4, 0.4, 0.4))

            pdf.draw_text(task_title, 50, current_y + 2, font_size=8.5, bold=False, color=(0.1, 0.1, 0.1))
            pdf.draw_text(disc_name, 260, current_y + 2, font_size=8.5, bold=False, color=(0.35, 0.35, 0.35))
            pdf.draw_text(task_due, 380, current_y + 2, font_size=8.5, bold=False, color=(0.3, 0.3, 0.3))
            pdf.draw_text(st_text, 470, current_y + 2, font_size=8.5, bold=True, color=st_color)
            current_y -= 15
    else:
        pdf.draw_text("Nenhuma tarefa registrada no momento.", 50, current_y + 2, font_size=9, bold=False, color=(0.5, 0.5, 0.5))
        current_y -= 16

    # Footer note
    pdf.draw_line(40, 45, 555, 45, line_width=0.5, color=(0.85, 0.85, 0.85))
    pdf.draw_text("Relatório gerado automaticamente pelo EduTrack AI", 40, 32, font_size=8, bold=False, color=(0.5, 0.5, 0.5))
    pdf.draw_text("Documento Acadêmico - Uso Interno", 410, 32, font_size=8, bold=False, color=(0.5, 0.5, 0.5))

    # Save to destination
    pdf_bytes = pdf.build()
    abs_output = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output) or ".", exist_ok=True)
    with open(abs_output, "wb") as f:
        f.write(pdf_bytes)

    return abs_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera relatório de desempenho do aluno em formato PDF.")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="relatorio_desempenho.pdf",
        help="Caminho do arquivo PDF de saída (padrão: relatorio_desempenho.pdf).",
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="Token de autenticação do Xano.",
    )

    args = parser.parse_args()
    result_path = generate_performance_report_pdf(output_path=args.output, auth_token=args.token)
    print(f"Relatório gerado com sucesso em: {result_path}")
