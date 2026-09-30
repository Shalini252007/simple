"""
Tests for CLI interface module.
"""

import io
import os
import tempfile
import unittest
from unittest.mock import patch
from taskmanager.cli import run_cli


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_cli_add_and_list(self):
        # Add task
        add_args = ["-f", self.temp_file.name, "add", "CLI Task", "-d", "CLI Description"]
        ret = run_cli(add_args)
        self.assertEqual(ret, 0)

        # List tasks
        list_args = ["-f", self.temp_file.name, "list"]
        stdout_capture = io.StringIO()
        with patch("sys.stdout", stdout_capture):
            ret = run_cli(list_args)

        self.assertEqual(ret, 0)
        output = stdout_capture.getvalue()
        self.assertIn("CLI Task", output)

    def test_cli_mark_status_and_delete(self):
        # Add task
        run_cli(["-f", self.temp_file.name, "add", "Status Task"])

        # Mark status
        mark_args = ["-f", self.temp_file.name, "mark-status", "1", "done"]
        ret = run_cli(mark_args)
        self.assertEqual(ret, 0)

        # Delete task
        delete_args = ["-f", self.temp_file.name, "delete", "1"]
        ret = run_cli(delete_args)
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
