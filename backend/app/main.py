from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, DateTime, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from typing import Optional
import os
from datetime import datetime
import uuid
from pathlib import Path
import requests

# Настройки базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./tools.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модели базы данных (аналогично вашим)
class ToolIssue(Base):
    __tablename__ = "tool_issues"
    
    IdOrder = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TabelID = Column(Integer, nullable=False, index=True)
    time = Column(DateTime(timezone=True), server_default=func.now())
    image_path = Column(String, nullable=True)  # Добавляем путь к изображению
    
    screwdriver_minus = Column(Integer, default=0)
    screwdriver_plus = Column(Integer, default=0)
    screwdriver_on_the_offset_cross = Column(Integer, default=0)
    whirlpool = Column(Integer, default=0)
    contouring_pliers = Column(Integer, default=0)
    pliers = Column(Integer, default=0)
    sharnitsa = Column(Integer, default=0)
    adjustable_wrench = Column(Integer, default=0)
    oil_can_opener = Column(Integer, default=0)
    horn_wrench_union = Column(Integer, default=0)
    side_cutters = Column(Integer, default=0)

class ToolReturn(Base):
    __tablename__ = "tool_returns"
    
    IdOrder = Column(Integer, primary_key=True, index=True, autoincrement=True)
    TabelID = Column(Integer, nullable=False, index=True)
    time = Column(DateTime(timezone=True), server_default=func.now())
    image_path = Column(String, nullable=True)  # Добавляем путь к изображению
    
    screwdriver_minus = Column(Integer, default=0)
    screwdriver_plus = Column(Integer, default=0)
    screwdriver_on_the_offset_cross = Column(Integer, default=0)
    whirlpool = Column(Integer, default=0)
    contouring_pliers = Column(Integer, default=0)
    pliers = Column(Integer, default=0)
    sharnitsa = Column(Integer, default=0)
    adjustable_wrench = Column(Integer, default=0)
    oil_can_opener = Column(Integer, default=0)
    horn_wrench_union = Column(Integer, default=0)
    side_cutters = Column(Integer, default=0)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tool Management API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Папка для загрузки изображений
UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

# Монтируем папку с изображениями как статическую
app.mount("/uploads", StaticFiles(directory="uploaded_images"), name="uploads")

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/process-tools")
async def process_tools(
    operation_type: str = Form(...),  # "issue" или "return"
    tabel_id: int = Form(...),
    recognition_threshold: float = Form(50),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Обработка заявки на выдачу или сдачу инструментов
    """
    
    # Валидация типа операции
    if operation_type not in ["issue", "return"]:
        raise HTTPException(status_code=400, detail="Invalid operation type")
    
    # Сохранение изображения
    file_extension = image.filename.split('.')[-1] if '.' in image.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / filename
    
    try:
        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving image: {str(e)}")
    
    # Логика распознавания инструментов на изображении
    recognized_tools, image_base64 = await recognize_tools_from_image(file_path, recognition_threshold)
    
    # Получаем полные данные распознавания для передачи confidence
    full_recognition_data = await get_full_recognition_data(file_path, recognition_threshold)

    # Выбор таблицы в зависимости от типа операции
    if operation_type == "issue":
        db_model = ToolIssue
    else:
        db_model = ToolReturn
    
    # Создание записи в базе данных
    db_record = db_model(
        TabelID=tabel_id,
        image_path=str(file_path),
        **recognized_tools  # Распаковать распознанные инструменты
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return {
        "success": True,
        "message": f"Operation '{operation_type}' completed successfully",
        "order_id": db_record.IdOrder,
        "tabel_id": db_record.TabelID,
        "image_url": f"/uploads/{filename}",
        "recognized_tools": recognized_tools,
        "image_base64": image_base64,
        "predictions_data": full_recognition_data.get("predictions", [])
    }

async def get_full_recognition_data(image_path: Path, threshold: int) -> dict:
    """Получает полные данные распознавания от CV-сервиса"""
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        params = {"conf": threshold/100}
        resp = requests.post(CV_URL, files=files, params=params)
        resp.raise_for_status()
        return resp.json()

CV_URL = os.getenv("CV_URL", "http://localhost:8001/predict")

async def recognize_tools_from_image(image_path: Path, threshold: float) -> dict:
    """
    Отправляет сохранённое изображение в CV-сервис,
    получает список предсказаний и преобразует их к полям БД.
    """

    # Открываем и отправляем файл в CV
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        params = {"conf": threshold/100}
        resp = requests.post(CV_URL, files=files, params=params)
        resp.raise_for_status()
        data = resp.json()

    # Маппинг YOLO-классов -> поля в таблицах backend
    CLASS_MAP = {
        "Отвертка_минус": "screwdriver_minus",
        "Отвертка_плюс": "screwdriver_plus",
        "Отвертка_смещенный_крест": "screwdriver_on_the_offset_cross",
        "Коловорот": "whirlpool",
        "Пассатижи_контровочные": "contouring_pliers",
        "Пассатижи": "pliers",
        "Шэрница": "sharnitsa",
        "Разводной_ключ": "adjustable_wrench",
        "Открывашка": "oil_can_opener",
        "Ключ_рожковый_накидной_3_4": "horn_wrench_union",
        "Бокорезы": "side_cutters",
    }

    # Инициализируем все поля 0
    counts = {field: 0 for field in CLASS_MAP.values()}

    # Считаем детекции по классам
    for pred in data.get("predictions", []):
        yolo_name = pred.get("class_name")
        if yolo_name in CLASS_MAP:
            db_field = CLASS_MAP[yolo_name]
            counts[db_field] += 1

    return counts, data.get("image_base64") 

@app.get("/")
def read_root():
    return {"message": "Tool Management API is running"}



# ПРОВЕРКА БД

@app.get("/api/issues")
def get_all_issues(db: Session = Depends(get_db)):
    """Получить все записи о выдаче инструментов"""
    issues = db.query(ToolIssue).all()
    
    result = []
    for issue in issues:
        result.append({
            'IdOrder': issue.IdOrder,
            'TabelID': issue.TabelID,
            'time': issue.time.isoformat() if issue.time else None,
            'image_path': issue.image_path,
            'screwdriver_minus': issue.screwdriver_minus,
            'screwdriver_plus': issue.screwdriver_plus,
            'screwdriver_on_the_offset_cross': issue.screwdriver_on_the_offset_cross,
            'whirlpool': issue.whirlpool,
            'contouring_pliers': issue.contouring_pliers,
            'pliers': issue.pliers,
            'sharnitsa': issue.sharnitsa,
            'adjustable_wrench': issue.adjustable_wrench,
            'oil_can_opener': issue.oil_can_opener,
            'horn_wrench_union': issue.horn_wrench_union,
            'side_cutters': issue.side_cutters
        })
    
    return result

@app.get("/api/returns")
def get_all_returns(db: Session = Depends(get_db)):
    """Получить все записи о сдаче инструментов"""
    returns = db.query(ToolReturn).all()
    
    result = []
    for return_item in returns:
        result.append({
            'IdOrder': return_item.IdOrder,
            'TabelID': return_item.TabelID,
            'time': return_item.time.isoformat() if return_item.time else None,
            'image_path': return_item.image_path,
            'screwdriver_minus': return_item.screwdriver_minus,
            'screwdriver_plus': return_item.screwdriver_plus,
            'screwdriver_on_the_offset_cross': return_item.screwdriver_on_the_offset_cross,
            'whirlpool': return_item.whirlpool,
            'contouring_pliers': return_item.contouring_pliers,
            'pliers': return_item.pliers,
            'sharnitsa': return_item.sharnitsa,
            'adjustable_wrench': return_item.adjustable_wrench,
            'oil_can_opener': return_item.oil_can_opener,
            'horn_wrench_union': return_item.horn_wrench_union,
            'side_cutters': return_item.side_cutters
        })
    
    return result

@app.get("/api/db-status")
def get_db_status(db: Session = Depends(get_db)):
    """Получить статистику по базе данных"""
    issues_count = db.query(ToolIssue).count()
    returns_count = db.query(ToolReturn).count()
    
    return {
        "tool_issues_count": issues_count,
        "tool_returns_count": returns_count,
        "database_file": "tools.db",
        "uploaded_images_count": len(list(UPLOAD_DIR.glob("*"))) if UPLOAD_DIR.exists() else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)