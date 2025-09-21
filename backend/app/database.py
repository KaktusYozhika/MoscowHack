from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем строку подключения ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# Это критически важно для облачного развертывания!
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Создаем движок для подключения к PostgreSQL
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Dependency для получения сессии БД.
    FastAPI автоматически вызывает эту функцию для каждого запроса.
    """
    db = SessionLocal()
    try:
        yield db  # Отдаем сессию в роутер
    finally:
        db.close()  # Гарантируем закрытие сессии