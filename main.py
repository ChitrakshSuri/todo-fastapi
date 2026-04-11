from fastapi import FastAPI
import models
from database import engine, SessionLocal
from routers import todos, auth, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/healthy")
async def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
