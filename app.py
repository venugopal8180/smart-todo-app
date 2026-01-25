from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# ---------- Database Connection ----------
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Create Table ----------
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT,
            task_time TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- Home Route ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- Get All Tasks ----------
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    task_list = []
    for task in tasks:
        task_list.append({
            "id": task["id"],
            "title": task["title"],
            "priority": task["priority"],
            "completed": task["completed"],
            "task_time":task["task_time"]
        })

    return jsonify(task_list)

# ---------- Add New Task ----------
@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    priority = data.get('priority')
    task_time = data.get('task_time') 

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, priority, task_time) VALUES (?, ?, ?)",
        (title, priority, task_time)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added successfully!"})

# ---------- Mark Task Completed ----------
@app.route('/complete/<int:id>', methods=['PUT'])
def complete_task(id):
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task marked as completed!"})

# ---------- Delete Task ----------
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted successfully!"})

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5000) 
