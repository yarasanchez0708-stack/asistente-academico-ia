// ── CONFIG ──────────────────────────────────────────────
const API = "http://localhost:8000";
let currentFilter = "all";

// ── API CALLS ───────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

async function fetchTasks() {
  const params = currentFilter === "pending"   ? "?completed=false"
               : currentFilter === "completed" ? "?completed=true"
               : "";
  return apiFetch("/tasks" + params);
}

async function createTask() {
  const title       = document.getElementById("f-title").value.trim();
  const subject     = document.getElementById("f-subject").value.trim();
  const due_date    = document.getElementById("f-due").value;
  const priority    = document.getElementById("f-priority").value;
  const description = document.getElementById("f-desc").value.trim();

  if (!title || !subject || !due_date) {
    showToast("Please fill in title, subject and due date.", "error");
    return;
  }

  try {
    await apiFetch("/tasks", {
      method: "POST",
      body: JSON.stringify({ title, subject, due_date, priority, description }),
    });
    showToast("Task created ✓", "success");
    clearForm();
    await refresh();
  } catch (e) {
    showToast(e.message, "error");
  }
}

async function completeTask(id) {
  try {
    await apiFetch(`/tasks/${id}/complete`, { method: "PATCH" });
    showToast("Marked as complete ✓", "success");
    await refresh();
  } catch (e) {
    showToast(e.message, "error");
  }
}

async function deleteTask(id) {
  try {
    await apiFetch(`/tasks/${id}`, { method: "DELETE" });
    showToast("Task deleted", "success");
    await refresh();
  } catch (e) {
    showToast(e.message, "error");
  }
}

async function fetchStats() {
  const data = await apiFetch("/tasks/stats/summary");
  document.getElementById("stat-total").textContent     = data.total;
  document.getElementById("stat-pending").textContent   = data.pending;
  document.getElementById("stat-completed").textContent = data.completed;
}

// ── RENDER ──────────────────────────────────────────────
function renderTasks(tasks) {
  const list = document.getElementById("task-list");
  if (!tasks.length) {
    list.innerHTML = `<div class="empty-state"><div class="empty-icon">✅</div>No tasks here.</div>`;
    return;
  }

  list.innerHTML = tasks.map(t => `
    <div class="task-card ${t.completed ? "completed" : ""}">
      <div>
        <div class="task-title">${escHtml(t.title)}</div>
        <div class="task-meta">
          <span class="tag">${escHtml(t.subject)}</span>
          <span class="tag ${t.priority}">${t.priority}</span>
          <span class="tag">📅 ${t.due_date}</span>
          ${t.description ? `<span class="tag" title="${escHtml(t.description)}">📝</span>` : ""}
        </div>
      </div>
      <div class="task-actions">
        ${!t.completed
          ? `<button class="icon-btn complete" title="Mark complete" onclick="completeTask('${t.id}')">✓</button>`
          : ""}
        <button class="icon-btn delete" title="Delete" onclick="deleteTask('${t.id}')">✕</button>
      </div>
    </div>
  `).join("");
}

// ── HELPERS ─────────────────────────────────────────────
async function refresh() {
  try {
    const [tasks] = await Promise.all([fetchTasks(), fetchStats()]);
    renderTasks(tasks);
  } catch (e) {
    renderTasks([]);
  }
}

function setFilter(filter, btn) {
  currentFilter = filter;
  document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  refresh();
}

function clearForm() {
  ["f-title", "f-subject", "f-due", "f-desc"].forEach(id => document.getElementById(id).value = "");
  document.getElementById("f-priority").value = "medium";
}

function escHtml(str) {
  return String(str).replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

let toastTimer;
function showToast(msg, type = "success") {
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();
  clearTimeout(toastTimer);
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  document.body.appendChild(el);
  toastTimer = setTimeout(() => { el.style.opacity = "0"; setTimeout(() => el.remove(), 300); }, 3000);
}

// ── INIT ────────────────────────────────────────────────
async function init() {
  const pill = document.getElementById("status-pill");
  const txt  = document.getElementById("status-text");
  try {
    const data = await apiFetch("/");
    txt.textContent = `API v${data.version}`;
    pill.classList.add("connected");
    await refresh();
  } catch {
    txt.textContent = "backend offline";
    document.getElementById("task-list").innerHTML =
      `<div class="empty-state"><div class="empty-icon">⚠️</div>Cannot reach the API.<br/>Make sure the backend is running on <code>localhost:8000</code></div>`;
  }
}

init();
