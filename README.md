# 🐍 Q-Python Camp

> A beginner-friendly Python bootcamp covering the fundamentals of Python, databases, and interactive web app development with Streamlit.
---

## 📖 About

**Q-Python Camp** is a structured Python bootcamp designed for beginners who want to go from zero programming knowledge to building real-world applications. The camp walks you through Python fundamentals step by step, then progresses into working with databases and finally building interactive web dashboards using Streamlit.

Whether you are a student, a career switcher, or just curious about programming — this bootcamp is open to everyone and free to learn from.

---

## 🗺️ Learning Path

```
Python Basics  ──►  Data Structures  ──►  OOP  ──►  Databases  ──►  APIs  ──►  Streamlit Apps
```

---

## 📚 What You Will Learn

### 🐣 Part 1 — Python Fundamentals
Get comfortable with the Python language from scratch.

| Topic | Description |
|---|---|
| Variables & Data Types | Strings, integers, floats, booleans |
| Operators | Arithmetic, comparison, logical operators |
| Control Flow | `if`, `elif`, `else` conditions |
| Loops | `for` and `while` loops, `break`, `continue` |
| Functions | Defining functions, parameters, return values |
| Modules & Imports | Using built-in and third-party modules |
| Error Handling | `try`, `except`, `finally` blocks |
| File Handling | Reading and writing `.txt` and `.csv` files |

---

### 🧱 Part 2 — Data Structures
Learn how Python organises and stores collections of data.

| Topic | Description |
|---|---|
| Lists | Ordered, mutable sequences |
| Tuples | Ordered, immutable sequences |
| Dictionaries | Key-value pairs |
| Sets | Unique unordered collections |
| List Comprehensions | Concise ways to build lists |

---

### 🏗️ Part 3 — Object-Oriented Programming (OOP)
Write clean, reusable code using classes and objects.

| Topic | Description |
|---|---|
| Classes & Objects | Defining and instantiating classes |
| Attributes & Methods | Instance variables and class functions |
| Inheritance | Extending base classes |
| Encapsulation | Private and public attributes |

---

### 🗄️ Part 4 — Databases
Connect Python to real databases and perform full CRUD operations.

#### SQLite3 (Local Database)
- Setting up a local SQLite database
- Creating tables and schemas
- Inserting, reading, updating, and deleting records
- Using `sqlite3` module from Python's standard library
- Querying with SQL inside Python scripts

#### MongoDB (NoSQL Database)
- Understanding NoSQL vs SQL concepts
- Connecting to MongoDB (local or Atlas cloud)
- Working with collections and documents
- CRUD operations using `pymongo`
- Managing a `DatabaseManager` class for clean code structure
- Using `.env` files to store connection strings safely

---

### ⚡ Part 5 — APIs with FastAPI
Build and consume REST APIs using FastAPI.

| Topic | Description |
|---|---|
| HTTP Methods | GET, POST, PUT, DELETE, PATCH |
| Pydantic Models | Request and response validation |
| Route Parameters | Path and query parameters |
| Status Codes | Proper HTTP response codes |
| Connecting API to MongoDB | Full backend with database integration |
| Running with Uvicorn | Serving the API locally |

---

### 🌐 Part 6 — Streamlit Web Apps
Turn your Python scripts into interactive web dashboards — no frontend experience needed.

| Topic | Description |
|---|---|
| Setting Up Streamlit | Installation and running your first app |
| UI Components | Buttons, inputs, forms, selectboxes, sliders |
| Layouts | Columns, tabs, expanders, sidebar navigation |
| Displaying Data | Tables, dataframes, charts, metrics |
| State Management | `st.session_state` for interactive navigation |
| Connecting to APIs | Calling FastAPI endpoints from Streamlit |
| Full-Stack Mini Project | Streamlit + FastAPI + MongoDB database manager |

---

## 🛠️ Prerequisites

No prior programming experience is needed. Just make sure you have these installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/) (recommended editor)
- [MongoDB](https://www.mongodb.com/try/download/community) (for database lessons) or a free [MongoDB Atlas](https://www.mongodb.com/atlas) account

---

## ⚙️ Setup & Installation

**1. Create repository**
```bash
https://github.com/your github name/repo name.git
cd repo name
```

**2. Create and activate a virtual environment in VScode terminal**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your environment variables**

Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb://localhost:27017
# or for MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## ▶️ Running the Projects

### Run a Python lesson file
```bash
python 01-Variables.py
```

### Start the FastAPI backend
```bash
python 18-FastMongo.py
# or
uvicorn 18-FastMongo:app --host 000.0.0.1 --port 8000 --reload
```

### Launch the Streamlit app
```bash
streamlit run streamlit_app.py
```

> ⚠️ Make sure the FastAPI server is running **before** launching the Streamlit app.

---

## 📦 Dependencies

```txt
fastapi
uvicorn
pymongo
python-dotenv
pydantic[email]
streamlit
pandas
requests
```

Install all at once:
```bash
pip install fastapi uvicorn pymongo python-dotenv "pydantic[email]" streamlit pandas requests
```

---

## 📁 Project Structure

```
Q-python_camp/
│
├── 📂 slides/              # Lesson slide decks (PDF/PPTX)
├── 📂 notes/               # PDF notes and cheat sheets
│
├── 01-Variables.py         # Part 1: Python basics
├── 02-DataTypes.py
├── 03-Operators.py
├── 04-ControlFlow.py
├── 05-Loops.py
├── 06-Functions.py
├── 07-Modules.py
├── 08-ErrorHandling.py
├── 09-FileHandling.py
├── 10-Lists.py             # Part 2: Data structures
├── 11-Tuples.py
├── 12-Dictionaries.py
├── 13-Sets.py
├── 14-OOP.py               # Part 3: Object-oriented programming
├── 15-SQLite.py            # Part 4: Databases
├── 16-MongoDB.py
├── 17-FastAPI.py           # Part 5: APIs
├── 18-FastMongo.py         # FastAPI + MongoDB integration
│
├── streamlit_app.py        # Part 6: Streamlit web app
├── mongoDB.py              # MongoDB DatabaseManager class
│
├── .env                    # Environment variables (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

Made with ❤️ for anyone who wants to learn Python the practical way.  
If this helped you, give it a ⭐ on GitHub!
