"""
Storage module.
Handles loading and saving tasks from/to a JSON file.
"""

import json
import os
from typing import List, Dict, Any
from taskmanager.task import Task


class Storage:
    """Manages file storage for tasks using JSON."""

    def __init__(self, filepath: str = "tasks.json") -> None:
        self.filepath = filepath

    def load_tasks(self) -> List[Task]:
        """Load tasks from the JSON file. Returns empty list if file doesn't exist."""
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save list of tasks to the JSON file."""
        data = [task.to_dict() for task in tasks]
        # Write to temporary file first then replace atomically for safety
        temp_filepath = f"{self.filepath}.tmp"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_filepath, self.filepath)
