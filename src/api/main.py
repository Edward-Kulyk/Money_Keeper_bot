from fastapi import FastAPI
from src.api.v1.routers import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.0.194", port=8000)
