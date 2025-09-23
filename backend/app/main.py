from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import images, tool_orders

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Tool Management & Recognition API",
    description="Комбинированный API для учета инструментов и их распознавания по фото",
    version="2.0.0",

    docs_url="/docs",                    # URL для Swagger UI (можно изменить)
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
app.include_router(tool_orders.router, prefix="/api/v1", tags=["tool management"])
app.include_router(images.router, prefix="/api/v1", tags=["image recognition"])

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы API""" # документация
    return { # Возвращаем словарь, который автоматически станет JSON
        "message": "Tool Management & Recognition API работает!",
        "version": "2.0.0", 
        "environment": "cloud",
        "available_modules": { # Полезная информация для разработчиков
            "управление_инструментами": {
                "выдача_инструментов": "POST /api/v1/issue-tools/",
                "сдача_инструментов": "POST /api/v1/return-tools/",
                "история_сотрудника": "GET /api/v1/employee-history/{id}"
            },
            "распознавание_по_фото": {
                "загрузить_изображение": "POST /api/v1/upload-image/"
            }
        }
    }

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return {"status": "healthy", "database": "connected"}