"""
Tests for TaskManager module.
"""

import os
import tempfile
import unittest
from taskmanager.manager import TaskManager
from taskmanager.storage import Storage


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.storage = Storage(filepath=self.temp_file.name)
        self.manager = TaskManager(storage=self.storage)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_task(self):
        task = self.manager.add_task(title="New Task", description="Description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "New Task")
        self.assertEqual(len(self.manager.list_tasks()), 1)

    def test_get_task(self):
        t1 = self.manager.add_task(title="Task A")
        retrieved = self.manager.get_task(t1.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.title, "Task A")

        self.assertIsNone(self.manager.get_task(999))

    def test_filter_tasks_by_status(self):
        t1 = self.manager.add_task(title="Task 1")
        t2 = self.manager.add_task(title="Task 2")
        self.manager.mark_status(t2.id, "done")

        todo_tasks = self.manager.list_tasks(status="todo")
        done_tasks = self.manager.list_tasks(status="done")

        self.assertEqual(len(todo_tasks), 1)
        self.assertEqual(todo_tasks[0].id, t1.id)
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].id, t2.id)

    def test_update_task(self):
        t = self.manager.add_task(title="Initial")
        updated = self.manager.update_task(t.id, title="Updated Title", description="New Desc")
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.description, "New Desc")

    def test_delete_task(self):
        t = self.manager.add_task(title="To Delete")
        self.assertEqual(len(self.manager.list_tasks()), 1)
        deleted = self.manager.delete_task(t.id)
        self.assertEqual(deleted.id, t.id)
        self.assertEqual(len(self.manager.list_tasks()), 0)

    def test_delete_non_existent_task_raises_error(self):
        with self.assertRaises(KeyError):
            self.manager.delete_task(999)


if __name__ == "__main__":
    unittest.main()
