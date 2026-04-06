# Classes and Objects

# Clases
# template of creating object
# basic class definition
class person:
    #class attribution (shared by all instances)
    species = "Homo sapiens"

# Constructor method
    def __init__(self, name, age):
    #instance attributes
        self.name = name
        self.age = age

# Instance method
    def introduction(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

# Method with parameters
    def birthday(self):
        self.age += 1
        return f"Happy birthday! {self.name} is now {self.age}."

# Objects
# instance of classes

# creatiing objects (instances)
person1 = person("Mia", 23)
person2 = person("Aisyah", 29)

# acessing attributes
print(person1.name)  # "Mia"
print(person1.age)   # 23

# calling methods
print(person1.introduction())   # Hi, I'm Mia and I'm 23 years old
print(person1.birthday())       # Happy birthday ! Mia is now 24

# class attributes
print(person2.species)          # Homo sapiens
print(person1.species)


class Bankaccount:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transaction_history = []
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            return f"Deposited ${amount}. New balance: ${self.balance}"
        else:
            return "Invalid deposit amount"
        
    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        else:
            return "Invalid withdrawal amount or insufficient funds"
    
    def get_balance(self):
        return f" Current balance: ${self.balance}"
    
    def get_transaction_history(self):
        return self.transaction_history

# using the bankaccount class
account = Bankaccount("0023", "Khadijah", 7600)
print(account.deposit(500))
print(account.withdraw(200))
print(account.get_balance())

# Exercise 1
# 1. create a simple game character class and health , attack and heal method.
class Miya_theShooter:
    def __init__(self, health, attack_power, heal_amount):
        self.health = health
        self.attack_power = attack_power
        self.heal_amount = heal_amount
    
    def attack(self, enemy):
        enemy.health -= self.attack_power
        return f"Attack! enemy health now {enemy.health}"
    
    def enemy_attack(self,enemy):
        self.health -= enemy.attack_power
        return f"Miya Been attack! Miya's health is {self.health}"
    
    def heal(self):
        self.health += self.heal_amount
        return f"Heals! Miya's health is now {self.health}"

miya = Miya_theShooter(health=100, attack_power=25, heal_amount=15)
enemy = Miya_theShooter(health=80, attack_power=10, heal_amount=5)

print(miya.attack(enemy))         # Attack! enemy health now 55
print(miya.enemy_attack(enemy))   # Miya Been attack! Miya's health is 90
print(miya.heal())                # Heals! Miya's health is now 105