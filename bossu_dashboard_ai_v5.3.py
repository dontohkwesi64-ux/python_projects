import tkinter as tk
from tkinter import ttk, messagebox
import os
import matplotlib.pyplot as plt

# File path for students data
FILE_NAME = "students.txt"

# --- Utility functions ---
def load_students():
    """Load students from file and return as list of dicts."""
    students = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    name, age, grade = parts
                    students.append({"name": name, "age": int(age), "grade": grade.upper()})
    return students

def save_students(students):
    """Save students back to file."""
    with open(FILE_NAME, "w") as file:
        for s in students:
            file.write(f"{s['name']},{s['age']},{s['grade']}\n")

def refresh_table():
    """Refresh table view with student data."""
    for row in tree.get_children():
        tree.delete(row)
    for s in students:
        tree.insert("", "end", values=(s['name'], s['age'], s['grade']))

def update_status(msg):
    status_var.set(msg)

# --- Button actions ---
def add_student():
    name = name_var.get().strip()
    age = age_var.get().strip()
    grade = grade_var.get().strip().upper()

    if not name or not age or not grade:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    if not age.isdigit():
        messagebox.showwarning("Input Error", "Age must be a number.")
        return
    if grade not in ["A", "B", "C", "D", "E", "F"]:
        messagebox.showwarning("Input Error", "Grade must be A, B, C, D, E, or F.")
        return

    students.append({"name": name, "age": int(age), "grade": grade})
    students.sort(key=lambda s: s['age'])
    save_students(students)
    refresh_table()
    update_status(f"Student {name} added and sorted by age.")
    name_var.set("")
    age_var.set("")
    grade_var.set("")

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")
        return
    for item in selected:
        values = tree.item(item, "values")
        name = values[0]
        students[:] = [s for s in students if s['name'] != name]
        tree.delete(item)
    save_students(students)
    update_status(f"Deleted selected record(s).")

def sort_by_age():
    students.sort(key=lambda s: s['age'])
    refresh_table()
    update_status("Sorted by Age (Ascending).")
    save_students(students)

def sort_by_grade():
    students.sort(key=lambda s: s['grade'])
    refresh_table()
    update_status("Sorted by Grade (A–F).")
    save_students(students)

def sort_by_grade_then_age():
    students.sort(key=lambda s: (s['grade'], -s['age']))
    refresh_table()
    update_status("Sorted by Grade then Age (Descending).")
    save_students(students)

def search_student():
    query = search_var.get().strip().lower()
    if not query:
        refresh_table()  # show all if empty
        update_status("Showing all students.")
        return

    results = [s for s in students if query in s['name'].lower()]
    for row in tree.get_children():
        tree.delete(row)
    for s in results:
        tree.insert("", "end", values=(s['name'], s['age'], s['grade']))
    update_status(f"Found {len(results)} result(s) for '{query}'.")

def show_analysis():
    """AI Analysis - counts students performing well vs needing assistance."""
    grade_counts = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0}
    for s in students:
        grade_counts[s['grade']] += 1

    # Students who need assistance (grades D, E, F)
    need_assist = grade_counts['D'] + grade_counts['E'] + grade_counts['F']
    doing_well = len(students) - need_assist

    # Show pie chart
    labels = ["Doing Well", "Need Assistance"]
    sizes = [doing_well, need_assist]
    colors = ['green', 'red']
    plt.figure(figsize=(5,5))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Student Performance Analysis")
    plt.show()

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Bossu Dashboard Edition – AI 5.3")
root.geometry("800x550")
root.configure(bg="#f0f4f7")

# Header
tk.Label(root, text="Bossu Student Dashboard – AI 5.3", font=("Segoe UI", 16, "bold"), bg="#2b5797", fg="white", pady=10).pack(fill="x")

# Input Frame
frame_input = tk.Frame(root, bg="#f0f4f7", pady=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="Name:", bg="#f0f4f7").grid(row=0, column=0, padx=5)
tk.Label(frame_input, text="Age:", bg="#f0f4f7").grid(row=0, column=2, padx=5)
tk.Label(frame_input, text="Grade:", bg="#f0f4f7").grid(row=0, column=4, padx=5)

name_var = tk.StringVar()
age_var = tk.StringVar()
grade_var = tk.StringVar()

tk.Entry(frame_input, textvariable=name_var, width=15).grid(row=0, column=1, padx=5)
tk.Entry(frame_input, textvariable=age_var, width=8).grid(row=0, column=3, padx=5)
tk.Entry(frame_input, textvariable=grade_var, width=5).grid(row=0, column=5, padx=5)
tk.Button(frame_input, text="Add Student", bg="#2b5797", fg="white", command=add_student).grid(row=0, column=6, padx=10)

# Search Frame
frame_search = tk.Frame(root, bg="#f0f4f7", pady=5)
frame_search.pack(fill="x")
search_var = tk.StringVar()
tk.Label(frame_search, text="Search Name:", bg="#f0f4f7").grid(row=0, column=0, padx=5)
tk.Entry(frame_search, textvariable=search_var, width=20).grid(row=0, column=1, padx=5)
tk.Button(frame_search, text="Search", command=search_student, bg="#2b5797", fg="white").grid(row=0, column=2, padx=10)

# Table Frame
frame_table = tk.Frame(root)
frame_table.pack(pady=10, fill="both", expand=True)
columns = ("Name", "Age", "Grade")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")
tree.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Button Frame
frame_buttons = tk.Frame(root, bg="#f0f4f7", pady=10)
frame_buttons.pack()
tk.Button(frame_buttons, text="Delete Selected", command=delete_student, bg="#d9534f", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Sort by Age", command=sort_by_age, width=15).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Sort by Grade", command=sort_by_grade, width=15).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Sort by Grade + Age", command=sort_by_grade_then_age, width=18).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="AI Analysis", command=show_analysis, bg="#5cb85c", fg="white", width=15).grid(row=0, column=4, padx=5)

# Status Bar
status_var = tk.StringVar(value="Ready.")
status_bar = tk.Label(root, textvariable=status_var, bg="#2b5797", fg="white", anchor="w", padx=10)
status_bar.pack(fill="x", side="bottom")

# Load data and refresh table
students = load_students()
refresh_table()

root.mainloop()
