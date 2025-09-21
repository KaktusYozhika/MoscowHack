from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import images

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Tool Recognition Cloud API",
    description="API для распознавания инструментов на изображениях в облаке",
    version="1.0.0"
)

# Настраиваем CORS для доступа из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(images.router, prefix="/api/v1", tags=["images"])

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы API"""
    return {
        "message": "Tool Recognition Cloud API работает!",
        "version": "1.0.0",
        "environment": "cloud"
    }

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return {"status": "healthy", "database": "connected"}