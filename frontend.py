 # This is the code written by sakshi
 
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


PORT = 8000

PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TeamTask — Project board</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #20232e;
      --muted: #85899a;
      --line: #ececf1;
      --purple: #6d5ce8;
      --canvas: #f7f7fa;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; color: var(--ink); background: var(--canvas); }
    button, input, select { font: inherit; }
    button { cursor: pointer; }
    .app { display: flex; min-height: 100vh; }
    .sidebar {
      width: 246px; flex: 0 0 246px; background: #fff; border-right: 1px solid var(--line);
      padding: 27px 17px; display: flex; flex-direction: column;
    }
    .brand { display: flex; align-items: center; gap: 11px; padding: 0 10px 36px; font-size: 19px; font-weight: 750; letter-spacing: -.6px; }
    .brand-mark { width: 30px; height: 30px; display: grid; place-items: center; border-radius: 10px; color: white; background: var(--purple); font-size: 17px; }
    .workspace { color: #777b8a; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; padding: 0 11px 12px; }
    .nav { display: grid; gap: 4px; }
    .nav-item { display: flex; gap: 12px; align-items: center; width: 100%; padding: 11px 12px; border: 0; border-radius: 8px; background: transparent; color: #656a7a; text-align: left; font-size: 14px; }
    .nav-item.active { color: var(--purple); background: #f0edff; font-weight: 650; }
    .nav-icon { width: 18px; text-align: center; font-size: 16px; }
    .nav-count { margin-left: auto; color: #9699a6; font-size: 12px; }
    .sidebar-bottom { margin-top: auto; }
    .upgrade { margin: 14px 4px 22px; padding: 15px; background: #f7f5ff; border: 1px solid #eeebff; border-radius: 11px; }
    .upgrade strong { display: block; margin-bottom: 5px; font-size: 13px; }
    .upgrade p { margin: 0 0 11px; color: #777b8a; font-size: 12px; line-height: 1.5; }
    .upgrade button { border: 0; border-radius: 6px; padding: 7px 10px; color: #fff; background: var(--purple); font-size: 12px; font-weight: 650; }
    .profile { display: flex; align-items: center; gap: 10px; border-top: 1px solid var(--line); padding: 18px 7px 0; }
    .avatar { width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; color: #5140ba; background: #e9e4ff; font-size: 12px; font-weight: 700; }
    .profile strong { display: block; font-size: 12px; }
    .profile small { color: var(--muted); font-size: 11px; }
    main { min-width: 0; flex: 1; }
    .topbar { height: 70px; padding: 0 38px; display: flex; align-items: center; justify-content: space-between; background: #fff; border-bottom: 1px solid var(--line); }
    .breadcrumb { color: #85899a; font-size: 13px; }
    .breadcrumb strong { color: var(--ink); font-weight: 650; }
    .top-actions { display: flex; align-items: center; gap: 12px; }
    .icon-button { width: 36px; height: 36px; border: 1px solid var(--line); border-radius: 9px; color: #696d7c; background: #fff; font-size: 17px; }
    .content { max-width: 1450px; margin: 0 auto; padding: 35px 38px 48px; }
    .heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; }
    h1 { margin: 0 0 7px; font-size: 27px; letter-spacing: -.8px; }
    .subtitle { margin: 0; color: var(--muted); font-size: 13px; }
    .primary { display: inline-flex; align-items: center; gap: 8px; border: 0; border-radius: 8px; padding: 11px 15px; color: #fff; background: var(--purple); box-shadow: 0 3px 8px #6d5ce833; font-size: 13px; font-weight: 650; }
    .primary:hover, .upgrade button:hover { background: #5948d1; }
    .toolbar { display: flex; align-items: center; justify-content: space-between; gap: 14px; margin: 29px 0 20px; }
    .view-tabs { display: flex; gap: 21px; height: 40px; }
    .view-tab { padding: 0 2px; border: 0; border-bottom: 2px solid transparent; color: #85899a; background: transparent; font-size: 13px; }
    .view-tab.active { border-bottom-color: var(--purple); color: var(--purple); font-weight: 650; }
    .tools { display: flex; gap: 9px; }
    .search { width: 205px; padding: 9px 11px; border: 1px solid #e8e8ee; border-radius: 8px; outline: none; background: #fff; font-size: 12px; }
    .search:focus, .field input:focus, .field select:focus { border-color: #9c91f4; box-shadow: 0 0 0 3px #6d5ce81a; }
    .filter { border: 1px solid #e8e8ee; border-radius: 8px; padding: 8px 11px; color: #656a7a; background: #fff; font-size: 12px; }
    .board { display: grid; grid-template-columns: repeat(4, minmax(210px, 1fr)); gap: 15px; align-items: start; overflow-x: auto; padding-bottom: 12px; }
    .column { min-height: 220px; padding: 13px; border: 1px solid #ededf2; border-radius: 11px; background: #f1f1f5; }
    .column-head { display: flex; align-items: center; gap: 8px; padding: 1px 2px 13px; }
    .column-head h2 { margin: 0; font-size: 12px; font-weight: 700; }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: #9497a4; }
    .column[data-status="In progress"] .dot { background: #f1a33c; }
    .column[data-status="In review"] .dot { background: #7e69e9; }
    .column[data-status="Done"] .dot { background: #48ae7a; }
    .column-count { color: #999daa; font-size: 11px; }
    .more { margin-left: auto; border: 0; color: #8c909d; background: transparent; letter-spacing: 2px; }
    .cards { display: grid; gap: 10px; }
    .task { padding: 13px; border: 1px solid #ececf1; border-radius: 9px; background: #fff; box-shadow: 0 1px 2px #20232e08; }
    .task-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
    .tag { display: inline-block; border-radius: 5px; padding: 4px 7px; color: #6254c9; background: #f0edff; font-size: 10px; font-weight: 650; }
    .tag.design { color: #bc7040; background: #fff1e7; }
    .tag.research { color: #327b72; background: #e6f5f1; }
    .task-menu { border: 0; padding: 0; color: #9b9eaa; background: transparent; letter-spacing: 1px; }
    .task h3 { margin: 10px 0 6px; font-size: 13px; line-height: 1.45; font-weight: 650; }
    .task p { margin: 0; color: #85899a; font-size: 11px; line-height: 1.5; }
    .task-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 14px; padding-top: 11px; border-top: 1px solid #f0f0f3; }
    .assignee { display: flex; align-items: center; gap: 6px; color: #777b8a; font-size: 10px; }
    .mini-avatar { width: 22px; height: 22px; display: grid; place-items: center; border-radius: 50%; color: #5447a8; background: #e9e4ff; font-size: 9px; font-weight: 700; }
    .due { color: #85899a; font-size: 10px; }
    .due.late { color: #d35d5d; }
    .empty { padding: 18px 8px; color: #9699a6; text-align: center; font-size: 11px; }
    .modal-backdrop { position: fixed; inset: 0; z-index: 2; display: none; place-items: center; padding: 20px; background: #20232e66; }
    .modal-backdrop.open { display: grid; }
    .modal { width: min(440px, 100%); padding: 23px; border-radius: 13px; background: #fff; box-shadow: 0 16px 60px #17182733; }
    .modal h2 { margin: 0 0 19px; font-size: 18px; }
    .field { display: grid; gap: 7px; margin-bottom: 14px; }
    .field label { color: #656a7a; font-size: 12px; font-weight: 600; }
    .field input, .field select { width: 100%; border: 1px solid #e8e8ee; border-radius: 7px; padding: 10px; outline: none; background: #fff; font-size: 13px; }
    .modal-actions { display: flex; justify-content: flex-end; gap: 9px; margin-top: 20px; }
    .secondary { border: 1px solid var(--line); border-radius: 7px; padding: 9px 13px; color: #656a7a; background: #fff; font-size: 12px; }
    @media (max-width: 900px) {
      .sidebar { width: 205px; flex-basis: 205px; }
      .content { padding-right: 24px; padding-left: 24px; }
      .topbar { padding-right: 24px; padding-left: 24px; }
      .board { grid-template-columns: repeat(4, minmax(225px, 1fr)); }
    }
    @media (max-width: 650px) {
      .app { display: block; }
      .sidebar { width: auto; height: auto; padding: 13px 15px; border-right: 0; border-bottom: 1px solid var(--line); }
      .brand { padding: 0 5px; }
      .workspace, .nav, .sidebar-bottom { display: none; }
      .topbar { height: 55px; padding: 0 17px; }
      .content { padding: 25px 17px; }
      .heading { align-items: center; }
      h1 { font-size: 23px; }
      .heading .primary { padding: 10px; font-size: 0; }
      .heading .primary span { font-size: 18px; }
      .toolbar { align-items: flex-start; flex-direction: column; margin-top: 23px; }
      .tools { width: 100%; }
      .search { flex: 1; width: auto; }
      .board { grid-template-columns: repeat(4, minmax(240px, 1fr)); margin-right: -17px; }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <div class="brand"><span class="brand-mark">✓</span> teamtask</div>
      <div class="workspace">Workspace</div>
      <nav class="nav" aria-label="Main navigation">
        <button class="nav-item"><span class="nav-icon">⌂</span> Home</button>
        <button class="nav-item active"><span class="nav-icon">▦</span> My projects <span class="nav-count">4</span></button>
        <button class="nav-item"><span class="nav-icon">◷</span> My tasks <span class="nav-count">8</span></button>
        <button class="nav-item"><span class="nav-icon">◉</span> Inbox <span class="nav-count">2</span></button>
      </nav>
      <div class="sidebar-bottom">
        <section class="upgrade"><strong>Make teamwork flow</strong><p>Bring your team together and get more done.</p><button type="button">Explore plans</button></section>
        <div class="profile"><div class="avatar">SM</div><div><strong>Sakshi Shirkar</strong><small>Free plan</small></div></div>
      </div>
    </aside>
    <main>
      <header class="topbar"><div class="breadcrumb">Projects&nbsp; / &nbsp;<strong>Website redesign</strong></div><div class="top-actions"><button class="icon-button" aria-label="Notifications">♧</button><div class="avatar">SM</div></div></header>
      <section class="content">
        <div class="heading"><div><h1>Website redesign</h1><p class="subtitle">Plan, organize, and track your team's work.</p></div><button class="primary" id="open-modal"><span>＋</span> Add task</button></div>
        <div class="toolbar">
          <div class="view-tabs" role="tablist" aria-label="Board views"><button class="view-tab active" role="tab">Board</button><button class="view-tab" role="tab">Timeline</button><button class="view-tab" role="tab">Files</button></div>
          <div class="tools"><input class="search" id="search" type="search" placeholder="⌕  Search tasks..." aria-label="Search tasks"><select class="filter" id="assignee-filter" aria-label="Filter by assignee"><option value="">All assignees</option><option>Sakshi</option><option>Alex</option><option>Jordan</option><option>Mia</option></select></div>
        </div>
        <div class="board" id="board" aria-label="Task board"></div>
      </section>
    </main>
  </div>
  <div class="modal-backdrop" id="modal-backdrop" role="presentation">
    <form class="modal" id="task-form" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <h2 id="modal-title">Add a task</h2>
      <div class="field"><label for="task-title">Task name</label><input id="task-title" name="title" required maxlength="100" placeholder="What needs to be done?"></div>
      <div class="field"><label for="task-description">Description</label><input id="task-description" name="description" maxlength="160" placeholder="Add a little more detail (optional)"></div>
      <div class="field"><label for="task-assignee">Assignee</label><select id="task-assignee" name="assignee"><option>Sakshi</option><option>Alex</option><option>Jordan</option><option>Mia</option></select></div>
      <div class="field"><label for="task-status">Status</label><select id="task-status" name="status"><option>To do</option><option>In progress</option><option>In review</option><option>Done</option></select></div>
      <div class="modal-actions"><button class="secondary" type="button" id="cancel-modal">Cancel</button><button class="primary" type="submit">Create task</button></div>
    </form>
  </div>
  <script>
    const statuses = ["To do", "In progress", "In review", "Done"];
    let tasks = [
      { title: "Map out user journey", description: "Document key paths for the new onboarding experience.", category: "Research", assignee: "Alex", status: "To do", due: "Nov 25" },
      { title: "Audit current website", description: "Review existing pages and note areas to improve.", category: "Research", assignee: "Sakshi", status: "To do", due: "Nov 27" },
      { title: "Create moodboard", description: "Gather visual inspiration for the new direction.", category: "Design", assignee: "Mia", status: "To do", due: "Nov 28" },
      { title: "Design homepage wireframes", description: "Explore a few layout options for the landing page.", category: "Design", assignee: "Mia", status: "In progress", due: "Nov 24" },
      { title: "Set up design system", description: "Define core colors, typography, and components.", category: "Design", assignee: "Sakshi", status: "In progress", due: "Nov 26" },
      { title: "Gather stakeholder feedback", description: "Share the first concepts and collect feedback.", category: "Planning", assignee: "Jordan", status: "In progress", due: "Nov 29" },
      { title: "Review mobile layouts", description: "Check responsive states across key screens.", category: "Design", assignee: "Alex", status: "In review", due: "Nov 23" },
      { title: "Define project scope", description: "Align on launch goals and project milestones.", category: "Planning", assignee: "Jordan", status: "Done", due: "Nov 20" }
    ];
    const initials = name => name.split(" ").map(part => part[0]).join("").slice(0, 2).toUpperCase();
    const escapeHtml = text => String(text).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
    function renderBoard() {
      const query = document.getElementById("search").value.trim().toLowerCase();
      const assignee = document.getElementById("assignee-filter").value;
      document.getElementById("board").innerHTML = statuses.map(status => {
        const matching = tasks.filter(task => task.status === status &&
          (!assignee || task.assignee === assignee) &&
          (!query || `${task.title} ${task.description} ${task.category} ${task.assignee}`.toLowerCase().includes(query)));
        const cards = matching.map(task => `<article class="task">
          <div class="task-top"><span class="tag ${task.category.toLowerCase()}">${escapeHtml(task.category)}</span><button class="task-menu" aria-label="More options">···</button></div>
          <h3>${escapeHtml(task.title)}</h3><p>${escapeHtml(task.description || "No description")}</p>
          <div class="task-foot"><span class="assignee"><span class="mini-avatar">${escapeHtml(initials(task.assignee))}</span>${escapeHtml(task.assignee)}</span><span class="due">${escapeHtml(task.due || "No due date")}</span></div>
        </article>`).join("");
        return `<section class="column" data-status="${status}"><div class="column-head"><span class="dot"></span><h2>${status}</h2><span class="column-count">${matching.length}</span><button class="more" aria-label="Column options">···</button></div><div class="cards">${cards || '<div class="empty">No tasks here yet</div>'}</div></section>`;
      }).join("");
    }
    const backdrop = document.getElementById("modal-backdrop");
    const form = document.getElementById("task-form");
    function closeModal() { backdrop.classList.remove("open"); }
    document.getElementById("open-modal").addEventListener("click", () => {
      backdrop.classList.add("open");
      document.getElementById("task-title").focus();
    });
    document.getElementById("cancel-modal").addEventListener("click", closeModal);
    backdrop.addEventListener("click", event => { if (event.target === backdrop) closeModal(); });
    document.addEventListener("keydown", event => { if (event.key === "Escape") closeModal(); });
    form.addEventListener("submit", event => {
      event.preventDefault();
      const data = new FormData(form);
      tasks.unshift({
        title: data.get("title").trim(),
        description: data.get("description").trim(),
        category: "Planning",
        assignee: data.get("assignee"),
        status: data.get("status"),
        due: ""
      });
      form.reset();
      closeModal();
      renderBoard();
    });
    document.getElementById("search").addEventListener("input", renderBoard);
    document.getElementById("assignee-filter").addEventListener("change", renderBoard);
    renderBoard();
  </script>
</body>
</html>"""


class FrontendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path not in ("/", "/index.html"):
            self.send_error(404)
            return
        page = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def log_message(self, format_string, *args):
        print("%s - %s" % (self.address_string(), format_string % args))


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), FrontendHandler)
    print("TeamTask is running at http://127.0.0.1:%s" % PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down TeamTask.")
        server.server_close()
