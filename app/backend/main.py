from fastapi import FastAPI
from routers import user
from routers import pill

app = FastAPI()

app.include_router(user.router)
app.include_router(pill.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}