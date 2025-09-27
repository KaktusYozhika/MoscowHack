from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil
import uuid
from pathlib import Path
import cv2
import base64

app = FastAPI()

 
MODEL_PATH = Path("weights/best.pt")
model = YOLO(str(MODEL_PATH))

@app.post("/predict")
async def predict(file: UploadFile = File(...), conf: float = 0.25):
 
    tmp_name = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(tmp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    results = model.predict(tmp_name, imgsz=1024, conf=conf, save=False, save_conf=True)

    predictions = []
 
    img = cv2.imread(tmp_name)

    for r in results:
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
 
            x1, y1, x2, y2 = map(int, xyxy)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{model.names[cls_id]} {conf:.2f}",
                        (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0), 2)
 
    _, buffer = cv2.imencode(".jpg", img)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "filename": file.filename,
        "predictions": predictions,
        "image_base64": img_base64
    }