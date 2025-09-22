from fastapi import FastAPI
from routers import user, pill, chat

app = FastAPI()

app.include_router(user.router)
app.include_router(pill.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}