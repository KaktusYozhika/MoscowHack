import io
from PIL import Image
import requests
from fastapi import HTTPException
from typing import Dict, Any
import os

def predict_via_http(image: Image.Image) -> Dict[str, Any]:
    """
    Заглушка (stub) для функции отправки изображения на ML-сервис.
    Пока возвращает тестовые данные, пока вы не настроите реальный ML-сервис.
    
    Args:
        image: Объект изображения PIL.Image
        
    Returns:
        dict: Тестовые данные распознавания инструментов
        
    Raises:
        HTTPException: Если произошла ошибка при обращении к ML-сервису
    """
    
    # ЗАГЛУШКА: возвращаем тестовые данные
    # УДАЛИТЕ этот блок, когда настроите реальный ML-сервис
    print("⚠️  ВНИМАНИЕ: Используются тестовые данные ML-модели")
    return {
        "detections": [
            {"name": "молоток", "confidence": 0.95, "bbox": [100, 150, 300, 400]},
            {"name": "отвертка", "confidence": 0.82, "bbox": [400, 200, 550, 450]},
            {"name": "гаечный ключ", "confidence": 0.65, "bbox": [600, 180, 750, 380]}
        ],
        "status": "success"
    }
    
    # РЕАЛЬНАЯ РЕАЛИЗАЦИЯ (раскомментируйте, когда будет готов ML-сервис):
    # """
    # Конвертируем изображение в байты для отправки
    # img_byte_arr = io.BytesIO()
    # image.save(img_byte_arr, format='JPEG')
    # img_byte_arr = img_byte_arr.getvalue()
    # 
    # # URL вашего ML-сервиса (берется из переменных окружения)
    # ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://localhost:8001/predict")
    # 
    # try:
    #     # Отправляем POST-запрос с изображением
    #     files = {'file': ('image.jpg', img_byte_arr, 'image/jpeg')}
    #     response = requests.post(ML_SERVICE_URL, files=files, timeout=30)
    #     response.raise_for_status()  # Проверяем статус ответа
    #     
    #     return response.json()  # Парсим JSON ответ
    #     
    # except requests.exceptions.RequestException as e:
    #     # Логируем ошибку и возвращаем понятное сообщение
    #     raise HTTPException(
    #         status_code=503, 
    #         detail=f"Ошибка соединения с ML-сервисом: {str(e)}"
    #     )
    # """