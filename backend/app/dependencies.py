from .database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

def get_database_session(db: Session = Depends(get_db)):
    """
    Dependency для получения сессии БД.
    Это простая обертка вокруг функции get_db из database.py.
    FastAPI автоматически внедряет эту зависимость в роутеры.
    
    Args:
        db: Сессия базы данных, которую автоматически предоставляет FastAPI
        
    Returns:
        Session: Объект сессии SQLAlchemy для работы с базой данных
    """
    return db