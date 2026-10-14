import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk

from todo.storage import Storage
from todo.task import Priority, Task
from todo.todo_list import ToDoList

DATA_FILE = Path.home() / "SimpleTasks" / "tasks.csv"


class TaskApp:
    def __init__(self, root):
        self.root = root
        root.title("Simple Tasks")
        root.geometry("480x420")
        root.minsize(380, 300)

        self.todo = ToDoList()
        self.storage = Storage()

        DATA_FILE.parent.mkdir(exist_ok=True)
        if DATA_FILE.exists():
            for task in self.storage.load_file(str(DATA_FILE)):
                self.todo.add_task(task)

        self.build_ui()
        self.refresh()

  
    def build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        self.title_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.title_var)
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda event: self.add())
        entry.focus()

        self.priority_var = tk.StringVar(value=Priority.MEDIUM.value)
        ttk.Combobox(
            top,
            textvariable=self.priority_var,
            values=[p.value for p in Priority],
            width=8,
            state="readonly",
        ).pack(side="left", padx=6)

        ttk.Button(top, text="Add", command=self.add).pack(side="left")

        self.tree = ttk.Treeview(
            self.root,
            columns=("done", "title", "priority"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("done", text="")
        self.tree.heading("title", text="Task")
        self.tree.heading("priority", text="Priority")
        self.tree.column("done", width=40, anchor="center", stretch=False)
        self.tree.column("title", width=280)
        self.tree.column("priority", width=80, anchor="center", stretch=False)
        self.tree.pack(fill="both", expand=True, padx=10)
        self.tree.bind("<Double-1>", lambda event: self.edit())

        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack(fill="x")
        ttk.Button(bottom, text="Done", command=self.complete).pack(side="left")
        ttk.Button(bottom, text="Delete", command=self.delete).pack(side="left", padx=6)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for i, task in enumerate(self.todo.show_tasks()):
            mark = "✅" if task.completed else "⬜"
            self.tree.insert(
                "", "end", iid=str(i), values=(mark, task.title, task.priority.name)
            )

    def selected_num(self):
        """Returns the 1-based task number (same as the CLI), or None."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Simple Tasks", "Select a task first.")
            return None
        return int(selection[0]) + 1

    def save(self):
        self.storage.save_file(str(DATA_FILE), self.todo.tasks)

  
    def add(self):
        title = self.title_var.get().strip()
        if not title:
            return
        priority = Priority(self.priority_var.get())
        self.todo.add_task(Task(title, "", priority))
        self.title_var.set("")
        self.save()
        self.refresh()

    def complete(self):
        num = self.selected_num()
        if num is None:
            return
        self.todo.mark_task_completed(num)
        self.save()
        self.refresh()

    def delete(self):
        num = self.selected_num()
        if num is None:
            return
        self.todo.remove_task(num)
        self.save()
        self.refresh()

    def edit(self):
        num = self.selected_num()
        if num is None:
            return
        new_title = simpledialog.askstring("Edit task", "New title:", parent=self.root)
        if new_title and new_title.strip():
            self.todo.edit_task(num, title=new_title.strip(), des=None, priority=None)
            self.save()
            self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    TaskApp(root)
    root.mainloop()
