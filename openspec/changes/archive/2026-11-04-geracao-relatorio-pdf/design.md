## Context

The application EduTrack AI manages subjects and academic tasks, and calculates progress percentages. Users need an exportable PDF report summarizing student performance across all subjects and tasks, as well as an endpoint in Xano allowing users to download or access this report securely.

## Goals / Non-Goals

**Goals:**
- Provide a Python script `scripts/generate_performance_report_pdf.py` that gathers student performance data (subjects, total tasks, completed tasks, completion percentage) and outputs a formatted PDF document.
- Support running the script via CLI (`python scripts/generate_performance_report_pdf.py --output report.pdf [--token <TOKEN>]`).
- Define an authenticated Xano API query in `api/reports/download_pdf_GET.xs` (or `api/reports/reports_download_GET.xs`) with `auth = "user"` and appropriate download headers (`Content-Type: application/pdf`, `Content-Disposition: attachment; filename="relatorio_desempenho.pdf"`).

**Non-Goals:**
- Do not create extra unrequested Streamlit UI pages or email dispatch mechanisms.
- Do not push or deploy files to the live Xano server (per AGENTS.md Rule #2).

## Decisions

- **Decision 1: Report generation architecture**: The Python script in `scripts/generate_performance_report_pdf.py` will reuse the existing calculation and CRUD services (`calculate_progress.py`, `subject_service.py`, `task_service.py`) to gather data, ensuring consistent numbers across the app.
- **Decision 2: PDF generation library**: Implement report generation using a lightweight, self-contained PDF generator or `reportlab`/`fpdf2` fallback to ensure execution without blocking missing system dependencies.
- **Decision 3: Xano endpoint structure**: Create the query endpoint in `api/reports/` using XanoScript:
  - Verb: `GET`
  - Group: `Reports`
  - Auth: `user`
  - Header setup using `util.set_header` for file download response.

## Risks / Trade-offs

- [Risk] Running the script offline or without a valid token → [Mitigation] Script falls back to local data store when no auth token is provided, allowing testing and standalone operation.
- [Risk] Missing third-party PDF compilation libraries in certain Python environments → [Mitigation] Implement clean, standard PDF construction or specify dependency requirements clearly.

