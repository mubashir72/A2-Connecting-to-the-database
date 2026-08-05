from fastapi import FastAPI, HTTPException 
from fastapi.responses import JSONResponse,Response
import sqlite3
from pydantic import BaseModel
app = FastAPI()

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)
    # Check if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    # Insert example tasks only once
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


# Initialize database when application starts
init_db()

@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

# @app.get("/tasks")
# async def get_tasks ():
#     return tasks

# @app.get("/tasks/{id}")
# async def get_task(id: int):
#     for task in tasks:
#         if task["id"] == id:
#             return task

#     raise HTTPException(
#         status_code=404,
#         detail={"error": f"Task {id} not found"}
#     )



# class TaskCreate(BaseModel):
#     title: str

# class TaskUpdate(BaseModel):
#     title: str
#     done: bool



# @app.post("/tasks", status_code=201)
# async def create_task(task: TaskCreate):
#     if not task.title.strip():
#         return JSONResponse(
#             status_code=400,
#             content={"error": "Title is required and cannot be empty"}
#         )
    
#     next_id = max(t["id"] for t in tasks) + 1 if tasks else 1
#     new_task = {
#         "id": next_id,
#         "title": task.title,
#         "done": False
#     }

#     tasks.append(new_task)

#     return new_task



# @app.put("/tasks/{id}")
# async def update_task(id: int, updated: TaskUpdate):
#     if not updated.title.strip():
#         return JSONResponse(
#             status_code=400,
#             content={"error": "Title must not be empty"}
#         )

#     for task in tasks:
#         if task["id"] == id:
#             task["title"] = updated.title
#             task["done"] = updated.done
#             return task

#     return JSONResponse(
#         status_code=404,
#         content={"error": f"Task {id} not found"}
#     )


# @app.delete("/tasks/{id}", status_code=204)
# async def delete_task(id: int):
#     for index, task in enumerate(tasks):
#         if task["id"] == id:
#             tasks.pop(index)
#             return Response(status_code=204)

#     return JSONResponse(
#         status_code=404,
#         content={"error": f"Task {id} not found"}
#     )