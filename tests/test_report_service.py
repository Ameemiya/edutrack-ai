import unittest
from services import report_service, subject_service, task_service


class TestReportService(unittest.TestCase):
    def setUp(self):
        # Reset local mock stores
        subject_service._in_memory_db = []
        subject_service._id_counter = 1
        task_service._in_memory_tasks = []
        task_service._task_id_counter = 1

    def test_generate_student_pdf_report(self):
        # Create a test subject and task
        s = subject_service.create_subject(name="Engenharia de Software", hours=80)
        task_service.create_task(
            title="Modelagem UML",
            status="completed",
            subject_id=s["id"],
        )

        pdf_bytes = report_service.generate_student_pdf_report(output_path="test_unit_report.pdf")
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(len(pdf_bytes) > 0)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-1.4"))
        self.assertTrue(pdf_bytes.strip().endswith(b"%%EOF"))
        self.assertIn(b"/WinAnsiEncoding", pdf_bytes)

    def test_generate_student_pdf_report_with_student_data(self):
        user_info = {
            "id": 42,
            "name": "Maria Silva",
            "email": "maria.silva@edutrack.ai",
        }
        test_subjects = [
            {"id": 1, "name": "Cálculo I", "teacher": "Prof. Newton", "hours": 60},
        ]
        test_tasks = [
            {"id": 101, "title": "Lista de Derivadas", "status": "completed", "subject_id": 1, "due_date": "2026-12-01"},
            {"id": 102, "title": "Prova de Integrais", "status": "pending", "subject_id": 1, "due_date": "2026-12-15"},
        ]

        pdf_bytes = report_service.generate_student_pdf_report(
            output_path="test_student_report.pdf",
            user_data=user_info,
            subjects=test_subjects,
            tasks=test_tasks,
        )
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(len(pdf_bytes) > 0)
        self.assertTrue(pdf_bytes.startswith(b"%PDF-1.4"))
        # Verify student details are encoded in PDF
        self.assertIn(b"Maria Silva", pdf_bytes)
        self.assertIn(b"42", pdf_bytes)
        self.assertIn(b"maria.silva@edutrack.ai", pdf_bytes)
        # Verify teacher / professor name is encoded in PDF
        self.assertIn(b"Prof. Newton", pdf_bytes)
        # Verify tasks are not duplicated
        self.assertEqual(pdf_bytes.count(b"Lista de Derivadas"), 1)
        self.assertEqual(pdf_bytes.count(b"Prova de Integrais"), 1)

    def test_generate_student_pdf_report_with_professor_alias(self):
        user_info = {"id": 10, "name": "Aluno Teste", "email": "aluno@edutrack.ai"}
        subjects_with_prof = [
            {"id": 2, "name": "Banco de Dados", "professor": "Dra. Ada Lovelace", "hours": 40}
        ]
        pdf_bytes = report_service.generate_student_pdf_report(
            output_path="test_student_prof.pdf",
            user_data=user_info,
            subjects=subjects_with_prof,
            tasks=[],
        )
        self.assertIn(b"Dra. Ada Lovelace", pdf_bytes)

    def test_fetch_report_data_without_token(self):
        ok, msg = report_service.fetch_report_data_from_xano(auth_token=None)
        self.assertFalse(ok)
        self.assertIn("não autenticado", msg.lower())

    def tearDown(self):
        import os
        for p in ["test_unit_report.pdf", "test_student_report.pdf", "test_student_prof.pdf"]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass


if __name__ == "__main__":
    unittest.main()

