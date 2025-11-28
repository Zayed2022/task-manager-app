from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
import pymongo

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["taskdb"]
tasks_collection = db["tasks"]

class Task(BaseModel):
    title: str
    completed: bool = False

@app.get("/tasks")
def get_tasks():
    tasks = []
    for task in tasks_collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "completed": task["completed"]
        })
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    new_task = {"title": task.title, "completed": task.completed}
    result = tasks_collection.insert_one(new_task)
    return {"id": str(result.inserted_id), **new_task}

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Task):
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"title": task.title, "completed": task.completed}}
    )
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return {"message": "Task deleted"}
