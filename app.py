from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for login sessions

# ---------- Login Manager ----------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------- Database Connection ----------
def get_db_connection():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- User Model ----------
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if user:
        return User(user["id"], user["username"], user["password"])
    return None

# ---------- Create Tables ----------
def create_tables():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT,
            task_time TEXT,
            completed INTEGER DEFAULT 0,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()

create_tables()

# ---------- Routes ----------

@app.route("/")
@login_required
def home():
    return render_template("index.html")

# ---------- Signup ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        username = data["username"]
        password = generate_password_hash(data["password"])

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except:
            return "Username already exists"
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            login_user(User(user["id"], user["username"], user["password"]))
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")

# ---------- Logout ----------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------- API: Get Tasks ----------
@app.route("/tasks")
@login_required
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ?", (current_user.id,)
    ).fetchall()
    conn.close()

    return jsonify([dict(task) for task in tasks])

# ---------- API: Add Task ----------
@app.route("/add", methods=["POST"])
@login_required
def add_task():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, priority, task_time, user_id) VALUES (?, ?, ?, ?)",
        (data["title"], data["priority"], data.get("task_time"), current_user.id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added"})

# ---------- API: Complete Task ----------
@app.route("/complete/<int:id>", methods=["PUT"])
@login_required
def complete_task(id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?",
        (id, current_user.id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Completed"})

# ---------- API: Delete Task ----------
@app.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_task(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (id, current_user.id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
