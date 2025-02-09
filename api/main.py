from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Optional
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Load student data from JSON file
try:
    with open("student_marks.json", "r") as file:
        student_data = json.load(file)
    student_marks: Dict[str, int] = {student["name"]: student["marks"] for student in student_data}
except FileNotFoundError:
    raise HTTPException(status_code=500, detail="student_marks.json not found.")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
async def get_student_marks(name: Optional[List[str]] = Query(None)):
    if not name:
        return {"students": student_marks}
    
    results = {n: student_marks.get(n, "Not Found") for n in name}
    return results