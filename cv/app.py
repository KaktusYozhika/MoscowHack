from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil
import uuid
from pathlib import Path
import cv2
import base64
import tempfile

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

 
MODEL_PATH = Path("weights/best.pt")
model = YOLO(str(MODEL_PATH))

@app.post("/predict")
async def predict(file: UploadFile = File(...), conf: float = 0.25):
    
    tmp_dir = tempfile.gettempdir()
    tmp_name = str(Path(tmp_dir) / f"{uuid.uuid4()}_{file.filename}")
    with open(tmp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    # Используем встроенную отрисовку Ultralytics
    results = model.predict(tmp_name, imgsz=1280, conf=conf, save=False, save_conf=True, agnostic_nms=True, iou=0.45)

    predictions = []
    
    # Берем первый результат (т.к. обрабатываем одно изображение)
    r = results[0]
    
    # Используем встроенный метод plot() для отрисовки
    plotted_img = r.plot()  # возвращает numpy array в формате RGB
    
    # Конвертируем RGB в BGR для OpenCV
    plotted_img_bgr = cv2.cvtColor(plotted_img, cv2.COLOR_RGB2BGR)
    
    # Собираем предсказания
    for box in r.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()

        predictions.append({
            "class_id": cls_id,
            "class_name": model.names[cls_id],
            "confidence": round(conf, 3),
            "bbox": [round(v, 2) for v in xyxy]
        })
 
    # Кодируем изображение
    _, buffer = cv2.imencode(".jpg", plotted_img_bgr)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    # Удаляем временный файл
    Path(tmp_name).unlink(missing_ok=True)

    return {
        "filename": file.filename,
        "predictions": predictions,
        "image_base64": img_base64
    }