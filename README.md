# smart-todo-app
# 📝 Smart To-Do & Productivity Tracker

A full-stack web application to manage daily tasks with smart AI-based productivity suggestions, priority scheduling, and per-user authentication.

---

## Features

- **User Authentication** — Secure signup, login, and logout using hashed passwords
- **Task Management** — Add, complete, and delete tasks with ease
- **Priority Levels** — Assign High, Medium, or Low priority to each task
- **Time Scheduling** — Set a time for each task to stay on track
- **Productivity Summary** — Live count of total, completed, and pending tasks
- **AI Suggestions** — Context-aware motivational tips based on time of day, overdue tasks, and progress
- **Dark Mode** — Toggle between light and dark themes, with preference saved in localStorage
- **Per-User Data** — Every user sees only their own tasks

---

## Project Structure

```
smart-todo-app/
├── app.py                  # Flask backend — routes, auth, API
├── requirements.txt        # Python dependencies
├── todo.db                 # SQLite database (auto-created on first run)
├── static/
│   ├── css/
│   │   └── style.css       # Global styles + dark mode + animations
│   ├── js/
│   │   ├── script.js       # Task CRUD logic + AI suggestion engine
│   │   └── theme.js        # Dark/light mode toggle
│   └── favicon_io/
│       └── favicon.ico
└── templates/
    ├── index.html          # Main dashboard
    ├── login.html          # Login page
    └── signup.html         # Signup page
```
---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Flask                     |
| Auth       | Flask-Login, Werkzeug (bcrypt)    |
| Database   | SQLite3                           |
| Frontend   | HTML, CSS, Vanilla JavaScript     |
| Deployment | Gunicorn                          |

---
## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-todo-app.git
cd smart-todo-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## Deployment (Gunicorn)

```bash
gunicorn app:app
```
> For production, also set a strong `SECRET_KEY` in `app.py` and consider using a `.env` file.
---

## Database Schema

### `users` table

| Column   | Type    | Description              |
|----------|---------|--------------------------|
| id       | INTEGER | Primary key              |
| username | TEXT    | Unique username          |
| password | TEXT    | Hashed password          |

### `tasks` table

| Column    | Type    | Description                     |
|-----------|---------|---------------------------------|
| id        | INTEGER | Primary key                     |
| title     | TEXT    | Task description                |
| priority  | TEXT    | High / Medium / Low             |
| task_time | TEXT    | Scheduled time (HH:MM)          |
| completed | INTEGER | 0 = pending, 1 = done           |
| user_id   | INTEGER | Foreign key → users.id          |

---

## AI Suggestion Logic

The suggestion engine in `script.js` generates tips based on:

- **No tasks** → Prompt to get started
- **Overdue tasks** → Urgent action reminder
- **Tasks due within 60 minutes** → Stay-ready alert
- **Morning (before 12 PM)** → Morning motivation
- **Evening (after 6 PM)** → End-of-day nudge
- **70%+ tasks completed** → Celebration message
- **Otherwise** → Steady progress encouragement
  
---

## Security Notes

- Passwords are hashed using Werkzeug's `generate_password_hash`
- Each user's tasks are isolated by `user_id` — no cross-user data access
- Session management is handled by Flask-Login
- Change the `app.secret_key` before deploying to production

---

## License

This project is open source and available under the [MIT License](LICENSE).
