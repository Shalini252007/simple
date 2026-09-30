"""
Task model module.
Defines the Task data class and valid statuses.
"""

from datetime import datetime
from typing import Any, Dict


VALID_STATUSES = ["todo", "in_progress", "done"]


class Task:
    """Represents a single task in the task manager."""

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: str = "todo",
        created_at: str | None = None,
        updated_at: str | None = None,
    ) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}")
        if not title.strip():
            raise ValueError("Task title cannot be empty.")

        now_str = datetime.now().isoformat(timespec="seconds")
        self.id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.status = status
        self.created_at = created_at if created_at else now_str
        self.updated_at = updated_at if updated_at else now_str

    def update(self, title: str | None = None, description: str | None = None, status: str | None = None) -> None:
        """Update task attributes and refresh updated_at timestamp."""
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty.")
            self.title = title.strip()

        if description is not None:
            self.description = description.strip()

        if status is not None:
            if status not in VALID_STATUSES:
                raise ValueError(f"Invalid status '{status}'. Must be one of {VALID_STATUSES}")
            self.status = status

        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> Dict[str, Any]:
        """Convert task object to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create a Task object from dictionary representation."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def __repr__(self) -> str:
        return f"<Task id={self.id} title={self.title!r} status={self.status!r}>"
