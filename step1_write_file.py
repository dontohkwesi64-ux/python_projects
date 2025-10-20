# step1_write_file.py

# Open a file in write mode ('w')
# If the file does not exist, it will be created
file = open("my_numbers.txt", "w")

# Write some numbers to the file
file.write("10\n")
file.write("5\n")
file.write("8\n")
file.write("20\n")
file.write("1\n")

# Close the file to save changes
file.close()

print("File created and numbers written successfully!")
