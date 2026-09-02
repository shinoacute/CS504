import os
import unittest

import function_app


class FunctionAppTests(unittest.TestCase):
    def setUp(self):
        self.original_env = {
            name: os.environ.get(name)
            for name in [
                "AZURE_SQL_SERVER",
                "AZURE_SQL_DATABASE",
                "AZURE_SQL_USERNAME",
                "AZURE_SQL_PASSWORD",
            ]
        }

    def tearDown(self):
        for key, value in self.original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_get_connection_string_sets_values_from_environment(self):
        os.environ["AZURE_SQL_SERVER"] = "cityuweek8thao.database.windows.net"
        os.environ["AZURE_SQL_DATABASE"] = "week8-thao"
        os.environ["AZURE_SQL_USERNAME"] = "thao-admin"
        os.environ["AZURE_SQL_PASSWORD"] = "Buihoangco123."

        connection_string = function_app.get_connection_string()

        self.assertIn("SERVER=server.database.windows.net", connection_string)
        self.assertIn("DATABASE=appdb", connection_string)
        self.assertIn("UID=appuser", connection_string)
        self.assertIn("PWD=secret", connection_string)

    def test_get_connection_string_requires_all_values(self):
        for key in [
            "AZURE_SQL_SERVER",
            "AZURE_SQL_DATABASE",
            "AZURE_SQL_USERNAME",
            "AZURE_SQL_PASSWORD",
        ]:
            os.environ.pop(key, None)

        with self.assertRaises(RuntimeError):
            function_app.get_connection_string()


if __name__ == "__main__":
    unittest.main()
