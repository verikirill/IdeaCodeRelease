from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from models import Base
from database import engine
from routes import api_router

app = FastAPI(title="ИдеяРелиз API", description="API for IdeaCodeRelease platform")

# Allow all origins for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Убедиться, что директория для статических файлов существует
os.makedirs("static", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/uploads/gallery", exist_ok=True)
os.makedirs("static/uploads/posts", exist_ok=True)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "IdeaRelease API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="89.169.1.14", port=8000, reload=True)