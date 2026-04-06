# Error handling
# process of anticipating, catching, and managing errors that occur
# during program execution

# basic exceptioon handling
try:
    number = int(input("Enter a number :"))
    result = 10 / number
    print(f"Result : {result}")
except ValueError:
    print("Invalid input! please enter a number")
except ZeroDivisionError:
    print("cannot divide by zero!")

# using else and finally
try:
    file = open("data.txt", "r")
except FileExistsError:
    print("File not found")
else:
    #execute if no exception occured
    content = file.read()
    print("File read succesfully")
finally:
    #always executes
    if 'file' in locals() and not file.closed():
        file.close()
    print("cleanup complete")

# Rising exceptions
def validation_age(age):
    if age < 0 :
        raise ValueError ("age cannot be negative")
    if age > 150:
        raise ValueError ("age seems unrealistic")
    return True

try:
    validation_age(-5)
except ValueError as e:
    print(f"validation error : {e}")

