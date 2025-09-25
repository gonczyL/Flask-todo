from flask import Flask, jsonify, request, abort

def create_app():
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # simple in-memory store
    store = {"seq": 0, "todos": {}}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/todos")
    def list_todos():
        return jsonify(list(store["todos"].values()))

    @app.post("/todos")
    def create_todo():
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        if not title:
            abort(400, description="title required")
        store["seq"] += 1
        todo = {"id": store["seq"], "title": title, "done": False}
        store["todos"][todo["id"]] = todo
        return todo, 201

    @app.get("/todos/<int:todo_id>")
    def get_todo(todo_id):
        todo = store["todos"].get(todo_id)
        if not todo:
            abort(404)
        return todo

    @app.patch("/todos/<int:todo_id>")
    def update_todo(todo_id):
        todo = store["todos"].get(todo_id)
        if not todo:
            abort(404)
        data = request.get_json(silent=True) or {}
        if "title" in data:
            todo["title"] = data["title"]
        if "done" in data:
            todo["done"] = bool(data["done"])
        return todo

    @app.delete("/todos/<int:todo_id>")
    def delete_todo(todo_id):
        if todo_id not in store["todos"]:
            abort(404)
        del store["todos"][todo_id]
        return "", 204

    return app
