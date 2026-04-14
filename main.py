from fastapi import FastAPI, Request, status
import models
from database import engine, SessionLocal
from routers import todos, auth, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def test(request: Request):
    user = auth.get_user_from_cookie(request)
    if user:
        return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
    if request.cookies.get("access_token"):
        return auth.redirect_to_login()
    return RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
async def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
