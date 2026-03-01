# FullStack Pro - Complete Internship Project
### By Divya Sumpagi | B.Sc Computer Science

---

## 📁 PROJECT STRUCTURE

```
fullstack_project/
│
├── app.py                  ← Main Flask backend (RUN THIS FILE)
├── database.db             ← SQLite database (auto-created when you run app.py)
├── requirements.txt        ← Python packages needed
├── README.md               ← This file
│
├── templates/              ← All HTML pages (Jinja2 templates)
│   ├── base.html           ← Base layout (navbar, footer, flash messages)
│   ├── index.html          ← Home page
│   ├── register.html       ← Registration page
│   ├── login.html          ← Login page
│   ├── dashboard.html      ← Dashboard (after login)
│   ├── contact.html        ← Contact page
│   ├── students.html       ← View all students
│   ├── add_student.html    ← Add student form
│   ├── edit_student.html   ← Edit student form
│   ├── tasks.html          ← View all tasks
│   ├── add_task.html       ← Add task form
│   └── edit_task.html      ← Edit task form
│
└── static/
    ├── css/
    │   └── style.css       ← All styles (responsive, animations, layout)
    └── js/
        └── main.js         ← Form validation + navbar toggle
```

---

## ⚙️ HOW TO RUN THE PROJECT

### Step 1: Install Python
Make sure Python 3.8+ is installed. Check with:
```
python --version
```

### Step 2: Install Flask
Open terminal/command prompt in the project folder and run:
```
pip install flask
```
Or use the requirements file:
```
pip install -r requirements.txt
```

### Step 3: Run the App
```
python app.py
```

### Step 4: Open in Browser
Open: **http://127.0.0.1:5000**

---

## 🧪 TESTING INSTRUCTIONS

| Feature | How to Test | Expected Result |
|---|---|---|
| Home Page | Visit / | See hero section + feature cards |
| Register | Go to /register, fill form | Account created, redirect to login |
| Login | Go to /login, enter credentials | Redirect to dashboard |
| Wrong Login | Enter wrong password | Error flash message shown |
| Add Student | Dashboard → Add Student | Record saved to database |
| View Students | Dashboard → Manage Students | Table with all records |
| Edit Student | Click Edit button | Form pre-filled, update works |
| Delete Student | Click Delete button | Confirmation popup, then deleted |
| Add Task | Dashboard → Add Task | Task saved with status |
| Logout | Click Logout | Session cleared, redirect home |
| Form Validation | Submit empty forms | Red error messages appear |

---

## 🗄️ DATABASE TABLES

**users** - Stores registered user accounts
- id, name, email, password, created_at

**students** - CRUD demo table for student records
- id, name, email, course, marks

**tasks** - Personal task manager per user
- id, title, description, status, user_id, created_at

---

## 🌐 URL ROUTES

| URL | Method | Description |
|---|---|---|
| / | GET | Home page |
| /register | GET/POST | Registration page |
| /login | GET/POST | Login page |
| /logout | GET | Logout, clear session |
| /dashboard | GET | Dashboard (login required) |
| /contact | GET/POST | Contact page |
| /students | GET | View all students |
| /students/add | GET/POST | Add student |
| /students/edit/<id> | GET/POST | Edit student |
| /students/delete/<id> | GET | Delete student |
| /tasks | GET | View all tasks |
| /tasks/add | GET/POST | Add task |
| /tasks/edit/<id> | GET/POST | Edit task |
| /tasks/delete/<id> | GET | Delete task |

---

## ✅ FEATURES CHECKLIST

- [x] Home Page with hero section
- [x] Registration page with JS validation
- [x] Login page with JS validation
- [x] Contact page with form
- [x] Responsive CSS (works on mobile!)
- [x] Navbar with hamburger menu
- [x] Flask backend with routing
- [x] SQLite database with 3 tables
- [x] User authentication (register/login/logout)
- [x] Session management
- [x] Flash messages
- [x] Full CRUD for Students
- [x] Full CRUD for Tasks
- [x] Protected routes (login required)
- [x] Beginner-friendly commented code
