import json
import sys
import os

# File to store tasks
TASKS_FILE = 'tasks.json'

# Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Add a new task
def add_task(title):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": "not done"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{title}' added successfully!")

# Delete a task by ID
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    
    # Reassign IDs after deleting
    for index, task in enumerate(tasks):
        task["id"] = index + 1

    save_tasks(tasks)
    print(f"Task with ID {task_id} deleted successfully!")

# Update a task title by ID
def update_task(task_id, new_title):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            print(f"Task with ID {task_id} updated successfully!")
            break
    else:
        print("Task not found.")
    save_tasks(tasks)

# Change the status of a task
def change_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            print(f"Task with ID {task_id} marked as {status}!")
            break
    else:
        print("Task not found.")
    save_tasks(tasks)

# List tasks, optionally filtered by status
def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        if filter_status is None or task["status"] == filter_status:
            print(f"ID: {task['id']} | Title: {task['title']} | Status: {task['status']}")

# Main function to handle user commands
def main():
    if len(sys.argv) < 2:
        print("Please provide a command.")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a title for the task.")
            return
        title = " ".join(sys.argv[2:])
        add_task(title)

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide the ID of the task to delete.")
            return
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Task ID must be an integer.")

    elif command == "update":
        if len(sys.argv) < 4:
            print("Please provide the ID and new title for the task.")
            return
        try:
            task_id = int(sys.argv[2])
            new_title = " ".join(sys.argv[3:])
            update_task(task_id, new_title)
        except ValueError:
            print("Task ID must be an integer.")

    elif command == "mark":
        if len(sys.argv) < 4:
            print("Please provide the ID and new status (not done, in progress, or done).")
            return
        try:
            task_id = int(sys.argv[2])
            status = sys.argv[3]
            if status not in ["not done", "in progress", "done"]:
                print("Status must be 'not done', 'in progress' or 'done'.")
                return
            change_status(task_id, status)
        except ValueError:
            print("Task ID must be an integer.")

    elif command == "list":
        if len(sys.argv) == 3:
            filter_status = sys.argv[2]
            list_tasks(filter_status)
        else:
            list_tasks()

    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()
