"""
Tests for Task model.
"""

import unittest
from taskmanager.task import Task


class TestTaskModel(unittest.TestCase):

    def test_task_creation_defaults(self):
        task = Task(task_id=1, title="Buy groceries")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, "todo")
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_invalid_status_raises_error(self):
        with self.assertRaises(ValueError):
            Task(task_id=1, title="Invalid task", status="invalid_status")

    def test_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            Task(task_id=1, title="   ")

    def test_task_update(self):
        task = Task(task_id=1, title="Old title", description="Old desc")
        task.update(title="New title", status="in_progress")
        self.assertEqual(task.title, "New title")
        self.assertEqual(task.description, "Old desc")
        self.assertEqual(task.status, "in_progress")

    def test_dict_conversion(self):
        task = Task(task_id=2, title="Read book", description="Chapter 1", status="done")
        task_dict = task.to_dict()
        self.assertEqual(task_dict["id"], 2)
        self.assertEqual(task_dict["title"], "Read book")

        task_recreated = Task.from_dict(task_dict)
        self.assertEqual(task_recreated.id, task.id)
        self.assertEqual(task_recreated.title, task.title)
        self.assertEqual(task_recreated.status, task.status)


if __name__ == "__main__":
    unittest.main()
