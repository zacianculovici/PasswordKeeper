import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "MainPage.py"

spec = importlib.util.spec_from_file_location("MainPage", MODULE_PATH)
MainPage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MainPage)


class AccountManagerTests(unittest.TestCase):
    def setUp(self):
        MainPage.testing_credentials = {"username": "testuser", "password": "testpass"}

    def test_check_account_availability_allows_new_username(self):
        self.assertTrue(MainPage.AccountManager.check_account_availability(None, "newuser"))

    def test_create_account_and_verify_account_work(self):
        self.assertTrue(MainPage.AccountManager.create_account(None, "newuser", "secret123"))
        self.assertTrue(MainPage.AccountManager.verify_account(None, "newuser", "secret123"))

    def test_verify_account_rejects_wrong_password(self):
        self.assertTrue(MainPage.AccountManager.create_account(None, "newuser", "secret123"))
        self.assertFalse(MainPage.AccountManager.verify_account(None, "newuser", "wrongpass"))


if __name__ == "__main__":
    unittest.main()
