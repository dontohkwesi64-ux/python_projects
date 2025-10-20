import tkinter as tk
from tkinter import ttk, messagebox
import os

# --- File path for saving student data ---
FILE_NAME = "students_ai.txt"

# --- Utility functions ---
def load_students():
    """Load students from file."""
    students = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    name, age, score, grade = parts
                    students.append({
                        "name": name,
                        "age": int(age),
                        "score": float(score),
                        "grade": grade
                    })
    return students


def save_students(students):
    """Save students back to file."""
    with open(FILE_NAME, "w") as file:
        for s in students:
            file.write(f"{s['name']},{s['age']},{s['score']},{s['grade']}\n")


def refresh_table():
    """Refresh table display."""
    for row in tree.get_children():
        tree.delete(row)
    for s in students:
        tree.insert("", "end", values=(s['name'], s['age'], s['score'], s['grade']))


def update_status(msg):
    status_var.set(msg)

# --- Grade computation ---
def compute_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "F"

# --- Button actions ---
def add_student():
    name = name_var.get().strip()
    age = age_var.get().strip()
    score = score_var.get().strip()

    if not name or not age or not score:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    if not age.isdigit():
        messagebox.showwarning("Input Error", "Age must be a number.")
        return
    try:
        score = float(score)
    except ValueError:
        messagebox.showwarning("Input Error", "Score must be a number.")
        return
    if not (0 <= score <= 100):
        messagebox.showwarning("Input Error", "Score must be between 0 and 100.")
        return

    grade = compute_grade(score)
    new_student = {"name": name, "age": int(age), "score": score, "grade": grade}
    students.append(new_student)
    save_students(students)
    refresh_table()

    if score < 60:
        update_status(f"⚠ {name} needs improvement! Grade: {grade}")
    else:
        update_status(f"✅ {name} added successfully. Grade: {grade}")

    name_var.set("")
    age_var.set("")
    score_var.set("")


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
    update_status("Deleted selected record(s).")


def sort_by_score():
    students.sort(key=lambda s: s['score'], reverse=True)
    refresh_table()
    update_status("Sorted by Score (High → Low).")
    save_students(students)


def sort_by_grade():
    students.sort(key=lambda s: s['grade'])
    refresh_table()
    update_status("Sorted by Grade (A–F).")
    save_students(students)


def sort_by_age():
    students.sort(key=lambda s: s['age'])
    refresh_table()
    update_status("Sorted by Age.")
    save_students(students)


def analyze_class():
    """Simple offline AI-like analysis."""
    if not students:
        messagebox.showinfo("Analysis", "No student data available.")
        return

    total_score = sum(s['score'] for s in students)
    avg_score = total_score / len(students)
    top_score = max(students, key=lambda s: s['score'])
    weak_students = [s['name'] for s in students if s['score'] < 60]

    report = (
        f"📊 CLASS PERFORMANCE ANALYSIS\n\n"
        f"Total Students: {len(students)}\n"
        f"Class Average: {avg_score:.2f}%\n"
        f"Top Performer: {top_score['name']} ({top_score['score']}%)\n"
    )
    if weak_students:
        report += f"⚠ Students Needing Help: {', '.join(weak_students)}"
    else:
        report += "✅ All students are performing well!"

    # Create a popup window for the report
    analysis_win = tk.Toplevel(root)
    analysis_win.title("AI Performance Report")
    analysis_win.geometry("400x300")
    analysis_win.configure(bg="#f8f9fa")

    tk.Label(analysis_win, text="Bossu AI Class Report", font=("Segoe UI", 14, "bold"), bg="#2b5797", fg="white", pady=8).pack(fill="x")
    tk.Message(analysis_win, text=report, width=380, bg="#f8f9fa", font=("Segoe UI", 11)).pack(pady=10)

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Bossu AI Dashboard Edition – 5.0")
root.geometry("780x520")
root.configure(bg="#f0f4f7")

# Header
tk.Label(root, text="Bossu AI Student Dashboard", font=("Segoe UI", 16, "bold"), bg="#2b5797", fg="white", pady=10).pack(fill="x")

# Input Frame
frame_input = tk.Frame(root, bg="#f0f4f7", pady=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="Name:", bg="#f0f4f7").grid(row=0, column=0, padx=5)
tk.Label(frame_input, text="Age:", bg="#f0f4f7").grid(row=0, column=2, padx=5)
tk.Label(frame_input, text="Score (%):", bg="#f0f4f7").grid(row=0, column=4, padx=5)

name_var = tk.StringVar()
age_var = tk.StringVar()
score_var = tk.StringVar()

tk.Entry(frame_input, textvariable=name_var, width=15).grid(row=0, column=1, padx=5)
tk.Entry(frame_input, textvariable=age_var, width=8).grid(row=0, column=3, padx=5)
tk.Entry(frame_input, textvariable=score_var, width=8).grid(row=0, column=5, padx=5)

tk.Button(frame_input, text="Add Student", bg="#2b5797", fg="white", command=add_student).grid(row=0, column=6, padx=10)

# Table Frame
frame_table = tk.Frame(root)
frame_table.pack(pady=10, fill="both", expand=True)

columns = ("Name", "Age", "Score", "Grade")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180, anchor="center")
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Button Frame
frame_buttons = tk.Frame(root, bg="#f0f4f7", pady=10)
frame_buttons.pack()

tk.Button(frame_buttons, text="Delete Selected", command=delete_student, bg="#d9534f", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Sort by Score", command=sort_by_score, width=15).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Sort by Grade", command=sort_by_grade, width=15).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Sort by Age", command=sort_by_age, width=15).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="AI Analysis", command=analyze_class, bg="#28a745", fg="white", width=15).grid(row=0, column=4, padx=5)

# Status Bar
status_var = tk.StringVar(value="Ready.")
status_bar = tk.Label(root, textvariable=status_var, bg="#2b5797", fg="white", anchor="w", padx=10)
status_bar.pack(fill="x", side="bottom")

# Load existing data
students = load_students()
refresh_table()

root.mainloop()
