import unittest
import json
from services import subject_service, task_service
from scripts.calculate_progress import (
    calculate_subject_progress,
    get_subject_progress_json,
    calculate_all_subjects_progress,
)


class TestCalculateProgress(unittest.TestCase):
    def setUp(self):
        # Reset local mock stores
        subject_service._in_memory_db = []
        subject_service._id_counter = 1
        task_service._in_memory_tasks = []
        task_service._task_id_counter = 1

        # Create a test subject
        self.subject = subject_service.create_subject(
            name="Matemática Aplicada",
            teacher="Prof. Euler",
            hours=60,
        )
        self.subject_id = self.subject["id"]

    def test_progress_with_completed_and_pending_tasks(self):
        # Create 1 completed task and 1 pending task
        task_service.create_task(
            title="Lista 1",
            status="completed",
            subject_id=self.subject_id,
        )
        task_service.create_task(
            title="Lista 2",
            status="pending",
            subject_id=self.subject_id,
        )

        res = calculate_subject_progress(self.subject_id)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_tasks"], 2)
        self.assertEqual(res["completed_tasks"], 1)
        self.assertEqual(res["pending_tasks"], 1)
        self.assertEqual(res["progress_percentage"], 50.0)
        self.assertEqual(res["subject_name"], "Matemática Aplicada")

    def test_progress_with_no_tasks(self):
        # Subject with zero tasks
        res = calculate_subject_progress(self.subject_id)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_tasks"], 0)
        self.assertEqual(res["completed_tasks"], 0)
        self.assertEqual(res["pending_tasks"], 0)
        self.assertEqual(res["progress_percentage"], 0.0)

    def test_progress_with_non_existent_subject(self):
        res = calculate_subject_progress(99999)
        self.assertEqual(res["status"], "not_found")
        self.assertIn("error", res)
        self.assertEqual(res["progress_percentage"], 0.0)
        self.assertIsNone(res["subject_name"])

    def test_json_output_serialization(self):
        task_service.create_task(
            title="Trabalho Final",
            status="completed",
            subject_id=self.subject_id,
        )
        json_str = get_subject_progress_json(self.subject_id)
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["progress_percentage"], 100.0)
        self.assertEqual(parsed["completed_tasks"], 1)

    def test_calculate_all_subjects_progress(self):
        # Create second subject
        s2 = subject_service.create_subject(name="Física Moderna")
        task_service.create_task(
            title="Laboratório 1",
            status="completed",
            subject_id=self.subject_id,
        )
        task_service.create_task(
            title="Exercício Física",
            status="pending",
            subject_id=s2["id"],
        )

        res = calculate_all_subjects_progress()
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_subjects"], 2)
        self.assertEqual(res["total_tasks"], 2)
        self.assertEqual(res["total_completed_tasks"], 1)
        self.assertEqual(res["overall_progress_percentage"], 50.0)
        self.assertEqual(len(res["subjects"]), 2)


if __name__ == "__main__":
    unittest.main()

