from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Your FastAPI backend is working!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # use Railway's dynamic PORT if available
    print(f"✅ Starting server on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port)
