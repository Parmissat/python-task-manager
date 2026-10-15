from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from todo.storage import Storage
from todo.task import Priority, Task
from todo.todo_list import ToDoList

# Always the same place, no matter where the app is launched from.
DATA_FILE = Path.home() / "SimpleTasks" / "tasks.csv"

# ---------- look (change colors here) ----------
BG = "#F5F2FB"            # window background (very light lavender)
CARD = "#FFFFFF"          # cards
CARD_BORDER = "#E7E1F4"   # thin soft border around cards
ACCENT = "#8E7CC3"        # soft purple: buttons, checkboxes
ACCENT_HOVER = "#7B69B0"
TEXT = "#2E2A3B"
MUTED = "#8C87A0"
BADGES = {                # (background, text) for each priority
    Priority.HIGH: ("#FADCE4", "#B03A5B"),
    Priority.MEDIUM: ("#FCEBC8", "#8A5A00"),
    Priority.LOW: ("#DDEFE3", "#2F6B45"),
}
PRIORITY_VALUES = ["high", "medium", "low"]

ctk.set_appearance_mode("light")


class TaskApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simple Tasks")
        self.geometry("520x680")
        self.minsize(420, 480)
        self.configure(fg_color=BG)

        self.todo = ToDoList()
        self.storage = Storage()
        self.expanded = set()  # tasks whose description is open

        DATA_FILE.parent.mkdir(exist_ok=True)
        for task in self.storage.load_file(str(DATA_FILE)):
            self.todo.add_task(task)

        self.build_ui()
        self.refresh()

    # ---------- UI ----------
    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 6))
        ctk.CTkLabel(
            header, text="My Tasks", text_color=TEXT,
            font=ctk.CTkFont(size=26, weight="bold"),
        ).pack(side="left")
        self.counter = ctk.CTkLabel(header, text="", text_color=MUTED)
        self.counter.pack(side="right")

        # add-task card
        form = ctk.CTkFrame(
            self, fg_color=CARD, corner_radius=16,
            border_width=1, border_color=CARD_BORDER,
        )
        form.pack(fill="x", padx=20, pady=10)

        row = ctk.CTkFrame(form, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(12, 6))

        self.title_entry = ctk.CTkEntry(
            row, placeholder_text="What needs doing?", height=38,
            corner_radius=12, fg_color=BG, border_color=CARD_BORDER,
            text_color=TEXT,
        )
        self.title_entry.pack(side="left", fill="x", expand=True)
        self.title_entry.bind("<Return>", lambda event: self.add())

        self.priority_menu = ctk.CTkOptionMenu(
            row, values=PRIORITY_VALUES, width=100, height=38,
            corner_radius=12, fg_color=BG, text_color=TEXT,
            button_color=ACCENT, button_hover_color=ACCENT_HOVER,
        )
        self.priority_menu.set("medium")
        self.priority_menu.pack(side="left", padx=6)

        ctk.CTkButton(
            row, text="Add", width=70, height=38, corner_radius=12,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, command=self.add,
        ).pack(side="left")

        self.desc_entry = ctk.CTkEntry(
            form, placeholder_text="Description (optional)", height=34,
            corner_radius=12, fg_color=BG, border_color=CARD_BORDER,
            text_color=TEXT,
        )
        self.desc_entry.pack(fill="x", padx=12, pady=(0, 12))
        self.desc_entry.bind("<Return>", lambda event: self.add())

        # list of task cards
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def refresh(self):
        for child in self.list_frame.winfo_children():
            child.destroy()

        tasks = self.todo.show_tasks()  # sorted; card number = list position + 1
        done = sum(1 for task in tasks if task.completed)
        self.counter.configure(text=f"{done}/{len(tasks)} done")

        if not tasks:
            ctk.CTkLabel(
                self.list_frame, text="Nothing here yet ✨", text_color=MUTED,
            ).pack(pady=40)
        for index, task in enumerate(tasks):
            self.make_card(index + 1, task)

    def make_card(self, num, task):
        card = ctk.CTkFrame(
            self.list_frame, fg_color=CARD, corner_radius=16,
            border_width=1, border_color=CARD_BORDER,
        )
        card.pack(fill="x", padx=8, pady=5)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=10)

        box = ctk.CTkCheckBox(
            row, text="", width=28, checkbox_width=24, checkbox_height=24,
            corner_radius=8, border_width=2, fg_color=ACCENT,
            hover_color=ACCENT_HOVER, border_color=ACCENT,
            command=lambda: self.toggle_done(num, box),
        )
        if task.completed:
            box.select()
        box.pack(side="left")

        title = ctk.CTkLabel(
            row, text=task.title, anchor="w", justify="left", wraplength=230,
            font=ctk.CTkFont(size=15, overstrike=task.completed),
            text_color=MUTED if task.completed else TEXT,
        )
        title.pack(side="left", fill="x", expand=True, padx=(6, 8))

        # right side (packed right-to-left): delete, edit, priority badge
        ctk.CTkButton(
            row, text="✕", width=28, height=28, corner_radius=14,
            fg_color="transparent", hover_color=BG, text_color=MUTED,
            command=lambda: self.delete(num, task),
        ).pack(side="right")
        ctk.CTkButton(
            row, text="✎", width=28, height=28, corner_radius=14,
            fg_color="transparent", hover_color=BG, text_color=MUTED,
            command=lambda: self.open_editor(num, task),
        ).pack(side="right")
        badge_bg, badge_text = BADGES[task.priority]
        ctk.CTkLabel(
            row, text=task.priority.name.title(), width=64, height=24,
            corner_radius=10, fg_color=badge_bg, text_color=badge_text,
            font=ctk.CTkFont(size=12),
        ).pack(side="right", padx=6)

        if id(task) in self.expanded:
            ctk.CTkLabel(
                card, text=task.des or "No description", text_color=MUTED,
                anchor="w", justify="left", wraplength=380,
            ).pack(fill="x", padx=48, pady=(0, 12))

        # clicking the card (not the buttons) opens/closes the description
        for widget in (card, row, title):
            widget.bind("<Button-1>", lambda event, t=task: self.toggle_details(t))

    def save(self):
        self.storage.save_file(str(DATA_FILE), self.todo.tasks)

    # ---------- actions ----------
    def add(self):
        title = self.title_entry.get().strip()
        if not title:
            return
        description = self.desc_entry.get().strip()
        priority = Priority(self.priority_menu.get())
        self.todo.add_task(Task(title, description, priority))
        self.title_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.save()
        self.refresh()
        self.title_entry.focus()

    def toggle_done(self, num, box):
        if box.get():
            self.todo.mark_task_completed(num)
        else:
            self.todo.mark_task_incomplete(num)
        self.save()
        self.refresh()

    def toggle_details(self, task):
        if id(task) in self.expanded:
            self.expanded.discard(id(task))
        else:
            self.expanded.add(id(task))
        self.refresh()

    def delete(self, num, task):
        if not messagebox.askyesno("Delete task", f'Delete "{task.title}"?'):
            return
        self.todo.remove_task(num)
        self.expanded.discard(id(task))
        self.save()
        self.refresh()

    def open_editor(self, num, task):
        win = ctk.CTkToplevel(self)
        win.title("Edit task")
        win.geometry("420x380")
        win.configure(fg_color=BG)
        win.transient(self)
        win.after(150, win.focus)
        win.bind("<Escape>", lambda event: win.destroy())

        title_entry = ctk.CTkEntry(
            win, height=38, corner_radius=12, fg_color=CARD,
            border_color=CARD_BORDER, text_color=TEXT,
        )
        title_entry.insert(0, task.title)
        title_entry.pack(fill="x", padx=20, pady=(20, 10))

        desc_box = ctk.CTkTextbox(
            win, height=130, corner_radius=12, border_width=1,
            border_color=CARD_BORDER, fg_color=CARD, text_color=TEXT,
        )
        desc_box.insert("1.0", task.des)
        desc_box.pack(fill="x", padx=20, pady=10)

        priority_menu = ctk.CTkOptionMenu(
            win, values=PRIORITY_VALUES, height=38, corner_radius=12,
            fg_color=CARD, text_color=TEXT,
            button_color=ACCENT, button_hover_color=ACCENT_HOVER,
        )
        priority_menu.set(task.priority.value)
        priority_menu.pack(fill="x", padx=20, pady=10)

        def submit():
            new_title = title_entry.get().strip()
            if not new_title:
                return
            self.todo.edit_task(
                num,
                title=new_title,
                des=desc_box.get("1.0", "end").strip(),
                priority=Priority(priority_menu.get()),
            )
            self.save()
            self.refresh()
            win.destroy()

        ctk.CTkButton(
            win, text="Save", height=40, corner_radius=12,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, command=submit,
        ).pack(fill="x", padx=20, pady=(10, 20))


if __name__ == "__main__":
    TaskApp().mainloop()
