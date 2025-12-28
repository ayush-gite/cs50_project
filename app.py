import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database connection
db = SQL("sqlite:///tasks.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Dashboard: Show tasks sorted by completion status and due date"""
    tasks = db.execute("""
        SELECT * FROM tasks
        WHERE user_id = ?
        ORDER BY CASE WHEN status = 'pending' THEN 1 ELSE 2 END, due_date ASC
    """, session["user_id"])
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
@login_required
def add():
    """Handle professional task creation"""
    task_name = request.form.get("task")
    priority = request.form.get("priority")
    due_date = request.form.get("due_date")

    if task_name and due_date:
        db.execute("INSERT INTO tasks (user_id, task_name, priority, due_date) VALUES (?, ?, ?, ?)",
                   session["user_id"], task_name, priority, due_date)
    return redirect("/")

@app.route("/toggle/<int:task_id>")
@login_required
def toggle(task_id):
    """Mark task as complete or pending"""
    task = db.execute("SELECT status FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
    if task:
        new_status = "completed" if task[0]["status"] == "pending" else "pending"
        db.execute("UPDATE tasks SET status = ? WHERE id = ?", new_status, task_id)
    return redirect("/")

@app.route("/delete/<int:task_id>")
@login_required
def delete(task_id):
    """Remove task safely"""
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
    return redirect("/")

@app.route("/clear_completed", methods=["POST"])
@login_required
def clear_completed():
    """Bulk delete completed tasks"""
    db.execute("DELETE FROM tasks WHERE user_id = ? AND status = 'completed'", session["user_id"])
    return redirect("/")

# --- Professional Auth Routes ---

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", error="Invalid username or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", error="All fields are required")

        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
            return redirect("/login")
        except:
            return render_template("register.html", error="Username already taken")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
