"""
CLI module for Task Manager.
Provides command-line argument parsing and formatted terminal output.
"""

import argparse
import sys
from typing import List, Optional
from taskmanager.manager import TaskManager
from taskmanager.task import VALID_STATUSES


def create_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="taskmanager",
        description="A lightweight and clean CLI Task Manager application.",
    )
    parser.add_argument(
        "--file",
        "-f",
        default="tasks.json",
        help="Path to JSON file used for task storage (default: tasks.json)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")
    add_parser.add_argument("-d", "--description", default="", help="Optional detailed description")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-s",
        "--status",
        choices=VALID_STATUSES,
        help="Filter tasks by status (todo, in_progress, done)",
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task title or description")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    update_parser.add_argument("-t", "--title", help="New title for the task")
    update_parser.add_argument("-d", "--description", help="New description for the task")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task by ID")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    # Mark status command
    mark_parser = subparsers.add_parser("mark-status", help="Change status of a task")
    mark_parser.add_argument("id", type=int, help="Task ID")
    mark_parser.add_argument("status", choices=VALID_STATUSES, help="New status")

    return parser


def format_status(status: str) -> str:
    """Format status for display."""
    symbols = {
        "todo": "[ ] Todo",
        "in_progress": "[-] In Progress",
        "done": "[x] Done",
    }
    return symbols.get(status, status)


def run_cli(args: Optional[List[str]] = None) -> int:
    """Execute CLI commands and handle outputs/errors."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 0

    from taskmanager.storage import Storage
    storage = Storage(filepath=parsed_args.file)
    manager = TaskManager(storage=storage)

    try:
        if parsed_args.command == "add":
            task = manager.add_task(title=parsed_args.title, description=parsed_args.description)
            print(f"Task added successfully! (ID: {task.id})")

        elif parsed_args.command == "list":
            tasks = manager.list_tasks(status=parsed_args.status)
            if not tasks:
                print("No tasks found.")
            else:
                print("\n" + "=" * 60)
                print(f"{'ID':<5} {'Status':<15} {'Title':<25} {'Updated At'}")
                print("=" * 60)
                for t in tasks:
                    desc_str = f"\n      Description: {t.description}" if t.description else ""
                    print(f"{t.id:<5} {format_status(t.status):<15} {t.title:<25} {t.updated_at}{desc_str}")
                print("=" * 60 + "\n")

        elif parsed_args.command == "update":
            if parsed_args.title is None and parsed_args.description is None:
                print("Error: Please provide at least --title or --description to update.")
                return 1
            task = manager.update_task(
                task_id=parsed_args.id,
                title=parsed_args.title,
                description=parsed_args.description,
            )
            print(f"Task {task.id} updated successfully.")

        elif parsed_args.command == "delete":
            task = manager.delete_task(task_id=parsed_args.id)
            print(f"Task {task.id} ('{task.title}') deleted successfully.")

        elif parsed_args.command == "mark-status":
            task = manager.mark_status(task_id=parsed_args.id, status=parsed_args.status)
            print(f"Task {task.id} status updated to '{task.status}'.")

        return 0

    except (KeyError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run_cli())
