from fastapi import FastAPI
from routers import user

app = FastAPI()

app.include_router(user.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}