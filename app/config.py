import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Blog App"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URI: str = os.getenv(
        "DATABASE_URI",
        "mysql+pymysql://root:parzival03@localhost/blog"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "blog_secret_key_1@1")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "def_jwt_secret_key_!(#)")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    cloudinary_url=os.getenv("CLOUDINARY_URL")


settings = Settings()