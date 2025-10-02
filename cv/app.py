from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil
import uuid
from pathlib import Path
import cv2
import base64
import tempfile
from PIL import Image, ImageDraw, ImageFont
import numpy as np

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

    results = model.predict(
        tmp_name, imgsz=1280, conf=conf,
        save=False, save_conf=True,
        agnostic_nms=True, iou=0.45
    )

    predictions = []
    r = results[0]

    # --- Визуализация через PIL (чтобы поддерживался русский текст) ---
    img = Image.fromarray(r.orig_img[..., ::-1])  # OpenCV BGR → RGB → PIL
    draw = ImageDraw.Draw(img)

    # Шрифт с поддержкой кириллицы
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()


    for box in r.boxes:
        cls_id = int(box.cls[0])
        conf_val = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, xyxy)

        # JSON (оставляем как было)
        predictions.append({
            "class_id": cls_id,
            "class_name": model.names[cls_id],
            "confidence": round(conf_val, 3),
            "bbox": [round(v, 2) for v in xyxy]
        })

        # Подпись: класс + процент
        label = f"{model.names[cls_id]} {conf_val*100:.1f}%%"

        # Бокс
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        # Фон под текстом
        bbox = draw.textbbox((0, 0), label, font=font)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        draw.rectangle([x1, y1 - text_h - 4, x1 + text_w, y1], fill="red")

        # Текст
        draw.text((x1, y1 - text_h - 2), label, fill="white", font=font)

    # --- Возврат картинки ---
    plotted_img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode(".jpg", plotted_img_bgr)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    Path(tmp_name).unlink(missing_ok=True)

    return {
        "filename": file.filename,
        "predictions": predictions,
        "image_base64": img_base64
    }
