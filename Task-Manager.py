import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
import pickle
import os

class Task:
    def __init__(self, description, due_time=None):
        self.description = description
        self.completed = False
        self.creation_date = datetime.datetime.now()
        self.due_time = due_time

class TodoApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Task Manager")
        self.geometry("600x400")
        self.tasks = self.load_tasks()

        self.create_widgets()
        self.update_task_list()

        # Save tasks when closing the window
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=BOTH, expand=YES)

        # Title
        ttk.Label(main_frame, text="My Tasks", font=("TkDefaultFont", 16, "bold")).pack(pady=10)

        # Task list
        self.task_list = ttk.Treeview(main_frame, columns=("Status", "Description", "Due Time"), show="headings")
        self.task_list.heading("Status", text="Status")
        self.task_list.heading("Description", text="Description")
        self.task_list.heading("Due Time", text="Due Time")
        self.task_list.column("Status", width=50)
        self.task_list.column("Description", width=300)
        self.task_list.column("Due Time", width=100)
        self.task_list.pack(fill=BOTH, expand=YES, pady=10)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=10)

        ttk.Button(button_frame, text="Add Task", command=self.add_task, style="success.TButton").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Mark as Completed", command=self.mark_completed, style="info.TButton").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task, style="danger.TButton").pack(side=LEFT, padx=5)

    def add_task(self):
        description = simpledialog.askstring("New Task", "Task description:")
        if description:
            due_time_str = simpledialog.askstring("New Task", "Due time (HH:MM, optional):")
            due_time = None
            if due_time_str:
                try:
                    due_time = datetime.datetime.strptime(due_time_str, "%H:%M").time()
                except ValueError:
                    messagebox.showerror("Error", "Invalid time format. Task will be added without a due time.")
            
            task = Task(description, due_time)
            self.tasks.append(task)
            self.update_task_list()

    def mark_completed(self):
        selected_item = self.task_list.selection()
        if selected_item:
            index = self.task_list.index(selected_item)
            self.tasks[index].completed = True
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task.")

    def delete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            index = self.task_list.index(selected_item)
            del self.tasks[index]
            self.update_task_list()
        else:
            messagebox.showwarning("Warning", "Please select a task.")

    def update_task_list(self):
        self.task_list.delete(*self.task_list.get_children())
        for task in self.tasks:
            status = "✓" if task.completed else "○"
            due_time = task.due_time.strftime("%H:%M") if task.due_time else "-"
            self.task_list.insert("", END, values=(status, task.description, due_time))

    def save_tasks(self):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.pkl"):
            with open("tasks.pkl", "rb") as f:
                return pickle.load(f)
        return []

    def on_closing(self):
        self.save_tasks()
        self.destroy()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
