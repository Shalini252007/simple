"""
Tests for Storage module.
"""

import os
import tempfile
import unittest
from taskmanager.storage import Storage
from taskmanager.task import Task


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.storage = Storage(filepath=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
        if os.path.exists(f"{self.temp_file.name}.tmp"):
            os.remove(f"{self.temp_file.name}.tmp")

    def test_load_non_existent_file(self):
        storage = Storage(filepath="non_existent_file_12345.json")
        tasks = storage.load_tasks()
        self.assertEqual(tasks, [])

    def test_save_and_load_tasks(self):
        t1 = Task(task_id=1, title="Task 1", description="Desc 1")
        t2 = Task(task_id=2, title="Task 2", status="done")
        self.storage.save_tasks([t1, t2])

        loaded = self.storage.load_tasks()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].id, 1)
        self.assertEqual(loaded[0].title, "Task 1")
        self.assertEqual(loaded[1].id, 2)
        self.assertEqual(loaded[1].status, "done")


if __name__ == "__main__":
    unittest.main()
