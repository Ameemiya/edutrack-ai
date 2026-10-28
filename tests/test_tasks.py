import unittest
from services import task_service


class TestTaskService(unittest.TestCase):
    def setUp(self):
        task_service._in_memory_tasks = []
        task_service._task_id_counter = 1

    def test_create_and_list_task(self):
        task = task_service.create_task(
            title="Estudar Streamlit",
            description="Revisar componentes de frontend",
            due_date="2026-03-01",
            status="pending",
        )
        self.assertEqual(task["title"], "Estudar Streamlit")
        self.assertEqual(task["status"], "pending")

        tasks = task_service.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], task["id"])

    def test_validation_title_required(self):
        with self.assertRaises(ValueError):
            task_service.create_task(title="")
        with self.assertRaises(ValueError):
            task_service.create_task(title="   ")

    def test_fetch_tasks_without_token(self):
        ok, msg = task_service.fetch_tasks(auth_token=None)
        self.assertFalse(ok)
        self.assertIn("não autenticado", msg.lower())

    def test_update_and_delete_task(self):
        task = task_service.create_task(
            title="Tarefa Teste",
            description="Descrição teste",
            status="pending",
        )
        task_id = task["id"]

        updated = task_service.update_task(task_id, status="completed", title="Tarefa Atualizada")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["status"], "completed")
        self.assertEqual(updated["title"], "Tarefa Atualizada")

        # Status validation
        with self.assertRaises(ValueError):
            task_service.update_task(task_id, status="invalid_status")

        # Delete
        success = task_service.delete_task(task_id)
        self.assertTrue(success)
        self.assertEqual(len(task_service.list_tasks()), 0)


if __name__ == "__main__":
    unittest.main()

