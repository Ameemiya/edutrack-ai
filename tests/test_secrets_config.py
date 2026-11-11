import os
import unittest
from unittest.mock import patch, MagicMock
from services import auth_service, subject_service, task_service, report_service


class TestSecretsConfiguration(unittest.TestCase):
    def test_secrets_precedence_over_environ(self):
        # Mock streamlit secrets and runtime
        mock_secrets = {
            "XANO_AUTH_API_URL": "https://secrets.xano.io/api:auth",
            "XANO_SUBJECTS_API_URL": "https://secrets.xano.io/api:subjects",
            "XANO_TASKS_API_URL": "https://secrets.xano.io/api:tasks",
            "XANO_REPORTS_API_URL": "https://secrets.xano.io/api:reports",
            "XANO_AUTH_TOKEN": "secrets_token_123",
        }
        
        with patch.dict(os.environ, {
            "XANO_AUTH_API_URL": "https://env.xano.io/api:auth",
            "XANO_SUBJECTS_API_URL": "https://env.xano.io/api:subjects",
            "XANO_TASKS_API_URL": "https://env.xano.io/api:tasks",
            "XANO_REPORTS_API_URL": "https://env.xano.io/api:reports",
            "XANO_AUTH_TOKEN": "env_token_456",
        }):
            # Patch st.secrets on services
            with patch.object(auth_service, "_st_runtime_exists", return_value=True), \
                 patch.object(auth_service.st, "secrets", mock_secrets, create=True), \
                 patch.object(subject_service, "_st_runtime_exists", return_value=True), \
                 patch.object(subject_service.st, "secrets", mock_secrets, create=True), \
                 patch.object(task_service, "_st_runtime_exists", return_value=True), \
                 patch.object(task_service.st, "secrets", mock_secrets, create=True), \
                 patch.object(report_service, "_st_runtime_exists", return_value=True), \
                 patch.object(report_service.st, "secrets", mock_secrets, create=True):

                self.assertEqual(auth_service.get_auth_api_url(), "https://secrets.xano.io/api:auth")
                self.assertEqual(subject_service._get_api_url(), "https://secrets.xano.io/api:subjects")
                self.assertEqual(task_service._get_api_url(), "https://secrets.xano.io/api:tasks")
                self.assertEqual(report_service.get_reports_api_url(), "https://secrets.xano.io/api:reports")
                self.assertEqual(subject_service._get_auth_token(), "secrets_token_123")
                self.assertEqual(task_service._get_auth_token(), "secrets_token_123")

    def test_environ_fallback_when_secrets_absent(self):
        with patch.dict(os.environ, {
            "XANO_AUTH_API_URL": "https://env.xano.io/api:auth",
            "XANO_SUBJECTS_API_URL": "https://env.xano.io/api:subjects",
            "XANO_TASKS_API_URL": "https://env.xano.io/api:tasks",
            "XANO_REPORTS_API_URL": "https://env.xano.io/api:reports",
            "XANO_AUTH_TOKEN": "env_token_fallback",
        }):
            # When secrets has no keys
            with patch.object(auth_service, "_st_runtime_exists", return_value=False), \
                 patch.object(subject_service, "_st_runtime_exists", return_value=False), \
                 patch.object(task_service, "_st_runtime_exists", return_value=False), \
                 patch.object(report_service, "_st_runtime_exists", return_value=False):

                self.assertEqual(auth_service.get_auth_api_url(), "https://env.xano.io/api:auth")
                self.assertEqual(subject_service._get_api_url(), "https://env.xano.io/api:subjects")
                self.assertEqual(task_service._get_api_url(), "https://env.xano.io/api:tasks")
                self.assertEqual(report_service.get_reports_api_url(), "https://env.xano.io/api:reports")
                self.assertEqual(subject_service._get_auth_token(), "env_token_fallback")
                self.assertEqual(task_service._get_auth_token(), "env_token_fallback")


if __name__ == "__main__":
    unittest.main()

