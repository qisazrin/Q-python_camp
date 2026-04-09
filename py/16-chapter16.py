# Mongo Database Management

from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()    # load environment variables from .env file

mongo_uri= os.getenv('mongo_API')

class DatabaseManager:
    def __init__(self, db_name="my_database", connection_string=mongo_uri):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.users_collection = self.db.users
        self.posts_collection = self.db.posts
        self.init_database()

    def init_database(self):
        """Initialize the database with necessary indexes and sample data."""
        # Create unique index on email to prevent duplicates
        self.users_collection.create_index("email", unique=True)
        # create index on user_id and created_at for efficient querying of posts
        self.posts_collection.create_index("user_id")

    def create_user(self, name, email, age):
        """Create a new user in the database."""
        try:
            user = {
            "name": name,
            "email": email,
            "age": age,
            "created_at": datetime.now()
        }
            result = self.users_collection.insert_one(user)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
        
    def create_post(self, user_id, title, content):
        """Create a new post for a user."""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            post = {
                "user_id": user_object_id,
                "title": title,
                "content": content,
                "created_at": datetime.now()
            }
            result = self.posts_collection.insert_one(post)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating post: {e}")
            return None
        
    def get_user(self, user_id):
        """Get all users."""   # FIX 1: docstring updated to reflect actual behaviour
        try:
            users = list(self.users_collection.find())
            for user in users:
                user["_id"] = str(user["_id"])
            return users
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_posts_by_user(self, user_id):
        """Get posts by user."""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            posts = list(self.posts_collection.find
                         ({"user_id": user_object_id}
                          ).sort("created_at", -1))

            for post in posts:
                post["_id"] = str(post["_id"])
                post["user_id"] = str(post["user_id"])

            return posts
        except Exception as e:
            print(f"Error getting posts: {e}")
            return None
        
    def delete_user(self, user_id):
        """Delete a user and their posts."""
        try:
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id

            # FIX 2: delete user's posts first (was using wrong collection & filter)
            self.posts_collection.delete_many({"user_id": user_object_id})
            # FIX 3: then delete the user (was using wrong collection)
            result = self.users_collection.delete_one({"_id": user_object_id})
            return result.deleted_count > 0
        
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        
    def close_connection(self):
        """Close the database connection."""
        self.client.close()

def display_menu():
    print("\nMenu:")
    print("1. Create User")
    print("2. Create Post")
    print("3. Get All Users")
    print("4. Get Posts by User")
    print("5. Delete User")
    print("6. Exit")
    print("-"*40)

def main():
    """Main interactive CLI function"""
    try:
        db = DatabaseManager()
        print("Welcome to the MongoDB Database Manager!")
    except Exception as e:
        print(f" X Error connecting to database: {e}")
        print(" Make sure Mongodb is running on localhost:27017 and try again.")
        return
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Create User ---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            try:
                age = int(input("Enter age: ").strip())
                user_id = db.create_user(name, email, age)
                if user_id:
                    print(f"User created successfully! ID: {user_id}")
            except ValueError:
                print("Invalid age. Please enter a valid number.")
        
        # FIX 4: choice 2 and 3 were swapped — now match the display_menu() order
        elif choice == "2":
            print("\n--- Create new post ---")
            user_id = input("Enter user ID: ").strip()
            title = input("Enter post title: ").strip()
            content = input("Enter post content: ").strip()
            post_id = db.create_post(user_id, title, content)
            if post_id:
                print(f"Post created successfully! ID: {post_id}")
            else:
                print("Failed to create post. Make sure the user ID is correct.")

        elif choice == "3":
            print("\n--- All Users ---")
            users = db.get_user(None)   # FIX 5: was calling undefined db.get_all_users()
            if users:
                for user in users:
                    print(f"ID: {user['_id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}")
            else:
                print("No users found.")
        
        elif choice == "4":
            print("\n--- View User Posts ---")
            user_id = input("Enter user ID: ").strip()
            posts = db.get_posts_by_user(user_id)
            if posts:
                for post in posts:
                    print(f"ID: {post['_id']}")
                    print(f"Title: {post['title']}")
                    print(f"Content: {post['content']}"), 
                    print(f"Created At: {post['created_at']}")
                    print("-"*30)
            else:
                print("No posts found for this user.")
        
        elif choice == "5":
            print("\n--- Delete User ---")
            user_id = input("Enter user ID to delete: ").strip()
            confirm = input("Are you sure you want to delete this user and all their posts? (yes/no): ").strip().lower()
            if confirm == "yes":
                if db.delete_user(user_id):
                    print("User and their posts deleted successfully.")
                else:
                    print("Failed to delete user. Make sure the user ID is correct.")
        
        elif choice == "6":
            print("\nClosing database connection....")
            db.close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
    
