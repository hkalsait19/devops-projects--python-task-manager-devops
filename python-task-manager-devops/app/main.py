from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    tasks = [
        {
            "id": 1,
            "title": "Learn Docker",
            "completed": False
        },
        {
            "id": 2,
            "title": "Learn Kubernetes",
            "completed": False
        }
    ]

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "application": "Python Task Manager",
            "version": "1.0.0",
            "message": "Welcome to the Task Manager API"
        })

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy"
        }), 200

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        return jsonify(tasks), 200

    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        task = next(
            (task for task in tasks if task["id"] == task_id),
            None
        )

        if task is None:
            return jsonify({
                "error": "Task not found"
            }), 404

        return jsonify(task), 200

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json()

        if not data or "title" not in data:
            return jsonify({
                "error": "Task title is required"
            }), 400

        task = {
            "id": max(
                [task["id"] for task in tasks],
                default=0
            ) + 1,
            "title": data["title"],
            "completed": data.get("completed", False)
        }

        tasks.append(task)

        return jsonify(task), 201

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        task = next(
            (task for task in tasks if task["id"] == task_id),
            None
        )

        if task is None:
            return jsonify({
                "error": "Task not found"
            }), 404

        data = request.get_json()

        if "title" in data:
            task["title"] = data["title"]

        if "completed" in data:
            task["completed"] = data["completed"]

        return jsonify(task), 200

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        task = next(
            (task for task in tasks if task["id"] == task_id),
            None
        )

        if task is None:
            return jsonify({
                "error": "Task not found"
            }), 404

        tasks.remove(task)

        return jsonify({
            "message": "Task deleted successfully"
        }), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5151, debug=True)