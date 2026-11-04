## Why

Students and academic administrators need a formal, exportable document summarizing student academic performance across subjects and tasks. Providing an automated Python script to generate a formatted PDF report and a corresponding Xano endpoint to deliver/download the report file enables students to export and archive their academic records easily.

## What Changes

- Add a Python script `scripts/generate_performance_report_pdf.py` that aggregates academic performance data (subjects, completed vs. pending tasks, progress percentage) and renders an academic performance report in PDF format.
- Add an authenticated Xano API query endpoint (e.g. `GET /reports/download` or `GET /reports/performance_pdf`) to download or serve the generated performance report file.

## Capabilities

### New Capabilities
- `student-performance-report`: Generation of an academic performance summary PDF via Python script and an authenticated Xano endpoint to download the report file.

### Modified Capabilities

## Impact

- New script: `scripts/generate_performance_report_pdf.py` using Python (such as ReportLab or FPDF).
- New Xano API endpoint file in `api/reports/` for report download.
- No breaking changes to existing endpoints or database tables.

