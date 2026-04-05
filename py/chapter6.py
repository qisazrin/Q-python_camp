#Lists
# a set of data within square bracket [...]

fruits = ["apple","grape","banana"]
numbers = [1,2,3,4,5]
mixed = ["hello", 1,34,True]
empty_list =[]

# accessing elements
print(fruits[0])      # "apple"
print(fruits[-1])     # 'banana'
print(numbers[1:4])   # [2,3,4]
print(numbers[:3])    # [1,2,3]
print(numbers[2:])    # [3,4,5]

# List operation : CRUD a list
fruits.append("mango")    #add to end
fruits.insert(1 , "kiwi") # insert at index
fruits.remove("apple")    # remove value
popped = fruits.pop()     # remove and return last
fruits.sort()             # sort in place
fruits.reverse()          # reverse in place

# list operations
len(fruits)               # length
"apple" in fruits         # check membership
fruits + ["pemogranate"]  # concatenation 
fruits * 2                # repetition

print(len(fruits))

# Exersice 1
# create a grocery list and perform various operation

grocery = ["chicken","beef","milk","bayam","chili"]

print(grocery.append("milo"))
print(grocery.insert(3, "kobis"))
print(grocery.reverse())
print(grocery + ["done"])

# Exercise 2
# 2. write a program that finds the largest and smallest number in list

num = [2, 3, 4, 5, 6, 7, 8, 23, 10, 55, 21, 90, 1 ]

small = min(num)
large = max(num)

print(num)
print(f"the smallest : {small}")
print(f"the largest : {large}")