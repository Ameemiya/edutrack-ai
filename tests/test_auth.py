import unittest
from unittest.mock import patch, MagicMock
from services import auth_service


class TestAuthService(unittest.TestCase):
    def test_get_auth_api_url(self):
        url = auth_service.get_auth_api_url()
        self.assertTrue(url.startswith("http"))
        self.assertFalse(url.endswith("/"))

    def test_signup_validation(self):
        ok, msg = auth_service.signup("", "test@test.com", "123")
        self.assertFalse(ok)
        self.assertIn("nome", msg.lower())

        ok, msg = auth_service.signup("User", "", "123")
        self.assertFalse(ok)
        self.assertIn("e-mail", msg.lower())

        ok, msg = auth_service.signup("User", "test@test.com", "")
        self.assertFalse(ok)
        self.assertIn("senha", msg.lower())

    def test_login_validation(self):
        ok, msg = auth_service.login("", "123")
        self.assertFalse(ok)
        self.assertIn("e-mail", msg.lower())

        ok, msg = auth_service.login("test@test.com", "")
        self.assertFalse(ok)
        self.assertIn("senha", msg.lower())

    def test_get_me_validation(self):
        ok, msg = auth_service.get_me("")
        self.assertFalse(ok)
        self.assertIn("token", msg.lower())

    @patch("requests.post")
    def test_signup_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"authToken": "jwt_token_123"}'
        mock_resp.json.return_value = {"authToken": "jwt_token_123"}
        mock_post.return_value = mock_resp

        ok, res = auth_service.signup("Alice", "alice@example.com", "pass123")
        self.assertTrue(ok)
        self.assertEqual(res["authToken"], "jwt_token_123")

    @patch("requests.post")
    def test_login_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"authToken": "jwt_token_456"}'
        mock_resp.json.return_value = {"authToken": "jwt_token_456"}
        mock_post.return_value = mock_resp

        ok, res = auth_service.login("alice@example.com", "pass123")
        self.assertTrue(ok)
        self.assertEqual(res["authToken"], "jwt_token_456")

    @patch("requests.get")
    def test_get_me_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"id": 1, "name": "Alice", "email": "alice@example.com"}'
        mock_resp.json.return_value = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        mock_get.return_value = mock_resp

        ok, res = auth_service.get_me("jwt_token_456")
        self.assertTrue(ok)
        self.assertEqual(res["name"], "Alice")
        self.assertEqual(res["id"], 1)


if __name__ == "__main__":
    unittest.main()

