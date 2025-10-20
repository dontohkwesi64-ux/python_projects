# step2_read_file.py

# Open the file in read mode ('r')
file = open("my_numbers.txt", "r")

# Read all lines into a list
numbers = file.readlines()

# Close the file
file.close()

# Print the numbers
print("Numbers in the file:")
for number in numbers:
    print(number.strip())  # .strip() removes the newline characters
