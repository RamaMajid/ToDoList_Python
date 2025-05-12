import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from TaskManager import TaskManager
from datetime import datetime
import json

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("900x800")
        self.root.configure(bg="#e0e7ff")

        self.task_manager = TaskManager()

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10, background="#6366f1", foreground="white")
        self.style.map("TButton", background=[("active", "#4f46e5")])
        self.style.configure("Treeview", font=("Segoe UI", 11), rowheight=30)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#c7d2fe", foreground="#1e3a8a")
        self.style.configure("TCombobox", font=("Segoe UI", 12))
        self.style.configure("TEntry", font=("Segoe UI", 12))
        self.style.configure("Progressbar", thickness=20, troughcolor="#d1d5db", background="#22c55e")

        # Header
        self.header_frame = tk.Frame(self.root, bg="#6366f1", pady=20)
        self.header_frame.pack(fill="x")
        self.title_label = tk.Label(
            self.header_frame,
            text="To-Do List",
            font=("Segoe UI", 24, "bold"),
            bg="#6366f1",
            fg="white"
        )
        self.title_label.pack()

        # Search and Filter Frame
        self.filter_frame = tk.Frame(self.root, bg="#e0e7ff")
        self.filter_frame.pack(pady=10, padx=20, fill="x")

        self.search_entry = ttk.Entry(self.filter_frame, width=30)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_tasks)

        self.status_var = tk.StringVar(value="All")
        self.status_menu = ttk.Combobox(
            self.filter_frame,
            textvariable=self.status_var,
            values=["All", "Completed", "Pending"],
            width=12,
            state="readonly"
        )
        self.status_menu.pack(side="left", padx=(0, 10))
        self.status_menu.bind("<<ComboboxSelected>>", self.update_task_list)

        self.category_var = tk.StringVar(value="All")
        self.category_menu = ttk.Combobox(
            self.filter_frame,
            textvariable=self.category_var,
            values=["All", "General", "Work", "Personal", "Urgent"],
            width=12,
            state="readonly"
        )
        self.category_menu.pack(side="left", padx=(0, 10))
        self.category_menu.bind("<<ComboboxSelected>>", self.update_task_list)

        # Input Frame
        self.input_frame = tk.Frame(self.root, bg="#e0e7ff")
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ttk.Entry(self.input_frame, width=30)
        self.task_entry.pack(side="left", padx=(0, 10))

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(
            self.input_frame,
            textvariable=self.priority_var,
            values=["Low", "Medium", "High"],
            width=10,
            state="readonly"
        )
        self.priority_menu.pack(side="left", padx=(0, 10))

        self.due_date_entry = DateEntry(
            self.input_frame,
            width=12,
            background="#6366f1",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )
        self.due_date_entry.pack(side="left", padx=(0, 10))

        self.category_input_var = tk.StringVar(value="General")
        self.category_input_menu = ttk.Combobox(
            self.input_frame,
            textvariable=self.category_input_var,
            values=["General", "Work", "Personal", "Urgent"],
            width=12,
            state="readonly"
        )
        self.category_input_menu.pack(side="left", padx=(0, 10))

        self.add_button = ttk.Button(self.input_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left")
        self.add_button.bind("<Button-1>", self.animate_button)

        # Progress Bar
        self.progress_frame = tk.Frame(self.root, bg="#e0e7ff")
        self.progress_frame.pack(pady=10, padx=20, fill="x")
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Completion Progress",
            font=("Segoe UI", 12),
            bg="#e0e7ff",
            fg="#1e3a8a"
        )
        self.progress_label.pack(anchor="w")
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400, mode="determinate")
        self.progress_bar.pack(fill="x")

        # Table Frame
        self.table_frame = tk.Frame(self.root, bg="#e0e7ff")
        self.table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.task_tree = ttk.Treeview(
            self.table_frame,
            columns=("Status", "Task", "Priority", "Due Date", "Category"),
            show="headings",
            selectmode="browse"
        )
        self.task_tree.heading("Status", text="Status", command=lambda: self.sort_column("status"))
        self.task_tree.heading("Task", text="Task Name", command=lambda: self.sort_column("name"))
        self.task_tree.heading("Priority", text="Priority", command=lambda: self.sort_column("priority"))
        self.task_tree.heading("Due Date", text="Due Date", command=lambda: self.sort_column("due_date"))
        self.task_tree.heading("Category", text="Category", command=lambda: self.sort_column("category"))
        self.task_tree.column("Status", width=80, anchor="center")
        self.task_tree.column("Task", width=250)
        self.task_tree.column("Priority", width=80, anchor="center")
        self.task_tree.column("Due Date", width=100, anchor="center")
        self.task_tree.column("Category", width=100, anchor="center")
        self.task_tree.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.task_tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)

        # Action Frame
        self.action_frame = tk.Frame(self.root, bg="#e0e7ff")
        self.action_frame.pack(pady=10)

        self.toggle_button = ttk.Button(self.action_frame, text="Toggle Status", command=self.toggle_task_status)
        self.toggle_button.pack(side="left", padx=5)
        self.toggle_button.bind("<Button-1>", self.animate_button)

        self.edit_button = ttk.Button(self.action_frame, text="Edit Task", command=self.open_edit_window)
        self.edit_button.pack(side="left", padx=5)
        self.edit_button.bind("<Button-1>", self.animate_button)

        self.remove_button = ttk.Button(self.action_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side="left", padx=5)
        self.remove_button.bind("<Button-1>", self.animate_button)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg="#c7d2fe",
            fg="#1e3a8a",
            relief="sunken",
            anchor="w",
            padx=10
        )
        self.status_bar.pack(side="bottom", fill="x")

        # Bindings
        self.task_tree.bind("<Double-1>", self.toggle_task_status)
        self.task_tree.bind("<ButtonRelease-1>", self.update_status_bar)
        self.add_button.bind("<Enter>", lambda e: self.set_status("Add a new task"))
        self.add_button.bind("<Leave>", lambda e: self.set_status("Ready"))
        self.toggle_button.bind("<Enter>", lambda e: self.set_status("Toggle task completion"))
        self.toggle_button.bind("<Leave>", lambda e: self.set_status("Ready"))
        self.edit_button.bind("<Enter>", lambda e: self.set_status("Edit selected task"))
        self.edit_button.bind("<Leave>", lambda e: self.set_status("Ready"))
        self.remove_button.bind("<Enter>", lambda e: self.set_status("Remove selected task"))
        self.remove_button.bind("<Leave>", lambda e: self.set_status("Ready"))

        # Sorting state
        self.sort_reverse = False
        self.last_sort_column = None

        # Initialize UI
        self.update_task_list()
        self.update_progress_bar()

    def set_status(self, message):
        self.status_var.set(message)

    def update_status_bar(self, event):
        selected_items = self.task_tree.selection()
        if selected_items:
            task_name = self.task_tree.item(selected_items[0])["values"][1]
            self.set_status(f"Selected: {task_name}")
        else:
            self.set_status("Ready")

    def animate_button(self, event):
        button = event.widget
        original_bg = self.style.lookup("TButton", "background")
        button.configure(style="Active.TButton")
        self.root.after(100, lambda: button.configure(style="TButton"))

    def update_progress_bar(self):
        total_tasks = len(self.task_manager.get_tasks())
        completed_tasks = len([t for t in self.task_manager.get_tasks() if t.is_completed])
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        self.progress_bar["value"] = progress
        self.progress_label.config(text=f"Completion Progress: {completed_tasks}/{total_tasks}")

    def search_tasks(self, event):
        self.update_task_list()

    def update_task_list(self, event=None):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        search_query = self.search_entry.get().lower()
        status_filter = self.status_var.get()
        category_filter = self.category_var.get()

        tasks = self.task_manager.filter_tasks(status_filter, category_filter)
        for task in tasks:
            if search_query in task.name.lower() or search_query in task.category.lower():
                status = "Done" if task.is_completed else "Pending"
                self.task_tree.insert("", "end", values=(status, task.name, task.priority, task.due_date, task.category))
                tag = f"priority_{task.priority.lower()}"
                self.task_tree.item(self.task_tree.get_children()[-1], tags=(tag,))
        self.task_tree.tag_configure("priority_high", background="#fee2e2")
        self.task_tree.tag_configure("priority_medium", background="#fef3c7")
        self.task_tree.tag_configure("priority_low", background="#dcfce7")

        self.update_progress_bar()
        self.set_status("Task list updated")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get()
        category = self.category_input_var.get()

        # Check for duplicate task name (case-insensitive)
        if task_name:
            tasks = self.task_manager.get_tasks()
            if any(task.name.lower() == task_name.lower() for task in tasks):
                messagebox.showwarning("Input Error", "Task name already exists. Please choose a different name.")
                return
            self.task_manager.add_task(task_name, priority, due_date, category)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.set_date(datetime.now())
            self.priority_var.set("Medium")
            self.category_input_var.set("General")
            self.set_status("Task added successfully")
        else:
            messagebox.showwarning("Input Error", "Please enter a task name.")

    def remove_task(self):
        selected_items = self.task_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")
            return
        selected_item = selected_items[0]
        task_name = self.task_tree.item(selected_item)["values"][1]
        for task in self.task_manager.get_tasks():
            if task.name == task_name:
                self.task_manager.remove_task(task)
                break
        self.update_task_list()
        self.set_status("Task removed successfully")

    def toggle_task_status(self, event=None):
        selected_items = self.task_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a task to toggle.")
            return
        selected_item = selected_items[0]
        task_name = self.task_tree.item(selected_item)["values"][1]
        for task in self.task_manager.get_tasks():
            if task.name == task_name:
                task.toggle_status()
                break
        self.update_task_list()
        self.set_status("Task status toggled")

    def open_edit_window(self):
        selected_items = self.task_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")
            return
        selected_item = selected_items[0]
        task_name = self.task_tree.item(selected_item)["values"][1]
        task = next((t for t in self.task_manager.get_tasks() if t.name == task_name), None)
        if not task:
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x400")
        edit_window.configure(bg="#e0e7ff")

        tk.Label(edit_window, text="Edit Task", font=("Segoe UI", 16, "bold"), bg="#e0e7ff").pack(pady=10)

        tk.Label(edit_window, text="Task Name:", bg="#e0e7ff", font=("Segoe UI", 12)).pack()
        name_entry = ttk.Entry(edit_window, width=40)
        name_entry.insert(0, task.name)
        name_entry.pack(pady=5)

        tk.Label(edit_window, text="Priority:", bg="#e0e7ff", font=("Segoe UI", 12)).pack()
        priority_var = tk.StringVar(value=task.priority)
        priority_menu = ttk.Combobox(edit_window, textvariable=priority_var, values=["Low", "Medium", "High"], state="readonly")
        priority_menu.pack(pady=5)

        tk.Label(edit_window, text="Due Date:", bg="#e0e7ff", font=("Segoe UI", 12)).pack()
        due_date_entry = DateEntry(
            edit_window,
            width=12,
            background="#6366f1",
            foreground="white",
            borderwidth=2,
            date_pattern="yyyy-mm-dd"
        )
        due_date_entry.set_date(task.due_date)
        due_date_entry.pack(pady=5)

        tk.Label(edit_window, text="Category:", bg="#e0e7ff", font=("Segoe UI", 12)).pack()
        category_var = tk.StringVar(value=task.category)
        category_menu = ttk.Combobox(
            edit_window,
            textvariable=category_var,
            values=["General", "Work", "Personal", "Urgent"],
            state="readonly"
        )
        category_menu.pack(pady=5)

        def save_changes():
            new_name = name_entry.get().strip()
            new_priority = priority_var.get()
            new_due_date = due_date_entry.get()
            new_category = category_var.get()
            if new_name:
                # Check for duplicate task name (case-insensitive), excluding the current task
                tasks = self.task_manager.get_tasks()
                if any(t.name.lower() == new_name.lower() and t != task for t in tasks):
                    messagebox.showwarning("Input Error", "Task name already exists. Please choose a different name.")
                    return
                task.update(new_name, new_priority, new_due_date, new_category)
                self.update_task_list()
                self.set_status("Task updated successfully")
                edit_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter a task name.")

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=20)
        save_button.bind("<Button-1>", self.animate_button)
        edit_window.transient(self.root)
        edit_window.grab_set()

    def sort_column(self, column):
        if self.last_sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        self.task_manager.sort_tasks(column, self.sort_reverse)
        self.update_task_list()
        self.last_sort_column = column
        self.set_status(f"Sorted by {column}")