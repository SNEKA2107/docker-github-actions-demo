from flask import Flask, request, redirect, url_for, jsonify, render_template_string

app = Flask(__name__)

# Simple in-memory store for the To-Do items.
todos = []
_next_id = 1

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Flask To-Do</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 480px; margin: 40px auto; }
    h1 { text-align: center; }
    form.add { display: flex; gap: 8px; }
    input[type=text] { flex: 1; padding: 8px; }
    button { padding: 8px 12px; cursor: pointer; }
    ul { list-style: none; padding: 0; }
    li { display: flex; align-items: center; justify-content: space-between;
         padding: 8px; border-bottom: 1px solid #ddd; }
    .done { text-decoration: line-through; color: #999; }
  </style>
</head>
<body>
  <h1>📝 To-Do List</h1>
  <form class="add" method="post" action="/add">
    <input type="text" name="title" placeholder="What needs doing?" required>
    <button type="submit">Add</button>
  </form>
  <ul>
    {% for t in todos %}
    <li>
      <span class="{{ 'done' if t.done else '' }}">{{ t.title }}</span>
      <span>
        <a href="{{ url_for('toggle', todo_id=t.id) }}">{{ '↩' if t.done else '✓' }}</a>
        <a href="{{ url_for('delete', todo_id=t.id) }}">🗑</a>
      </span>
    </li>
    {% else %}
    <li>No tasks yet — add one above!</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE, todos=todos)


@app.route("/add", methods=["POST"])
def add():
    global _next_id
    title = (request.form.get("title") or "").strip()
    if title:
        todos.append({"id": _next_id, "title": title, "done": False})
        _next_id += 1
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>")
def toggle(todo_id):
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            break
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return jsonify(status="ok")


# JSON API (handy for automated testing).
@app.route("/api/todos", methods=["GET", "POST"])
def api_todos():
    global _next_id
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify(error="title is required"), 400
        todo = {"id": _next_id, "title": title, "done": False}
        todos.append(todo)
        _next_id += 1
        return jsonify(todo), 201
    return jsonify(todos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
