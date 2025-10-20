# student_records_manager.py
# Smart version: with validation + flexible sorting + search

import os

FILENAME = "student_records.txt"

# --- Helper functions ---
def is_valid_grade(grade):
    return grade.upper() in ["A", "B", "C", "D", "F"]

def is_valid_age(age):
    return age.isdigit() and 5 <= int(age) <= 120

# --- Core functions ---
def add_student():
    name = input("Enter student name: ").strip()
    age = input("Enter age: ").strip()
    while not is_valid_age(age):
        print("Invalid age! Please enter a valid number between 5 and 120.")
        age = input("Enter age: ").strip()

    grade = input("Enter grade (A–F): ").strip().upper()
    while not is_valid_grade(grade):
        print("Invalid grade! Please enter one of the following: A, B, C, D, F.")
        grade = input("Enter grade (A–F): ").strip().upper()

    with open(FILENAME, "a") as file:
        file.write(f"{name},{age},{grade}\n")
    print(f"Record for {name} added successfully!")

def view_students():
    if not os.path.exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        print("No student records found.")
        return

    with open(FILENAME, "r") as file:
        records = [line.strip().split(",") for line in file]

    print("\nSort students by:")
    print("1. Name")
    print("2. Age")
    print("3. Grade")
    sort_choice = input("Enter your choice (1-3): ").strip()

    if sort_choice == "1":
        sorted_records = sorted(records, key=lambda x: x[0].lower())
    elif sort_choice == "2":
        sorted_records = sorted(records, key=lambda x: int(x[1]))
    elif sort_choice == "3":
        grade_order = {"A": 1, "B": 2, "C": 3, "D": 4, "F": 5}
        sorted_records = sorted(records, key=lambda x: grade_order.get(x[2].upper(), 99))
    else:
        print("Invalid choice! Defaulting to sorting by name.")
        sorted_records = sorted(records, key=lambda x: x[0].lower())

    print("\n--- Student Records (Sorted) ---")
    for name, age, grade in sorted_records:
        print(f"Name: {name} | Age: {age} | Grade: {grade}")
    print("------------------------")

def update_student():
    name_to_update = input("Enter the student name to update: ").strip()
    if not os.path.exists(FILENAME):
        print("No records available to update.")
        return

    updated = False
    with open(FILENAME, "r") as file:
        lines = file.readlines()

    with open(FILENAME, "w") as file:
        for line in lines:
            name, age, grade = line.strip().split(",")
            if name.lower() == name_to_update.lower():
                print(f"Updating record for {name}")
                new_age = input("Enter new age: ").strip()
                while not is_valid_age(new_age):
                    print("Invalid age! Please enter a valid number between 5 and 120.")
                    new_age = input("Enter new age: ").strip()

                new_grade = input("Enter new grade (A–F): ").strip().upper()
                while not is_valid_grade(new_grade):
                    print("Invalid grade! Please enter one of the following: A, B, C, D, F.")
                    new_grade = input("Enter new grade (A–F): ").strip().upper()

                file.write(f"{name},{new_age},{new_grade}\n")
                updated = True
                print(f"Record for {name} updated successfully!")
            else:
                file.write(line)

    if not updated:
        print(f"No record found for {name_to_update}.")

def delete_student():
    name_to_delete = input("Enter the student name to delete: ").strip()
    if not os.path.exists(FILENAME):
        print("No records available to delete.")
        return

    deleted = False
    with open(FILENAME, "r") as file:
        lines = file.readlines()

    with open(FILENAME, "w") as file:
        for line in lines:
            name, _, _ = line.strip().split(",")
            if name.lower() != name_to_delete.lower():
                file.write(line)
            else:
                deleted = True

    if deleted:
        print(f"Record for {name_to_delete} deleted successfully!")
    else:
        print(f"No record found for {name_to_delete}.")

def search_student():
    if not os.path.exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        print("No student records to search.")
        return

    search_name = input("Enter student name to search: ").strip().lower()
    found = False
    with open(FILENAME, "r") as file:
        for line in file:
            name, age, grade = line.strip().split(",")
            if search_name in name.lower():
                print(f"Found -> Name: {name} | Age: {age} | Grade: {grade}")
                found = True

    if not found:
        print(f"No records found for '{search_name}'.")

# --- Main Program Loop ---
while True:
    print("\n=== Student Record Manager ===")
    print("1. Add Student")
    print("2. View Students (Sorted)")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Search Student")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        update_student()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        search_student()
    elif choice == "6":
        print("Goodbye! 👋")
        break
    else:
        print("Invalid choice! Please select a number from 1 to 6.")
