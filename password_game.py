password = "sohit123"
tries = 0

while tries < 3:
    guess = input("Enter password: ")
    if guess == password:
        print("Login successful")
        break
    else:
        print("Wrong password. Tries left:", 2 - tries)
    tries += 1
else:
    print("Access denied")
