
class ToDoList:

    def __init__(self):
        self.tasks = []

    def sort_priority(self):
        priority_order = {
            "low" : 1,
            "medium" : 2,
            "high" : 3
        }
        self.tasks.sort(
            key=lambda task: priority_order[task.priority.value],
            reverse=True
        )

    def add_task(self, task):
        self.tasks.append(task)

    def show_tasks(self):
        self.sort_priority()
        return self.tasks
        
    def remove_task(self, task_number):
        index = task_number - 1

        if index < 0 or index >= len(self.tasks):
            return "invalid task number"

        removed = self.tasks.pop(index)
        return removed
    

    def mark_task_completed(self, task_number):
        index = task_number-1
        if index < 0 or index >= len(self.tasks):
            return "invalid task number"
        
        self.tasks[index].mark_completed()
        return self.tasks[index]
    
    def edit_task(self, task_number, title=None, des=None, priority=None, completed=None):
        index = task_number-1
        if index < 0 or index >= len(self.tasks):
            return False
        task = self.tasks[index]
        task.edit(title, des, priority, completed)
        return True
        
    def search_tasks(self, keyword):
        results = []
        for task in self.tasks:
            if keyword.lower() in task.title.lower():
                results.append(task)
        return results

