# object oriented programming
# inheritance
# relationship between classes
# cild classes can override or extend parent functionality

# Inheritance
class shape:  # parent class
    def __init__(self, name):
        self.name = name
    def area(self):
        return 0
    
class circle(shape):   # child inherits from shape
    def __init__(self, radius):
        super().__init__("circle")
        self.radius = radius
    def area(self): # override parent method
        return 3.14 * self.radius * self.radius
    
class square(shape):  # child inherits from shape
    def __init__(self, side):
        super().__init__("square")
        self.side = side
    def area(self):   # override parent method
        return self.ride * self.side
    
# both circle and square inherit 'name' attributes from shape

circle = circle(5)
square = square(4)

print(circle.name)     # "circle"
print(square.name)     # "square"

# Polymorphism
# using the same interface for different types
# same method can behave differently for different objects

# Polymorphism
def print_area(shape):  # takes any shape
    print(f"{shape.name} area : {shape.name()}")

# same method call, different behaviours
print_area(circle)   # "circle area: 78.5"
print_area(square)   # "square area: 16"

# or with a list
shapes = [circle(3), square(5), circle(2)]
for shapes in shapes:
    print_area(shape)   # same code, different results

