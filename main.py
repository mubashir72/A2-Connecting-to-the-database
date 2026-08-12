from fastapi import FastAPI, HTTPException 
from fastapi.responses import JSONResponse,Response
import sqlite3
from pydantic import BaseModel
app = FastAPI()

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", True),
                ("Test endpoints", False)
            ]
        )

    conn.commit()
    conn.close()


init_db()

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, done FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return [dict(task) for task in tasks]


@app.get("/tasks/{id}")
async def get_task(id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (id,)
    )

    task = cursor.fetchone()

    conn.close()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"error": f"Task {id} not found"}
        )

    return dict(task)

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):

    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, False)
    )

    new_id = cursor.lastrowid

    conn.commit()

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (new_id,)
    )

    new_task = cursor.fetchone()

    conn.close()

    return {
        "id": new_task[0],
        "title": new_task[1],
        "done": new_task[2]
    }