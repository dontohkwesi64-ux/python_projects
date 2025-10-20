import tkinter as tk
from tkinter import ttk, messagebox
import os

FILE_NAME = "students.txt"

# --- Utility functions ---
def load_students():
    students = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    name, age, grade = parts
                    try:
                        students.append({"name": name, "age": int(age), "grade": grade.upper()})
                    except ValueError:
                        # skip malformed lines
                        continue
    return students

def save_students(students):
    with open(FILE_NAME, "w") as file:
        for s in students:
            file.write(f"{s['name']},{s['age']},{s['grade']}\n")

# grade letter -> numeric mapping (for counseling analysis)
GRADE_TO_SCORE = {
    "A": 90,
    "B": 80,
    "C": 70,
    "D": 60,
    "F": 50
}

def grade_letter_from_score(score):
    """Convert numeric average score back to a letter grade approximation."""
    if score >= 85:
        return "A"
    if score >= 75:
        return "B"
    if score >= 65:
        return "C"
    if score >= 55:
        return "D"
    return "F"

def refresh_table(data=None):
    """Refresh table view with student data. Optionally pass a list 'data' to show."""
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)

    # Determine rows source
    rows = data if data is not None else students

    # Insert rows; tag students who need help
    for s in rows:
        tags = ()
        # Highlight criteria: D or F, or unknown grade
        grade = s.get("grade", "").upper()
        if grade in ("D", "F") or (grade not in GRADE_TO_SCORE and isinstance(s.get("age"), int) and s.get("age") > 120):
            tags = ("need_help",)
        tree.insert("", "end", values=(s['name'], s['age'], s['grade']), tags=tags)

    # Apply tag styling (ensure configured)
    tree.tag_configure("need_help", background="#ffe6e6")  # light red/pink highlight

def update_status(msg):
    status_var.set(msg)

# --- CRUD actions ---
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
    if grade not in ("A","B","C","D","F"):
        if not messagebox.askyesno("Grade Confirmation", f"'{grade}' is not a standard grade (A-F). Save anyway?"):
            return

    new_student = {"name": name, "age": int(age), "grade": grade}
    students.append(new_student)
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
    refresh_table(results)
    update_status(f"Found {len(results)} result(s) for '{query}'.")

# --- AI Counseling Logic (offline) ---
def run_ai_analysis():
    """
    Offline counselor:
    - Convert grades to numeric scores
    - Compute class average and approximate class letter grade
    - Identify students with D/F (or below threshold)
    - Produce personalized advice lines and overall recommendations
    """
    ai_output.config(state="normal")
    ai_output.delete("1.0", "end")

    if not students:
        ai_output.insert("end", "AI Counselor: No student records available.\n")
        ai_output.config(state="disabled")
        return

    # Convert student grades to numeric scores; handle unknowns conservatively
    scored_students = []
    for s in students:
        grade = (s.get("grade") or "").upper()
        score = GRADE_TO_SCORE.get(grade)
        if score is None:
            # If unknown letter, try to estimate or skip; we'll set None
            scored_students.append((s, None))
        else:
            scored_students.append((s, score))

    # Compute averages for those with numeric scores
    numeric_scores = [score for (_, score) in scored_students if score is not None]
    avg_score = sum(numeric_scores) / len(numeric_scores) if numeric_scores else None
    avg_letter = grade_letter_from_score(avg_score) if avg_score is not None else "N/A"

    # Build report
    report_lines = []
    report_lines.append("📊 Bossu AI Counselor Report")
    report_lines.append("----------------------------------------")
    if avg_score is not None:
        report_lines.append(f"Class Average Score: {avg_score:.1f}%    (Approx. Grade: {avg_letter})")
    else:
        report_lines.append("Class Average Score: N/A (not enough graded data)")

    # Count per grade
    grade_counts = {}
    for s in students:
        g = (s.get("grade") or "").upper()
        grade_counts[g] = grade_counts.get(g, 0) + 1
    report_lines.append("\nGrade distribution:")
    for g in sorted(grade_counts.keys()):
        report_lines.append(f" - {g or 'Unknown'} : {grade_counts[g]}")

    # Identify students needing help (D/F) or low numeric score threshold
    threshold = 65  # numeric threshold considered 'needs help'
    need_help = []
    borderline = []
    doing_well = []

    for s, score in scored_students:
        g = (s.get("grade") or "").upper()
        if score is not None:
            if score < threshold:
                need_help.append((s, score))
            elif score < (threshold + 10):
                borderline.append((s, score))
            else:
                doing_well.append((s, score))
        else:
            # unknown grade -> consider as borderline for review
            borderline.append((s, score))

    # Personalized advice
    report_lines.append("\nStudents who need improvement:")
    if need_help:
        for s, score in need_help:
            report_lines.append(f" - {s['name']} ({s['grade']} / {score}%) : Suggest: One-on-one tutoring, weekly revision plan, extra practice quizzes.")
    else:
        report_lines.append(" - None")

    report_lines.append("\nStudents borderline (review suggested):")
    if borderline:
        for s, score in borderline:
            grade_text = s['grade']
            score_text = f"{score}%" if score is not None else "N/A"
            report_lines.append(f" - {s['name']} ({grade_text} / {score_text}) : Suggest: monitor progress, small group study.")
    else:
        report_lines.append(" - None")

    # Top performers quick list
    report_lines.append("\nTop performers:")
    top = sorted([(s, sc) for s, sc in scored_students if sc is not None], key=lambda x: -x[1])[:5]
    if top:
        report_lines.append(", ".join([f"{s['name']}({sc}%)" for s, sc in top]))
    else:
        report_lines.append(" - No graded data")

    # Final advice
    report_lines.append("\nOverall Recommendations:")
    if avg_score is not None:
        if avg_score >= 85:
            report_lines.append("The class is performing excellently. Keep up the good work and encourage peer mentoring.")
        elif avg_score >= 75:
            report_lines.append("Good overall performance. Consider targeted revisions for borderline students.")
        elif avg_score >= 65:
            report_lines.append("Average performance. Introduce regular assessments and focused interventions.")
        else:
            report_lines.append("Performance is below expectations. Implement immediate remediation: extra lessons, tutoring, and regular feedback.")
    else:
        report_lines.append("No sufficient numeric grade data. Encourage teachers to record letter grades (A-F) consistently.")

    # Display report
    ai_output.insert("end", "\n".join(report_lines) + "\n")
    ai_output.config(state="disabled")
    ai_output.see("end")

    # Highlight low performing rows in table
    # We'll refresh table and tag need_help rows by D/F or score<threshold
    for row in tree.get_children():
        tree.delete(row)

    for s in students:
        tagset = ()
        g = (s.get("grade") or "").upper()
        score = GRADE_TO_SCORE.get(g)
        if score is not None and score < threshold:
            tagset = ("need_help",)
        tree.insert("", "end", values=(s['name'], s['age'], s['grade']), tags=tagset)
    tree.tag_configure("need_help", background="#ffe6e6")  # highlight

# --- GUI ---
root = tk.Tk()
root.title("Bossu Dashboard – AI Counselor Edition")
root.geometry("820x720")
root.configure(bg="#f0f4f7")

# Header
tk.Label(root, text="Bossu Student Dashboard – AI Counselor", font=("Segoe UI", 16, "bold"),
         bg="#2b5797", fg="white", pady=10).pack(fill="x")

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

# Table
frame_table = tk.Frame(root)
frame_table.pack(pady=10, fill="both", expand=True)
columns = ("Name", "Age", "Grade")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=240, anchor="center")
tree.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Buttons
frame_buttons = tk.Frame(root, bg="#f0f4f7", pady=10)
frame_buttons.pack()
tk.Button(frame_buttons, text="Delete Selected", command=delete_student, bg="#d9534f", fg="white", width=16).grid(row=0, column=0, padx=6)
tk.Button(frame_buttons, text="Sort by Age", command=sort_by_age, width=14).grid(row=0, column=1, padx=6)
tk.Button(frame_buttons, text="Sort by Grade", command=sort_by_grade, width=14).grid(row=0, column=2, padx=6)
tk.Button(frame_buttons, text="Sort by Grade + Age", command=sort_by_grade_then_age, width=18).grid(row=0, column=3, padx=6)

# AI Counselor panel
frame_ai = tk.LabelFrame(root, text="Bossu AI Counselor", bg="#f0f4f7", padx=10, pady=10)
frame_ai.pack(fill="both", expand=True, padx=10, pady=5)

ai_output = tk.Text(frame_ai, height=14, wrap="word", state="disabled", bg="#eef2f5")
ai_output.pack(fill="both", expand=True, pady=5)

# Controls for AI
frame_ai_controls = tk.Frame(frame_ai, bg="#f0f4f7")
frame_ai_controls.pack(fill="x", pady=5)
tk.Button(frame_ai_controls, text="Run AI Analysis", command=run_ai_analysis, bg="#2b5797", fg="white").pack(side="left", padx=6)
tk.Button(frame_ai_controls, text="Clear Report", command=lambda: (ai_output.config(state="normal"), ai_output.delete("1.0","end"), ai_output.config(state="disabled")), width=12).pack(side="left", padx=6)

# Status bar
status_var = tk.StringVar(value="Ready.")
status_bar = tk.Label(root, textvariable=status_var, bg="#2b5797", fg="white", anchor="w", padx=10)
status_bar.pack(fill="x", side="bottom")

# Load data and refresh table
students = load_students()
refresh_table()
root.mainloop()
