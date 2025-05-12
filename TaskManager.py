import json
from Task import Task

class TaskManager:
    def __init__(self, file_path="tasks.json"):
        self.tasks = []
        self.file_path = file_path
        self.load_tasks()

    def add_task(self, task_name, priority="Medium", due_date=None, category="General"):
        task = Task(task_name, priority, due_date, category)
        self.tasks.append(task)
        self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def remove_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()

    def sort_tasks(self, key, reverse=False):
        if key == "status":
            self.tasks.sort(key=lambda x: x.is_completed, reverse=reverse)
        elif key == "name":
            self.tasks.sort(key=lambda x: x.name.lower(), reverse=reverse)
        elif key == "priority":
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            self.tasks.sort(key=lambda x: priority_order.get(x.priority, 0), reverse=reverse)
        elif key == "due_date":
            self.tasks.sort(key=lambda x: x.due_date, reverse=reverse)
        elif key == "category":
            self.tasks.sort(key=lambda x: x.category.lower(), reverse=reverse)
        self.save_tasks()

    def filter_tasks(self, status=None, category=None):
        filtered = self.tasks
        if status == "Completed":
            filtered = [t for t in filtered if t.is_completed]
        elif status == "Pending":
            filtered = [t for t in filtered if not t.is_completed]
        if category and category != "All":
            filtered = [t for t in filtered if t.category == category]
        return filtered

    def save_tasks(self):
        with open(self.file_path, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def load_tasks(self):
        try:
            with open(self.file_path, "r") as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(data) for data in tasks_data]
        except FileNotFoundError:
            self.tasks = []