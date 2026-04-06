# Functions
# reusable block of code that do specific task

#function with parameters
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Bambi")

# functions with return values
def add_number(a,b):
    return a + b

result = add_number(5,9)
print(result)   # 14

# default parameters
def greet_with_title(name, title="Mr. "):
    return f"Hello, {title} {name}!"

print(greet_with_title("smith"))    # Hello, Mr.smith
print(greet_with_title("Johnny", "Dr."))  #Hello, Dr.Johnny

#agrs
# access by index:agrs[0]
# unpacking:func(*list)

#*agrs - variable number of argruments
def sum_all(*args):
    return sum(args)
print(sum_all(1 , 2, 3, 4, 5))  #15

#kwargs
# acess by key : kwargs["key"]
# unpacking: func(**dict)

# kwargs - keyword arguments
def print_info(**kwargs):
    for key , value in kwargs.items():
        print(f"{key} : {value}")
print_info(name="mirul", age=43, city="Mississippi")
#name : mirul
#age : 43
#city : Mississippi

#args & kwargs
#combining *args & **kwargs
def flexible_func(*args,**kwargs):
    print("positional arguments : ",args)  #positional arguments :  (1, 2, 3)
    print("keyword arguments : ", kwargs)  #keyword arguments :  {'name': 'Halizah', 'age': 88}
flexible_func(1,2,3, name="Halizah", age=88)

#lambde
# anonymous function
# small function
square = lambda x: x**2
print(square(5)) # 25

add = lambda x, y: x + y
print(add(3,4))  # 7


# Exercise 1
# 1. write a function that check if a number is prime
def prime_number():
    for number in range(2,21):
        prime= True
        for j in range (2,number):
            if number % j == 0:
                prime = False
                break
        if prime:
            print(number)

prime_number()

# 2. build a temperature converter function (celcius to fahrenheit)
def celcius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

print(celcius_to_fahrenheit(0))   # 32.0
print(celcius_to_fahrenheit(100)) # 212.0
print(celcius_to_fahrenheit(37))  # 98.6