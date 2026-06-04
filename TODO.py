import json
import os

shards = {
    0: [],
    1: [],
    2: []
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "todo_data.json")

def get_next_id():
    max_id = 0

    for shard in shards.values():
        for task in shard:
            if task["id"] > max_id:
                max_id = task["id"]

    return max_id + 1

def save_tasks():
    with open(DATA_FILE, "w") as file:
        json.dump(shards, file, indent=4)

def load_tasks():
    global shards

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        shards = {
            int(key): value
            for key, value in data.items()
        }

def addTask(name):
    taskId = get_next_id()

    newTask = {
        "id": taskId,
        "task": name
    }

    shard_number = taskId % 3
    shards[shard_number].append(newTask)
    save_tasks()

    print(f"Task '{name}' added successfully.")
    print(f"Stored in Shard {shard_number}")

def get_all_tasks():
    all_tasks = []

    for shard in shards.values():
        all_tasks.extend(shard)

    return sorted(all_tasks, key=lambda x: x["id"])

def viewTasks():
    all_tasks = get_all_tasks()

    if not all_tasks:
        print("\nYour To-Do List is currently empty.")
        return

    print("\n===== YOUR TO-DO LIST =====")
    for task in all_tasks:
        print(f"ID: {task['id']} -> {task['task']}")

def main():
    load_tasks()
    print("----------------------------------")
    print("Welcome to the To-Do List Manager!")
    while True:
        print("----------------------------------")
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Exit")
        choice = input("Select an option: ")
        if choice == "1":

            task_name = input("Enter the task description: ").strip()
            if task_name:
                addTask(task_name)
            else:
                print("Task cannot be empty.")
        elif choice == "2":
            viewTasks()
        elif choice == "3":
            print("Exiting To-Do List. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()