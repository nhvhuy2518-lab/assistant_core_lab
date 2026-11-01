from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Hello API")

COURSES = {
    "CSC10014": "Computational Thinking",
    "CSC10001": "Introduction to Programming",
}


# P1
@app.get("/")
def home() -> dict:
    return {"message": "Hello, CSC10014!"}


# P2: path parameter
@app.get("/hello/{name}")
def hello(name: str) -> dict:
    return {"message": f"Hello, {name}!"}


# P3: query parameter
@app.get("/square")
def square(n: int) -> dict:
    return {"n": n, "square": n * n}


# P4: request body with Pydantic model
class Numbers(BaseModel):
    a: float
    b: float


@app.post("/add")
def add(nums: Numbers) -> dict:
    return {"sum": nums.a + nums.b}


# P5: errors
@app.get("/courses/{code}")
def course(code: str) -> dict:
    if code not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"code": code, "name": COURSES[code]}
