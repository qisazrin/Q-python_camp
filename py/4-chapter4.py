# Condition statement
# if else : 2 conditions
# if elif else : more than 2 conditions

age = int(input("Enter age :"))
if age >= 18:
    print ("you are an adult")
else:
    print("you are a minor")


score = int(input("Enter your score :"))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"your grade is : {grade}")

# and and or conditional statement
# and : condition must be True
# or : at least one condition must be True

#and conditon
user_age = int(input("Enter age :"))
has_license = True

if user_age >=18 and has_license:
    print("you allowed to drive")
else:
    print("you are underage")

# or condition
day= "saturday"
if day == "saturday" or day == "sunday":
    print("it's the weekend!")
else:
    print("it's a weekday")


# Nested conditions : condition within condition

weather = str(input("Enter weather condition (sunny or cold): "))
temperature = int(input("Enter temperature: "))

if weather == "sunny":
    if temperature > 28:
        print("It's sunny and warm")
    else:
        print("It's sunny but cool")
elif weather == "cold":
    if temperature < 27:
        print("Kinda cold day >,<")


# operators
# `=` Assignment
# `==` Equal to
# `===` Strict equality
# `!=` Not equal
# `>` Greater than
# `<` Less than
# `>=` Greater and equal to
# `<=` Less and equal to

# Exercise 1
# categorize bmi

weight = float(input("Enter weight :"))
height = float(input("Enter height : "))
bmi = weight /(height / 100) ** 2
bmi = round(bmi, 1)

if bmi <= 18.5:
    category = "Underweight"
elif bmi <= 24.9:
    category = "Normal"
elif bmi <= 29.9:
    category = "Overweight"
else:
    catergory = "Obesity"

print(f"Bmi : {bmi}")
print(f"Category : {category}")