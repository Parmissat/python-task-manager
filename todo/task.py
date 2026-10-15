from enum import Enum

class Priority (Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task:

    def __init__(self, title, des="" , priority=Priority.MEDIUM, completed = False):
        self.title = title
        self.des = des
        self.priority = priority
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def edit(self, title=None, des=None , priority=None):
        if title: self.title = title
        if des is not None: self.des = des
        if priority: self.priority = priority
        

    def __str__(self):
        
        status = "✅" if self.completed else "❌"
        return f"{status} | Title: {self.title} | Description: {self.des} | Priority: {self.priority.value}"