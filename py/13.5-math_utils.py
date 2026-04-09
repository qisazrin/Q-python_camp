def add(a,b):
    """ add twon numbers"""
    return a + b
def multiply(a,b):
    """ calculate two numbers"""
    return a * b
def factorial(n):
    """ calculate factorial of n"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

PI = 3.14159

class calculator:
    def __init__(self):
        self.history = []

    def calculate(self, operation, a, b):
        if operation == "add":
            result = add(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        else:
            result = None
            self.history.append(f"{operation}({a}, {b}) - {result}")
            return result