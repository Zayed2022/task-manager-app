const API = "http://backend:8000";

async function loadTasks() {
    let res = await fetch(`${API}/tasks`);
    let tasks = await res.json();
    let list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(t => {
        list.innerHTML += `
            <li>
                <input type="checkbox" ${t.completed ? "checked" : ""} onclick="toggleTask('${t.id}', '${t.title}', this.checked)">
                ${t.title}
                <button onclick="deleteTask('${t.id}')">Delete</button>
            </li>
        `;
    });
}

async function addTask() {
    let title = document.getElementById("taskInput").value;
    await fetch(`${API}/tasks`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title})
    });
    loadTasks();
}

async function toggleTask(id, title, completed) {
    await fetch(`${API}/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, completed})
    });
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}

loadTasks();
