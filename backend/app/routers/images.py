import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from sqlalchemy.orm import Session
from PIL import Image
from io import BytesIO

from .. import schemas, models
from ..dependencies import get_database_session
from ..ml_model.model_client import predict_via_http
from ..cloud_storage import storage_client  # Импортируем облачный клиент

router = APIRouter()

@router.post("/upload-image/", response_model=schemas.ImageProcessResponse)
async def upload_image(
    file: UploadFile = File(..., description="Изображение для анализа"),
    db: Session = Depends(get_database_session)
):
    """
    Загружает изображение в облачное хранилище, отправляет ML-модели,
    сохраняет результат в облачной БД.
    """
    
    # 1. ВАЛИДАЦИЯ: Проверяем, что файл является изображением
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть изображением (JPEG, PNG, etc.)"
        )

    try:
        # 2. ЧИТАЕМ СОДЕРЖИМОЕ ФАЙЛА В ПАМЯТЬ
        file_content = await file.read()
        
        # 3. СОХРАНЯЕМ В ОБЛАЧНОЕ ХРАНИЛИЩЕ (вместо локального диска)
        image_url = await storage_client.upload_file(file_content, file.filename)
        
        # 4. ОБРАБОТКА: Создаем изображение PIL из памяти
        pil_image = Image.open(BytesIO(file_content))
        
        # 5. ML-АНАЛИЗ: Отправляем изображение модели
        raw_prediction = predict_via_http(pil_image)
        
        # 6. ФИЛЬТРАЦИЯ: Обрабатываем сырой ответ модели
        filtered_tools = []
        for tool in raw_prediction.get("detections", []):
            if tool.get("confidence", 0) > 0.7:
                filtered_tools.append({
                    "tool_name": tool["name"],
                    "confidence": tool["confidence"],
                    "bbox": tool.get("bbox")
                })
        
        # 7. СОХРАНЕНИЕ В БД: Создаем запись в облачной БД
        db_image = models.ProcessedImage(
            image_filename=file.filename,
            raw_model_output=raw_prediction,
            filtered_tools=filtered_tools
        )
        
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        # 8. ФОРМИРУЕМ ОТВЕТ: Возвращаем URL из облачного хранилища
        return {
            "id": db_image.id,
            "image_url": image_url,  # URL из облачного хранилища!
            "result_image_url": None,
            "filtered_tools": filtered_tools,
            "processed_at": db_image.uploaded_at
        }

    except Exception as e:
        # Логируем ошибку (в продакшене лучше использовать logging)
        print(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обработке изображения: {str(e)}"
        )