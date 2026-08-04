from todo.task import Priority, Task
from todo.todo_list import ToDoList
from todo.storage import Storage

todo = ToDoList()
storage = Storage()
filename = "data/tasks.csv"
loaded_tasks = storage.load_file(filename)

for task in loaded_tasks:
    todo.add_task(task)



def print_table(task_list):
    if not task_list:
            print("No task found")

    print("-------------------------------------------")
    print("# | Title           | Priority | Status")
    print("-------------------------------------------")

    for index, task in enumerate(task_list, start=1):

        status = "✅" if task.completed else "❌"
        print(f"{index:<1} | {task.title:<15} | {task.priority.name:<8} | {status}")


while True:

    print("\n--- ToDo Menu ---")
    print("1. Show tasks")
    print("2. Add task")
    print("3. Remove task")
    print("4. Mark task compeleted")
    print("5. Edit task")
    print("6. Search for a task")
    print("7. Save and Exit")


    choice = input("Choose an option: ")

    if choice == "1":
        print_table(todo.show_tasks())

    elif choice == "2":
        title = input("Title: ")
        des = input("Description: ")
        priority = input("Priority (High/Medium/Low): ").lower()

        try:
            priority = Priority(priority)
        except ValueError:
            priority = Priority.MEDIUM
 
        task = Task(title, des, priority)
        todo.add_task(task)

        print ("New task added successfully")

    elif choice == "3":
        print_table(todo.show_tasks())

        num = int (input("Task number to remove: "))
        removed = todo.remove_task(num)
        print(f"Removed: {removed}")

    elif choice == "4":
        print_table(todo.show_tasks())
        try:
            num = int(input("Task number: "))
            result = todo.mark_task_completed(num)
            print(result)
        except ValueError:
            print ("invalid number")


    elif choice == "5":
        print_table(todo.show_tasks())
        try: 
            num = int(input("Enter task number to edit: "))
            print("Leave it empty if you wont change it !!!")
            new_title = input("New title: ")
            new_des = input("New description: ")
            new_priority_str = input("Priority (LOW \ MEDIUM \ HIGH): ").lower()
            new_priority = None
            if new_priority_str in ["low", "medium", "high"]:
                new_priority = Priority(new_priority_str)

            success = todo.edit_task(num, title=new_title or None, des=new_des or None, priority=new_priority)
            
            if success: 
                print("Task updated")
                storage.save_file(filename, todo.tasks)

            else:
                print("Invalid number")

        except ValueError:
            print("Error!!! invalid number")

    elif choice == "6":
        keyword = input("Enter keyword to search in titles: ")
        print_table(todo.search_tasks(keyword))

    elif choice == "7":
        storage.save_file(filename, todo.tasks)
        print("Saved successfully")
        break

    else:
        print("Invalid option")

    