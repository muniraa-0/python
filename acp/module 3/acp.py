try:
    age = int(input("Enter your age: "))

    if age < 0:
        print("Invalid age! Age cannot be negative.")
    else:
        print("Valid age.")

        if age % 2 == 0:
            print("The age is Even.")
        else:
            print("The age is Odd.")

except ValueError:
    print("Error! Please enter a valid number.")