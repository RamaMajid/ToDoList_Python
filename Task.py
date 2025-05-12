from datetime import datetime

class Task:
    def __init__(self, name, priority="Medium", due_date=None, category="General"):
        self.name = name
        self.is_completed = False
        self.priority = priority
        self.due_date = due_date if due_date else datetime.now().strftime("%Y-%m-%d")
        self.category = category

    def toggle_status(self):
        self.is_completed = not self.is_completed

    def update(self, name=None, priority=None, due_date=None, category=None):
        if name:
            self.name = name
        if priority:
            self.priority = priority
        if due_date:
            self.due_date = due_date
        if category:
            self.category = category

    def to_dict(self):
        return {
            "name": self.name,
            "is_completed": self.is_completed,
            "priority": self.priority,
            "due_date": self.due_date,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["name"], data["priority"], data["due_date"], data["category"])
        task.is_completed = data["is_completed"]
        return task

    def __str__(self):
        return f"{'[Done]' if self.is_completed else '[Pending]'} {self.name} (Priority: {self.priority}, Due: {self.due_date}, Category: {self.category})"