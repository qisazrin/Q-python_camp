#Loops
# for loops : known iteration
# while loops : Unknown iteration
# Rule;
# if u can count use FOR LOOP
# if waiting for condition use WHILE LOOP

# For loop
for i in range(5):      # 0,1,2,3,4
    print(i)

for i in range(1,6):    # 1,2,3,4,5
    print(i)

for i in range(0,10,2):   # 2,4,6,8
    print(i)


# While loop
count = 0
while count < 5:
    print(count)
    count += 1      # dont forget this one, if not it will be infinity loops

# loop contro; statement
for i in range(10):
    if i == 3:
        continue     # skip iteration
    if i == 7 :
        break        # Exit the loop
    print(i)

#Nested loop:
for i in range(2):
    for j in range(3):
        print(f"({i},{j})")

# Exercise 1
# 1. create a multiplication table generator

# table range
start = 1
end = 10

# Outer loop - goes through each row number
for row in range(start, end + 1):

    # Inner loop - goes through each column number
    for col in range(start, end + 1):

        # Multiply row and column
        result = row * col
        print(result, end="\t")  # \t adds a tab space

    # Move to the next line after each row
    print()

#Exersice 2
# 2. a program that finds all prime numbers up to 20.
# A prime number is only divisible by 1 and itself

for number in range(2,21):
    prime= True

     # Check if anything divides evenly into this number
    for j in range (2,number):
        if number % j == 0:
            prime = False
            break

        # print prime number
        if prime:
            print(number)