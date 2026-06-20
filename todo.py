#!/usr/bin/env python3
"""
Simple CLI to-do list with persistent JSON storage.

Usage:
    python todo.py add "Buy groceries"
    python todo.py list
    python todo.py done 2
    python todo.py remove 2
    python todo.py import tasks.txt
    python todo.py clear
"""

import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(text):
    tasks = load_tasks()
    tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print(f"Added: {text}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for i, task in enumerate(tasks, start=1):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i}. {task['text']}")


def complete_task(index):
    tasks = load_tasks()
    if not (1 <= index <= len(tasks)):
        print("Invalid task number.")
        return
    tasks[index - 1]["done"] = True
    save_tasks(tasks)
    print(f"Marked done: {tasks[index - 1]['text']}")


def remove_task(index):
    tasks = load_tasks()
    if not (1 <= index <= len(tasks)):
        print("Invalid task number.")
        return
    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"Removed: {removed['text']}")


def import_tasks(filepath):
    tasks = load_tasks()
    with open(filepath, "r") as f:
        new_tasks = [line.strip() for line in f if line.strip()]
    for text in new_tasks:
        tasks.append({"text": text, "done": False})
    save_tasks(tasks)
    print(f"Imported {len(new_tasks)} tasks.")


def clear_tasks():
    save_tasks([])
    print("All tasks cleared.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "list":
        list_tasks()
    elif command == "done" and len(sys.argv) > 2:
        complete_task(int(sys.argv[2]))
    elif command == "remove" and len(sys.argv) > 2:
        remove_task(int(sys.argv[2]))
    elif command == "import" and len(sys.argv) > 2:
        import_tasks(sys.argv[2])
    elif command == "clear":
        clear_tasks()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
