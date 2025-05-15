from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Face Recognition System")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)