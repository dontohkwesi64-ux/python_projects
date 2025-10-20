# sort_students_by_age.py

import os

FILENAME = "student_records.txt"

if not os.path.exists(FILENAME):
    print(f"No file named {FILENAME} found!")
    exit()

# Read student records
with open(FILENAME, "r") as file:
    records = [line.strip().split(",") for line in file]

# Convert age to integer and sort by age descending
sorted_records = sorted(records, key=lambda x: int(x[1]), reverse=True)

# Display sorted students
print("\n--- Students Sorted by Age (Descending) ---")
for name, age, grade in sorted_records:
    print(f"Name: {name} | Age: {age} | Grade: {grade}")
print("-------------------------------------------")
