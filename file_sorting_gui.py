
# file_sorting_gui_v2.py
# Author: Alfred Kwesi Dontoh
# Description: Advanced GUI version with output display and status bar

import tkinter as tk
from tkinter import scrolledtext
import random

# ---------------- Helper Functions ----------------

def update_output(text):
    """Display text in the output area."""
    output_box.config(state="normal")
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, text)
    output_box.config(state="disabled")

def update_status(message):
    """Update the status bar message."""
    status_label.config(text=f"Status: {message}")

# ---------------- Exercises ----------------

def exercise1_fruits():
    fruits = ["Banana", "Mango", "Apple", "Orange", "Pineapple"]
    with open("my_fruits.txt", "w") as f:
        for fruit in fruits:
            f.write(fruit + "\n")

    with open("my_fruits.txt", "r") as f:
        fruits_list = [line.strip() for line in f.readlines()]

    sorted_fruits = sorted(fruits_list)
    result = "--- Fruits in Alphabetical Order ---\n" + "\n".join(sorted_fruits)
    update_output(result)
    update_status("Fruits sorted alphabetically and displayed.")


def exercise2_numbers():
    numbers = [random.randint(1, 100) for _ in range(10)]
    with open("numbers.txt", "w") as f:
        for num in numbers:
            f.write(str(num) + "\n")

    with open("numbers.txt", "r") as f:
        num_list = [int(line.strip()) for line in f.readlines()]

    sorted_nums = sorted(num_list)
    result = "--- Numbers in Ascending Order ---\n" + "\n".join(map(str, sorted_nums))
    update_output(result)
    update_status("Random numbers sorted in ascending order.")


def exercise3_students_grade():
    students = [
        "Janet,25,A",
        "Collins,27,C",
        "Sean,30,B",
        "Ama,23,B",
        "Kojo,29,A"
    ]
    with open("students.txt", "w") as f:
        for student in students:
            f.write(student + "\n")

    with open("students.txt", "r") as f:
        records = [line.strip().split(",") for line in f.readlines()]

    sorted_records = sorted(records, key=lambda x: x[2])
    lines = [f"{name} | Age: {age} | Grade: {grade}" for name, age, grade in sorted_records]
    result = "--- Students Sorted by Grade ---\n" + "\n".join(lines)
    update_output(result)
    update_status("Students sorted by grade (A–F).")


def exercise4_students_grade_age():
    try:
        with open("students.txt", "r") as f:
            records = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        update_output("Error: 'students.txt' not found! Run Exercise 3 first.")
        update_status("Missing students.txt file.")
        return

    sorted_records = sorted(records, key=lambda x: (x[2], -int(x[1])))
    lines = [f"{name} | Age: {age} | Grade: {grade}" for name, age, grade in sorted_records]
    result = "--- Students Sorted by Grade then Age (Descending) ---\n" + "\n".join(lines)
    update_output(result)
    update_status("Students sorted by grade, then by age (descending).")


def exercise5_add_student():
    try:
        with open("students.txt", "r") as f:
            records = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        update_output("Error: 'students.txt' not found! Run Exercise 3 first.")
        update_status("Missing students.txt file.")
        return

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    grade = grade_entry.get().strip().upper()

    if not (name and age.isdigit() and grade):
        update_output("Error: Please fill all fields correctly before adding a student.")
        update_status("Invalid input.")
        return

    records.append([name, age, grade])
    sorted_by_age = sorted(records, key=lambda x: int(x[1]))

    with open("students.txt", "w") as f:
        for record in sorted_by_age:
            f.write(",".join(record) + "\n")

    lines = [f"{name} | Age: {age} | Grade: {grade}" for name, age, grade in sorted_by_age]
    result = "--- Updated Students Sorted by Age ---\n" + "\n".join(lines)
    update_output(result)
    update_status(f"Student '{name}' added and file updated successfully.")

# ---------------- GUI Setup ----------------

root = tk.Tk()
root.title("File Sorting Practice - Bossu Edition 2.0")
root.geometry("650x550")
root.resizable(False, False)
root.configure(bg="#f8f8f8")

# Title
title_label = tk.Label(root, text="File Sorting Practice - Bossu Edition 2.0",
                       font=("Segoe UI", 16, "bold"), bg="#f8f8f8", fg="#222")
title_label.pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f8f8f8")
btn_frame.pack(pady=10)

btn_style = {"font": ("Segoe UI", 11), "width": 35, "bg": "#0078D7", "fg": "white", "bd": 0, "relief": "flat"}

tk.Button(btn_frame, text="1. Write and Sort Fruits (Alphabetical)", command=exercise1_fruits, **btn_style).grid(row=0, column=0, padx=5, pady=4)
tk.Button(btn_frame, text="2. Write and Sort Random Numbers (Ascending)", command=exercise2_numbers, **btn_style).grid(row=1, column=0, padx=5, pady=4)
tk.Button(btn_frame, text="3. Create and Sort Students by Grade", command=exercise3_students_grade, **btn_style).grid(row=2, column=0, padx=5, pady=4)
tk.Button(btn_frame, text="4. Sort Students by Grade then Age (Descending)", command=exercise4_students_grade_age, **btn_style).grid(row=3, column=0, padx=5, pady=4)

# Add Student Section
add_frame = tk.LabelFrame(root, text="Add New Student (Exercise 5)", font=("Segoe UI", 11, "bold"),
                          bg="#f8f8f8", fg="#333", padx=10, pady=10)
add_frame.pack(pady=10)

tk.Label(add_frame, text="Name:", bg="#f8f8f8").grid(row=0, column=0, sticky="e", padx=5)
tk.Label(add_frame, text="Age:", bg="#f8f8f8").grid(row=1, column=0, sticky="e", padx=5)
tk.Label(add_frame, text="Grade:", bg="#f8f8f8").grid(row=2, column=0, sticky="e", padx=5)

name_entry = tk.Entry(add_frame, width=25)
age_entry = tk.Entry(add_frame, width=25)
grade_entry = tk.Entry(add_frame, width=25)

name_entry.grid(row=0, column=1, padx=5, pady=2)
age_entry.grid(row=1, column=1, padx=5, pady=2)
grade_entry.grid(row=2, column=1, padx=5, pady=2)

tk.Button(add_frame, text="Add Student & Sort by Age", command=exercise5_add_student,
          font=("Segoe UI", 10), bg="#107C10", fg="white", width=25).grid(row=3, column=0, columnspan=2, pady=8)

# Output Box
output_box = scrolledtext.ScrolledText(root, width=75, height=12, font=("Consolas", 10), bg="#ffffff", wrap=tk.WORD)
output_box.pack(pady=10)
output_box.config(state="disabled")

# Status Bar
status_label = tk.Label(root, text="Status: Ready", bg="#e0e0e0", anchor="w", font=("Segoe UI", 10))
status_label.pack(fill="x", side="bottom")

# Exit Button
tk.Button(root, text="Exit Program", command=root.destroy,
          font=("Segoe UI", 11), bg="#D83B01", fg="white", width=30).pack(pady=8)

root.mainloop()

