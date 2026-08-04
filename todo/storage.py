import csv 
from todo.task import Task, Priority
class Storage : 
    
    def save_file(self, filename , tasks):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for task in tasks:
                writer.writerow([
                    task.title,
                    task.des,
                    task.priority.value,
                    task.completed
                ])


    def load_file(self, filename):
        tasks = []
        try:
            with open(filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)

                for row in reader:
                    title, des, priority, completed = row


                    task = Task(
                        title,
                        des,
                        Priority(priority),
                        completed == "True"
                    )
                    tasks.append(task)


        except FileNotFoundError:
            pass

        return tasks