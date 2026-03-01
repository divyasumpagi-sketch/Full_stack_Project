# ============================================================
# app.py - Main Backend File (Flask Application)
# ============================================================
# HOW TO RUN: Open terminal in project folder, type:
#   python app.py
# Then open browser and go to: http://127.0.0.1:5000
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

# Create the Flask app
app = Flask(__name__)

# Secret key for session management (keep this secret in real projects!)
app.secret_key = "divya_secret_key_2024"

# Database file path
DATABASE = "database.db"


# ============================================================
# DATABASE HELPER FUNCTIONS
# ============================================================

def get_db():
    """Connect to the SQLite database and return connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    # --- Users Table (for login/register) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            email    TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            created_at TEXT  DEFAULT (datetime('now'))
        )
    """)

    # --- Students Table (for CRUD demo) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT    NOT NULL,
            email   TEXT    NOT NULL,
            course  TEXT    NOT NULL,
            marks   INTEGER NOT NULL
        )
    """)

    # --- Tasks Table (for task manager demo) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT,
            status      TEXT    DEFAULT 'Pending',
            user_id     INTEGER,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


# ============================================================
# ROUTES - PUBLIC PAGES
# ============================================================

@app.route("/")
def home():
    """Home Page - Welcome message"""
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact Page - Show form and handle submission"""
    if request.method == "POST":
        name    = request.form.get("name")
        email   = request.form.get("email")
        message = request.form.get("message")
        # In a real project you'd save this or send an email
        flash(f"Thank you {name}! Your message has been received.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


# ============================================================
# AUTHENTICATION ROUTES
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration Page"""
    if request.method == "POST":
        name     = request.form.get("name").strip()
        email    = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirm  = request.form.get("confirm_password").strip()

        # Basic validation
        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))

        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))

        # Check if email already exists
        conn = get_db()
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()

        if existing:
            flash("Email already registered! Please login.", "error")
            conn.close()
            return redirect(url_for("register"))

        # Save new user (NOTE: In production, always hash passwords!)
        conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                     (name, email, password))
        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Page"""
    if request.method == "POST":
        email    = request.form.get("email").strip()
        password = request.form.get("password").strip()

        # Validate against database
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            # Save user info in session
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            flash(f"Welcome back, {user['name']}! 🎉", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout - Clear session"""
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("home"))


# ============================================================
# DASHBOARD (Protected Route)
# ============================================================

@app.route("/dashboard")
def dashboard():
    """Dashboard - Only accessible after login"""
    if "user_id" not in session:
        flash("Please login first!", "error")
        return redirect(url_for("login"))

    conn = get_db()
    # Count totals for dashboard cards
    student_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    task_count    = conn.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?",
                                  (session["user_id"],)).fetchone()[0]
    user_count    = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()

    return render_template("dashboard.html",
                           student_count=student_count,
                           task_count=task_count,
                           user_count=user_count)


# ============================================================
# STUDENTS CRUD MODULE
# ============================================================

@app.route("/students")
def students():
    """View all students"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    all_students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("students.html", students=all_students)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    """Add a new student record"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name   = request.form.get("name").strip()
        email  = request.form.get("email").strip()
        course = request.form.get("course").strip()
        marks  = request.form.get("marks")

        if not name or not email or not course or not marks:
            flash("All fields are required!", "error")
            return redirect(url_for("add_student"))

        conn = get_db()
        conn.execute("INSERT INTO students (name, email, course, marks) VALUES (?, ?, ?, ?)",
                     (name, email, course, int(marks)))
        conn.commit()
        conn.close()
        flash("Student added successfully! ✅", "success")
        return redirect(url_for("students"))

    return render_template("add_student.html")


@app.route("/students/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    """Edit a student record"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

    if not student:
        flash("Student not found!", "error")
        return redirect(url_for("students"))

    if request.method == "POST":
        name   = request.form.get("name").strip()
        email  = request.form.get("email").strip()
        course = request.form.get("course").strip()
        marks  = request.form.get("marks")

        conn.execute("UPDATE students SET name=?, email=?, course=?, marks=? WHERE id=?",
                     (name, email, course, int(marks), id))
        conn.commit()
        conn.close()
        flash("Student updated successfully! ✏️", "success")
        return redirect(url_for("students"))

    conn.close()
    return render_template("edit_student.html", student=student)


@app.route("/students/delete/<int:id>")
def delete_student(id):
    """Delete a student record"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Student deleted! 🗑️", "success")
    return redirect(url_for("students"))


# ============================================================
# CALCULATOR MODULE
# ============================================================

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    """Simple Arithmetic Calculator Page"""
    result     = None
    error      = None
    expression = None
    num1_val   = ""
    num2_val   = ""
    op_val     = ""

    if request.method == "POST":
        try:
            num1      = float(request.form.get("num1"))
            num2      = float(request.form.get("num2"))
            operation = request.form.get("operation")
            num1_val  = request.form.get("num1")
            num2_val  = request.form.get("num2")
            op_val    = operation
            symbol    = ""

            if operation == "add":
                result = num1 + num2
                symbol = "+"
            elif operation == "subtract":
                result = num1 - num2
                symbol = "−"
            elif operation == "multiply":
                result = num1 * num2
                symbol = "×"
            elif operation == "divide":
                if num2 == 0:
                    error = "Cannot divide by zero!"
                else:
                    result = num1 / num2
                    symbol = "÷"
            elif operation == "modulus":
                if num2 == 0:
                    error = "Cannot use modulus with zero!"
                else:
                    result = num1 % num2
                    symbol = "mod"
            elif operation == "power":
                result = num1 ** num2
                symbol = "^"
            else:
                error = "Please select a valid operation."

            if result is not None:
                # Show whole number if no decimal needed
                display = int(result) if result == int(result) else round(result, 6)
                expression = f"{num1} {symbol} {num2} = {display}"
                result = display

        except ValueError:
            error = "Please enter valid numbers."

    return render_template("calculator.html",
                           result=result,
                           expression=expression,
                           error=error,
                           num1_val=num1_val,
                           num2_val=num2_val,
                           op_val=op_val)


# ============================================================
# TASKS CRUD MODULE
# ============================================================

@app.route("/tasks")
def tasks():
    """View all tasks for logged-in user"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    all_tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("tasks.html", tasks=all_tasks)


@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    """Add a new task"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title       = request.form.get("title").strip()
        description = request.form.get("description").strip()
        status      = request.form.get("status", "Pending")

        if not title:
            flash("Task title is required!", "error")
            return redirect(url_for("add_task"))

        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)",
            (title, description, status, session["user_id"])
        )
        conn.commit()
        conn.close()
        flash("Task added! ✅", "success")
        return redirect(url_for("tasks"))

    return render_template("add_task.html")


@app.route("/tasks/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):
    """Edit a task"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    task = conn.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?",
                        (id, session["user_id"])).fetchone()

    if not task:
        flash("Task not found!", "error")
        return redirect(url_for("tasks"))

    if request.method == "POST":
        title       = request.form.get("title").strip()
        description = request.form.get("description").strip()
        status      = request.form.get("status", "Pending")

        conn.execute("UPDATE tasks SET title=?, description=?, status=? WHERE id=?",
                     (title, description, status, id))
        conn.commit()
        conn.close()
        flash("Task updated! ✏️", "success")
        return redirect(url_for("tasks"))

    conn.close()
    return render_template("edit_task.html", task=task)


@app.route("/tasks/delete/<int:id>")
def delete_task(id):
    """Delete a task"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?",
                 (id, session["user_id"]))
    conn.commit()
    conn.close()
    flash("Task deleted! 🗑️", "success")
    return redirect(url_for("tasks"))


# ============================================================
# RUN THE APP
# ============================================================
if __name__ == "__main__":
    # Initialize database tables when app starts
    init_db()
    print("🚀 Server is running at http://127.0.0.1:5000")
    # debug=True means auto-reload on code changes (use only during development)
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=10000)