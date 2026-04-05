# Sets
# a set of data within curly bracket {...}
# unordered collection of elements

#set operations
fruits = {"grape", "pisang", "durian"}
numbers = { 3, 4, 5, 7, 9}

fruits.add("papaya")     # add element
fruits.remove("durian")  # remove element
fruits.discard("kiwi")   # remove if exists (no error)
print(fruits)

# sets mathematic operations
set1 = {2, 4, 6, 8}
set2 = {1, 3, 4, 7}

print(set1.union(set2))         # {1,2,3,4,6,7,8}
print(set1.intersection(set2))  # {4} 
print(set1.difference(set2))    # {8,2,6}

#Exercise 1
# 1. create a system that store student grade as tuple(name,subject,grade)
# and uses sets to find unique subjects and students

grades = [ ("Alice", "Math", 85), 
           ("Bob", "Science", 92),
           ("Alice", "Science", 78),
           ("Charlie", "Math", 90),
           ("Bob", "Math", 88),
           ("Alice", "English", 95)]

unique_subjects= set()
unique_students= set()

for names, subjects, grade in grades:
    unique_subjects.add(subjects)  #duplicate are ignore automatically
    unique_students.add(names)     # add only if not in set
    
print(f"unique students : {unique_students}")
print(f"unique_subjects : {unique_subjects}")