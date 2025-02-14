from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.auth.auth import router as auth_router
from app.routers.blog.blog import router as blog_router
from app.routers.user.user import router as user_router
from app.routers.follow.follow import router as follow_router
from app.routers.comments.coments import router as comments_router
from app.routers.files.files import router as files_router
import os
import cloudinary
from dotenv import load_dotenv
from pathlib import Path
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="/static")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(blog_router, prefix="/blog", tags=["blog"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(follow_router, prefix="/follow", tags=["follow"])
app.include_router(comments_router, prefix="/comments")
app.include_router(files_router, prefix="/files", tags=["files"])

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@app.get('/')
def index():
    return {"message": "Welcome to the blog app"}