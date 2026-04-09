# string manipulation
'''single quote
   double quote
   triple quote'''

sing_quote = 'hello'
doub_quote = "world"
trip_quote = '''multiple line strings'''

# string indexing and slicing

text = "python bootcamp"

print(text[0])    # first character
print(text[-1])   # last character
print(text[0:6])  # slice 0 to 5
print(text[:6])   # from start to 5
print(text[7:])   # 7 to end


# string method
''' - len(): lengh
    - strip(): remove space
    - upper(): UPPERCASE
    - lower(): lowercase
    - title(): Titlecase
    - replace(): ("old",'New")'''

name= "apple pie"

print(len(name))
print(name.strip())
print(name.upper())
print(name.lower())
print(name.title())
print(name.replace("pie","jack"))

# string formatting
''' - f-string
    - str.format()
    - %-formatting '''

name1= 'alisyia yus'
age = 32

msg_1= f'My name is {name1} and i am {age} years old'    # f-string
msg_2= "my name is {} and i am {} years old".format(name1,age) 
msg_3= "my name is %s and i am %d years old" %(name1,age)

print(msg_1)
print(msg_2)
print(msg_3)

# exercie 1

text = "python is a powerful programming language. It's easy to learn and versatile!You  can  use  Python  for  web  development,data  science, and automation. The syntax is clean and readable. This makes Python perfect for beginners and experts alike."

print(len(text))
print(len(text.strip()))