const taskList = document.getElementById("taskList");
const addTaskBtn = document.getElementById("addTaskBtn");

const totalTasksEl = document.getElementById("totalTasks");
const completedTasksEl = document.getElementById("completedTasks");
const pendingTasksEl = document.getElementById("pendingTasks");
const aiMessageEl = document.getElementById("aiMessage");

const now = new Date();
const currentMinutes = now.getHours() * 60 + now.getMinutes();

let overdueCount = 0;
let upcomingCount = 0;

// ---------------- Fetch and Display Tasks ----------------
async function loadTasks() {
  const response = await fetch("/tasks");
  const tasks = await response.json();

  // Clear old list
  taskList.innerHTML = "";

  let completedCount = 0;
  let highPriorityPending = 0;

  tasks.forEach((task) => {
    const li = document.createElement("li");

    // Task text
    li.innerHTML = `
      <span class="${task.completed ? "completed" : ""}">
       ${task.title} (${task.priority}) ⏰ ${task.task_time || "Anytime"}
      </span>
    `;

    // Buttons container
    const actionsDiv = document.createElement("div");
    actionsDiv.className = "task-actions";

    // Complete button
    if (!task.completed) {
      const completeBtn = document.createElement("button");
      completeBtn.textContent = "Complete";
      completeBtn.onclick = () => completeTask(task.id);
      actionsDiv.appendChild(completeBtn);
    } else {
      completedCount++;
    }

    // Delete button
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = () => deleteTask(task.id);
    actionsDiv.appendChild(deleteBtn);

    li.appendChild(actionsDiv);

    // ✅ MOST IMPORTANT LINE (renders task)
    taskList.appendChild(li);

    // AI logic
    if (task.priority === "High" && task.completed === 0) {
      highPriorityPending++;
    }

    if (task.task_time && task.completed === 0) {
      const [h, m] = task.task_time.split(":").map(Number);
      const taskMinutes = h * 60 + m;

      if (taskMinutes < currentMinutes) {
        overdueCount++;
      } else if (taskMinutes - currentMinutes <= 60) {
        upcomingCount++;
      }
    }
  });

  // ---------------- Update Summary ----------------
  totalTasksEl.textContent = tasks.length;
  completedTasksEl.textContent = completedCount;
  pendingTasksEl.textContent = tasks.length - completedCount;

  // ---------------- AI Suggestions ----------------
  if (tasks.length === 0) {
    aiMessageEl.textContent = "Add tasks to get started 🚀";
  } else if (overdueCount > 0) {
    aiMessageEl.textContent = "You have overdue tasks ⏰ Please take action";
  } else if (upcomingCount > 0) {
    aiMessageEl.textContent = "You have tasks scheduled soon 🔔 Stay ready";
  } else if (currentMinutes < 720) {
    aiMessageEl.textContent = "Good morning! Start with your planned tasks ☀️";
  } else if (currentMinutes >= 1080) {
    aiMessageEl.textContent =
      "Try to complete pending tasks before day ends 🌙";
  } else if (completedCount / tasks.length >= 0.7) {
    aiMessageEl.textContent = "Great time management today! 🎉";
  } else {
    aiMessageEl.textContent = "Keep going, you are making steady progress 👍";
  }
}

// ---------------- Add Task ----------------
addTaskBtn.addEventListener("click", async () => {
  const title = document.getElementById("taskTitle").value;
  const taskTime = document.getElementById("taskTime").value;
  const priority = document.getElementById("taskPriority").value;

  if (title.trim() === "") {
    alert("Task title cannot be empty");
    return;
  }

  await fetch("/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title, priority, task_time: taskTime }),
  });

  document.getElementById("taskTitle").value = "";
  loadTasks();
});

// ---------------- Complete Task ----------------
async function completeTask(id) {
  await fetch(`/complete/${id}`, {
    method: "PUT",
  });
  loadTasks();
}

// ---------------- Delete Task ----------------
async function deleteTask(id) {
  await fetch(`/delete/${id}`, {
    method: "DELETE",
  });
  loadTasks();
}

// ---------------- Initial Load ----------------
loadTasks();
