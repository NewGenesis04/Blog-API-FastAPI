from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.database import engine
from app.db import models
from app.auth.auth import router as auth_router
from app.routers.blog.blog import router as blog_router
from app.routers.user.user import router as user_router
from app.routers.follow.follow import router as follow_router


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="/static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(blog_router, prefix="/blog", tags=["blog"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(follow_router, prefix="/follow", tags=["follow"])

@app.get('/')
def index():
    return {"message": "Welcome to the blog app"}