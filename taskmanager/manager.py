"""
TaskManager module.
Provides high-level CRUD business operations for managing tasks.
"""

from typing import List, Optional
from taskmanager.task import Task, VALID_STATUSES
from taskmanager.storage import Storage


class TaskManager:
    """Business logic class to manage collection of tasks."""

    def __init__(self, storage: Optional[Storage] = None) -> None:
        self.storage = storage if storage is not None else Storage()
        self.tasks: List[Task] = self.storage.load_tasks()

    def _get_next_id(self) -> int:
        """Calculate next available unique task ID."""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def _save(self) -> None:
        """Persist current tasks state to storage."""
        self.storage.save_tasks(self.tasks)

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task."""
        new_id = self._get_next_id()
        task = Task(task_id=new_id, title=title, description=description, status="todo")
        self.tasks.append(task)
        self._save()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Find task by ID. Returns None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        """List all tasks or filter by status."""
        if status is not None:
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status filter '{status}'. Choose from {VALID_STATUSES}")
            return [task for task in self.tasks if task.status == status]
        return list(self.tasks)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Task:
        """Update an existing task's title, description, or status."""
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found.")

        task.update(title=title, description=description, status=status)
        self._save()
        return task

    def delete_task(self, task_id: int) -> Task:
        """Delete task by ID."""
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found.")

        self.tasks.remove(task)
        self._save()
        return task

    def mark_status(self, task_id: int, status: str) -> Task:
        """Mark task with new status ('todo', 'in_progress', or 'done')."""
        return self.update_task(task_id, status=status)
