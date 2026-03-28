from fastapi import FastAPI, HTTPException

app = FastAPI()

logs = []

@app.get("/")
def home():
    return {"message": "Target App is Running"}

@app.get("/divide")
def divide(a: int, b: int):
    try:
        result = a / b
        return {"result": result}
    except Exception as e:
        logs.append({"endpoint": "divide", "error": str(e)})
        raise HTTPException(status_code=500, detail="Division failed")

@app.post("/login")
def login(data: dict):
    username = data.get("username")

    if username is None:
        logs.append({"endpoint": "login", "error": "Missing username"})
        raise HTTPException(status_code=400, detail="Username required")

    if not isinstance(username, str) or username.strip() == "":
        logs.append({"endpoint": "login", "error": "Invalid username"})
        raise HTTPException(status_code=400, detail="Invalid username")

    return {"message": "Login successful"}

@app.post("/age-check")
def age_check(data: dict):
    age = data.get("age")

    if age is None:
        logs.append({"endpoint": "age-check", "error": "Missing age"})
        raise HTTPException(status_code=400, detail="Age required")

    if not isinstance(age, int):
        logs.append({"endpoint": "age-check", "error": "Invalid age type"})
        raise HTTPException(status_code=400, detail="Age must be number")

    if age < 0:
        logs.append({"endpoint": "age-check", "error": "Negative age"})
        raise HTTPException(status_code=400, detail="Invalid age")

    if age > 120:
        logs.append({"endpoint": "age-check", "error": "Unrealistic age"})
        raise HTTPException(status_code=400, detail="Unrealistic age")

    return {"message": "Age accepted"}

@app.get("/logs")
def get_logs():
    return logs


@app.post("/clear-logs")
def clear_logs():
    logs.clear()
    return {"message": "Logs cleared successfully"}