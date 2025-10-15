from fastapi import FastAPI

app = FastAPI(title="Smart Parking API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Welcome to Smart Parking API"}

@app.get("/owners/")
def list_owners():
    return [{"id": 1, "name": "Alice"}]
