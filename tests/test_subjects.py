import unittest
from services import subject_service


class TestSubjectService(unittest.TestCase):
    def setUp(self):
        # Reset the local in-memory database
        subject_service._in_memory_db = []
        subject_service._id_counter = 1

    def test_create_and_list_subject(self):
        subj = subject_service.create_subject(
            name="Inteligência Artificial",
            code="IA-301",
            professor="Dra. Santos",
            semester="2025/1",
            status="Ativa",
            notes="Estudos sobre LLMs e Agentes"
        )
        self.assertEqual(subj["name"], "Inteligência Artificial")
        self.assertEqual(subj["code"], "IA-301")
        self.assertEqual(subj["status"], "Ativa")

        subjects = subject_service.list_subjects()
        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0]["id"], subj["id"])

    def test_validation_name_required(self):
        with self.assertRaises(ValueError):
            subject_service.create_subject(name="")
        with self.assertRaises(ValueError):
            subject_service.create_subject(name="   ")

    def test_validation_status_invalid(self):
        with self.assertRaises(ValueError):
            subject_service.create_subject(name="Matemática", status="Pendente")

    def test_update_subject_status(self):
        subj = subject_service.create_subject(name="Engenharia de Software", status="Ativa")
        self.assertEqual(subject_service.count_active_subjects(), 1)

        updated = subject_service.update_subject(subj["id"], status="Concluída")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["status"], "Concluída")
        self.assertEqual(subject_service.count_active_subjects(), 0)

        # Check retrieval reflects change
        retrieved = subject_service.get_subject(subj["id"])
        self.assertEqual(retrieved["status"], "Concluída")

    def test_delete_subject(self):
        s1 = subject_service.create_subject(name="Disciplina 1")
        s2 = subject_service.create_subject(name="Disciplina 2")
        self.assertEqual(len(subject_service.list_subjects()), 2)

        deleted = subject_service.delete_subject(s1["id"])
        self.assertTrue(deleted)
        self.assertEqual(len(subject_service.list_subjects()), 1)
        self.assertIsNone(subject_service.get_subject(s1["id"]))

    def test_active_subjects_metric(self):
        subject_service.create_subject(name="Subj 1", status="Ativa")
        subject_service.create_subject(name="Subj 2", status="Ativa")
        subject_service.create_subject(name="Subj 3", status="Concluída")
        subject_service.create_subject(name="Subj 4", status="Trancada")

        self.assertEqual(subject_service.count_active_subjects(), 2)


if __name__ == "__main__":
    unittest.main()

