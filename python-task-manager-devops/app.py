import os
import time
import psycopg2
from psycopg2 import OperationalError
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "task_manager_db")
DB_USER = os.getenv("POSTGRES_USER", "task_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "task_dev_password")
APP_ENV = os.getenv("APP_ENV", "development")


def get_connection():
    """Establish a connection to the database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def initialize_database():
    """Initialize the database by creating the tasks table if it doesn't exist."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE
                )
                """
            )
            connection.commit()


@app.route("/")
def home():
    """Home route to verify the API is running."""
    return jsonify({
        "message": "Task Manager API is running",
        "environment": os.getenv("APP_ENV", "development"),
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Retrieve all tasks."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, completed FROM tasks ORDER BY id"
            )
            rows = cursor.fetchall()

    tasks = [
        {
            "id": row[0],
            "title": row[1],
            "completed": row[2],
        }
        for row in rows
    ]

    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title)
                VALUES (%s)
                RETURNING id, title, completed
                """,
                (data["title"],),
            )

            row = cursor.fetchone()

    return jsonify({
        "id": row[0],
        "title": row[1],
        "completed": row[2],
    }), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by its ID."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,),
            )

            deleted = cursor.fetchone()

    if deleted is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    # Retry logic to wait for the database to be ready
    while True:
        try:
            initialize_database()
            print("Database initialized successfully")
            break
        except OperationalError:
            print("Database not ready. Retrying...")
            time.sleep(2)

    # Start the Flask application
    app.run(host="0.0.0.0", port=5151)