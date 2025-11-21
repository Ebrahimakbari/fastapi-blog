import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    project_name:str = "FastApi Blog project"
    project_version:str = "1.0.0"

    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_blog")
    
    DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "v+s)k2d)s#!6f!6(()_a988+%sxo)#sksc+y8361(+16!42wm8")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    ALLOWED_DOCUMENT_TYPES: list = ["application/pdf", "text/plain", "application/msword"]
    ALLOWED_VIDEO_TYPES: list = ["video/mp4", "video/mpeg", "video/quicktime"]
    
    # Create directories if they don't exist
    def __init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(f"{self.UPLOAD_DIR}/images", exist_ok=True)
        os.makedirs(f"{self.UPLOAD_DIR}/documents", exist_ok=True)
        os.makedirs(f"{self.UPLOAD_DIR}/videos", exist_ok=True)
        os.makedirs(f"{self.UPLOAD_DIR}/avatars", exist_ok=True)

settings = Settings()