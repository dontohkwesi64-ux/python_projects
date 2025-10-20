def calculator():
    while True:
        print("\nSimple Calculator")
        print("Choose an operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("Q. Quit")
        
        choice = input("Enter choice (1/2/3/4 or Q to quit): ").lower()

        if choice == 'q':
            print("Goodbye Bossu! 👋")
            break

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                print(f"The result is: {num1 + num2}")
            elif choice == '2':
                print(f"The result is: {num1 - num2}")
            elif choice == '3':
                print(f"The result is: {num1 * num2}")
            elif choice == '4':
                if num2 != 0:
                    print(f"The result is: {num1 / num2}")
                else:
                    print("Error: Division by zero is not allowed.")
        else:
            print("Invalid choice. Please try again.")

# Run the calculator
calculator()
