def calculator():
    print("Select an operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")

    
    choice = input("Enter choice (1/2/3/4): ")

    if choice in ('1', '2', '3', '4'):
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Error: Invalid input. Please enter numerical values.")
            return

        # Perform the requested operation
        if choice == '1':
            print(f"Result: {num1} + {num2} = {num1 + num2}")
            
        elif choice == '2':
            print(f"Result: {num1} - {num2} = {num1 - num2}")
            
        elif choice == '3':
            print(f"Result: {num1} * {num2} = {num1 * num2}")
            
        elif choice == '4':
            # Handle division by zero
            if num2 == 0.0:
                print("Error: Cannot divide by zero.")
            else:
                print(f"Result: {num1} / {num2} = {num1 / num2}")
    else:
        print("Invalid choice. Please select a valid operation number.")


if __name__ == "__main__":
    calculater()
    
