
#!/usr/bin/env python3
"""
file_sorting_gui_v4.py
Bossu Dashboard Edition 4.0
Features:
 - Treeview student table (Name, Age, Grade)
 - Add / Delete / Sort buttons
 - Search by name (live) and filter by Grade
 - Export to Excel (.xlsx) with fallbacks (openpyxl / pandas / CSV)
 - Dark mode toggle
 - Data persisted in students.txt (name,age,grade)
Author: Alfred Kwesi Dontoh (Bossu)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv
import datetime

FILE_NAME = "students.txt"

# -----------------------
# Helper: persistence
# -----------------------
def load_students():
    students = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    name, age, grade = parts
                    try:
                        age_i = int(age)
                    except ValueError:
                        continue
                    students.append({"name": name, "age": age_i, "grade": grade})
    return students

def save_students(students):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s['name']},{s['age']},{s['grade']}\n")

# -----------------------
# UI helpers
# -----------------------
def refresh_table(filtered=None):
    """Refresh tree from the given list or global students"""
    for row in tree.get_children():
        tree.delete(row)
    source = filtered if filtered is not None else students
    for s in source:
        tree.insert("", "end", values=(s["name"], s["age"], s["grade"]))

def update_status(msg, timeout_ms=None):
    status_var.set(msg)
    if timeout_ms:
        root.after(timeout_ms, lambda: status_var.set("Ready."))

def clear_input_fields():
    name_var.set("")
    age_var.set("")
    grade_var.set("")

# -----------------------
# Core actions
# -----------------------
def add_student():
    name = name_var.get().strip()
    age = age_var.get().strip()
    grade = grade_var.get().strip().upper()
    if not name or not age or not grade:
        messagebox.showwarning("Input Error", "Please fill Name, Age and Grade.")
        return
    if not age.isdigit():
        messagebox.showwarning("Input Error", "Age must be an integer.")
        return
    student = {"name": name, "age": int(age), "grade": grade}
    students.append(student)
    students.sort(key=lambda s: s["age"])
    save_students(students)
    refresh_table()
    clear_input_fields()
    update_status(f"Added: {name} — saved to {FILE_NAME}", 4000)

def delete_selected():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Delete", "No row selected.")
        return
    names = []
    for item in sel:
        vals = tree.item(item, "values")
        names.append(vals[0])
    if not messagebox.askyesno("Confirm delete", f"Delete selected record(s):\n{', '.join(names)}?"):
        return
    # remove from students list by exact match on name+age+grade to be safe
    for item in sel:
        vals = tree.item(item, "values")
        name, age, grade = vals[0], int(vals[1]), vals[2]
        for s in list(students):
            if s["name"] == name and s["age"] == age and s["grade"] == grade:
                students.remove(s)
                break
    save_students(students)
    refresh_table()
    update_status("Deleted selected record(s).", 3000)

def sort_by_age():
    students.sort(key=lambda s: s["age"])
    save_students(students)
    refresh_table()
    update_status("Sorted by age (ascending).", 2500)

def sort_by_grade():
    students.sort(key=lambda s: s["grade"])
    save_students(students)
    refresh_table()
    update_status("Sorted by grade (A–F).", 2500)

def sort_by_grade_then_age():
    # grade ascending, age descending
    students.sort(key=lambda s: (s["grade"], -s["age"]))
    save_students(students)
    refresh_table()
    update_status("Sorted by grade then age (desc).", 2500)

# -----------------------
# Search & Filter
# -----------------------
def apply_search_filter(*_):
    q = search_var.get().strip().lower()
    g = grade_filter_var.get()
    if g == "All":
        grade_cond = lambda s: True
    else:
        grade_cond = lambda s: s["grade"].upper() == g

    def match(s):
        return grade_cond(s) and (q == "" or q in s["name"].lower())

    filtered = [s for s in students if match(s)]
    refresh_table(filtered=filtered)
    update_status(f"Filter: name contains '{q}' | grade: {g}", 1200)

# -----------------------
# Export (Excel with fallbacks)
# -----------------------
def export_to_excel():
    if not students:
        messagebox.showinfo("Export", "No data available to export.")
        return
    default_name = f"students_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel Workbook", "*.xlsx"), ("CSV", "*.csv")],
                                             initialfile=default_name,
                                             title="Export Students As")
    if not file_path:
        return

    # Try pandas if available
    try:
        import pandas as pd
        df = pd.DataFrame(students)
        df = df[["name", "age", "grade"]]
        df.columns = ["Name", "Age", "Grade"]
        df.to_excel(file_path, index=False)
        update_status(f"Exported to {file_path}", 4000)
        messagebox.showinfo("Export", f"Export successful: {file_path}")
        return
    except Exception:
        pass

    # Try openpyxl
    try:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Students"
        ws.append(["Name", "Age", "Grade"])
        for s in students:
            ws.append([s["name"], s["age"], s["grade"]])
        wb.save(file_path)
        update_status(f"Exported to {file_path}", 4000)
        messagebox.showinfo("Export", f"Export successful: {file_path}")
        return
    except Exception:
        pass

    # Fallback to CSV
    try:
        if not file_path.lower().endswith(".csv"):
            file_path = os.path.splitext(file_path)[0] + ".csv"
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Age", "Grade"])
            for s in students:
                writer.writerow([s["name"], s["age"], s["grade"]])
        update_status(f"Exported to {file_path}", 4000)
        messagebox.showinfo("Export", f"Exported as CSV (fallback): {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Could not export: {e}")

# -----------------------
# Dark mode toggle
# -----------------------
LIGHT = {
    "bg": "#f0f4f7",
    "header_bg": "#2b5797",
    "header_fg": "white",
    "button_bg": "#2b5797",
    "button_fg": "white",
    "status_bg": "#2b5797",
    "row_bg": "white",
    "text_fg": "black",
    "entry_bg": "white"
}

DARK = {
    "bg": "#222831",
    "header_bg": "#393E46",
    "header_fg": "white",
    "button_bg": "#00ADB5",
    "button_fg": "#222831",
    "status_bg": "#393E46",
    "row_bg": "#30475e",
    "text_fg": "white",
    "entry_bg": "#393E46"
}

current_theme = LIGHT

def apply_theme(theme):
    root.configure(bg=theme["bg"])
    main_frame.configure(bg=theme["bg"])
    title_label.configure(bg=theme["bg"], fg=theme["fg"])
    status_label.configure(bg=theme["bg"], fg=theme["fg"])

    # Style ttk widgets instead of direct bg config
    style = ttk.Style()
    style.configure("TCombobox", fieldbackground=theme["entry_bg"], foreground=theme["fg"])
    style.configure("TEntry", fieldbackground=theme["entry_bg"], foreground=theme["fg"])

    # Update buttons and Treeview
    for button in [add_button, sort_age_button, sort_grade_button, export_button, toggle_theme_button]:
        button.configure(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["accent"])

    tree.tag_configure("evenrow", background=theme["table_even"])
    tree.tag_configure("oddrow", background=theme["table_odd"])

def refresh_table(filtered_data=None):
    # Use only one function to refresh table safely
    refresh_table_with_striping(filtered_data)

# Keep references for theme application
header = header
header_label = header_label
frame_input = frame_input
input_labels = input_labels
input_entries = input_entries
add_btn = add_btn
action_buttons = action_buttons
search_entry = search_entry
grade_filter_menu = grade_filter_menu
status_bar = status_bar

# Apply initial theme (LIGHT)
current_theme = LIGHT
apply_theme = globals().get("apply_theme")  # already defined above
apply_theme(current_theme)

# Re-apply striping after initial populate
apply_row_striping()

# Bind tree selection -> show selected in inputs (optional convenience)
def on_tree_select(event):
    sel = tree.selection()
    if not sel:
        return
    # take first selected
    vals = tree.item(sel[0], "values")
    if vals:
        name_var.set(vals[0])
        age_var.set(vals[1])
        grade_var.set(vals[2])

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Run app
root.mainloop()

