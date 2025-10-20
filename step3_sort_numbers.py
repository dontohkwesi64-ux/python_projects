# step3_sort_numbers.py

# Open the file in read mode
with open("my_numbers.txt", "r") as file:
    # Read all lines, convert each line to an integer
    numbers = [int(line.strip()) for line in file]

# Sort numbers in descending order
numbers.sort(reverse=True)

# Print sorted numbers
print("Numbers sorted in descending order:")
for number in numbers:
    print(number)
