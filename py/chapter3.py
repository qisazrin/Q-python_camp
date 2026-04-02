# Input/Output validation
name = input("Enter your name :")
height = int(input("Enter your height :"))    #Integer input

#Input validation
while True:
    try:
        age= int(input("Enter age :"))
        if age > 17:
            break
        else:
            print("Age must be positive!")
    except ValueError:
        print("please enter a valid number!")

#ouput validation
print(f"Hello,{name}!")
print(f"you are {age} years old and {height} feet tall.")


# excersise 1
while True:
    try:
        num_first = float(input("Enter first number: "))
        num_second = float(input("Enter second number: "))

        if num_first <= 0 or num_second <= 0:
            print("Fill positive number only!")
        else:
            num_cal = num_first + num_second
            break  # Valid input received, exit loop

    except ValueError:
        print("Please enter a valid number!")

# Output
print("Result:", num_cal)
    
