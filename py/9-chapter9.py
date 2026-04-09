#Dictionaries
#key-value data structure
#key need to be unique
#Value can be duplicated

student = {"name": "Ahmand",
           "age" : 21,
           "grade" : "A",
           "courses" : ["math","science", "English"]}

#acessing and modifying
print(student["name"])               #"Ahmad"
print(student.get("age"))            # 21
student["age"] = 22                  # modify value
student["email"] = "ahmad11@gmail.com"  # add new key-value


# dictionaries method
keys = student.keys()        # get all keys
values = student.values()    # get all values
items = student.items()      # get kay-value pairs

print(keys)         #dict_keys(['name', 'age', 'grade', 'courses', 'email'])
print(values)       #dict_values(['Ahmand', 21, 'A', ['math', 'science', 'English'], 'ahmad11@gmail.com'])
print(items)        #dict_items([('name', 'Ahmand'), ('age', 21), ('grade', 'A'), ('courses', ['math', 'science', 'English']), ('email', 'ahmad11@gmail.com')])


# iterating dictionaries
#1
for key in student:
    print(f"{key} : {student[key]}")
#2
for key, value in student.items():
    print(f"{key} : {value}")

# for both style give the same ouput
#name : Ahmand
#age : 21
#grade : A
#courses : ['math', 'science', 'English']
#email : ahmad11@gmail.com

#Nested dictionaries
company = {
    "employees" : {
        "ali" : {"age" : 33, "deparment" : "IT"},
        "syila" : {"age" : 29, "deparment": "HR"}},
    "departments" : ["IT", "HR", "Operation"]}

print(company["employees"].items())   #dict_items([('ali', {'age': 33, 'deparment': 'IT'}), ('syila', {'age': 29, 'deparment': 'HR'})])
print(company["departments"])         #['IT', 'HR', 'Operation']


#exercise 1
# 1. create a dictionary called student_records with the following infomation;

student_records = {
    "student_001": {
        "name" : "John",
        "age" : 19,
        "major" : "Computer Science", 
        "grades" : [85 , 92 , 78]},
    "student_002" : {
        "name" : "sarah",
        "age" : 20,
        "major" : "Biology", 
        "grades" : [90 , 88 , 95]}}

# 2. add a new student 
student_records["student_003"] = {"name" : "Mike",
                                  "age" : 18,
                                  "major" : "Math",
                                  "grades" : [82 , 79 , 91]}

# 3. update john's age to 20
student_records["student_001"]["age"] = 20

# 4. loop through the dictionary and print each student's information in this format:
# student ID : id , name:[name], major:[major]
for student_id , info in student_records.items():
    print(f" student_ID : {student_id}, Name : {info['name']} , Major : {info['major']}")
