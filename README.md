# Task Manager CLI

A lightweight, clean, beginner-friendly Command-Line Interface (CLI) application for managing daily tasks and to-do lists, written in Python with no external dependencies required.

## Features

- **Add Tasks**: Create tasks with titles and optional descriptions.
- **List Tasks**: View all tasks or filter by status (`todo`, `in_progress`, `done`).
- **Update Tasks**: Modify task titles and descriptions.
- **Status Tracking**: Mark tasks as `todo`, `in_progress`, or `done`.
- **Delete Tasks**: Remove tasks by their ID.
- **JSON Storage**: Automatically persists tasks in a clean JSON format.
- **Zero External Dependencies**: Built entirely using Python's standard library (`argparse`, `json`, `datetime`, `unittest`).

---

## Project Structure

```text
.
├── README.md               # Documentation and usage guide
├── taskmanager/            # Main application package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface argument parsing & handling
│   ├── manager.py          # Core business logic and task collection management
│   ├── storage.py          # File persistence handler (JSON)
│   └── task.py             # Task data model and status constants
└── tests/                  # Unit test suite
    ├── __init__.py
    ├── test_cli.py         # CLI integration tests
    ├── test_manager.py     # TaskManager business logic tests
    ├── test_storage.py     # JSON persistence tests
    └── test_task.py        # Task model unit tests
```

---

## Setup & Requirements

- **Python Version**: Python 3.10 or higher.
- **Dependencies**: None! Uses standard library modules only.

### Installation

1. Clone or download this repository.
2. Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```

---

## Usage Guide

You can run the application directly using Python's module runner:

```bash
python3 -m taskmanager.cli [OPTIONS] COMMAND [ARGS]
```

### Options

- `-f`, `--file <path>`: Specify custom JSON storage file path (Default: `tasks.json`).

---

### Commands & Examples

#### 1. Add a Task
Add a new task with a title and optional description (`-d` / `--description`).

```bash
python3 -m taskmanager.cli add "Buy groceries" -d "Milk, Eggs, Bread"
python3 -m taskmanager.cli add "Write report"
```

#### 2. List Tasks
Display all tasks in a formatted table layout.

```bash
python3 -m taskmanager.cli list
```

Filter tasks by status using `-s` or `--status` (`todo`, `in_progress`, `done`):

```bash
python3 -m taskmanager.cli list -s todo
python3 -m taskmanager.cli list -s in_progress
python3 -m taskmanager.cli list -s done
```

#### 3. Change Task Status
Update the status of a task by ID to `todo`, `in_progress`, or `done`.

```bash
python3 -m taskmanager.cli mark-status 1 in_progress
python3 -m taskmanager.cli mark-status 1 done
```

#### 4. Update Task Details
Update the title or description of an existing task by ID.

```bash
python3 -m taskmanager.cli update 1 -t "Buy groceries and fruit"
python3 -m taskmanager.cli update 1 -d "Milk, Eggs, Bread, Apples"
```

#### 5. Delete a Task
Delete a task by its ID.

```bash
python3 -m taskmanager.cli delete 1
```

---

## Running Tests

The project includes unit tests covering all core modules and CLI operations.

Run the test suite using Python's built-in `unittest` module:

```bash
python3 -m unittest discover -s tests
```

To run with verbose test output:

```bash
python3 -m unittest discover -s tests -v
```

---

## License

This project is open-source and available under the MIT License.
