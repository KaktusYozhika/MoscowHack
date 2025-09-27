from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil
import uuid
from pathlib import Path

app = FastAPI()

 
MODEL_PATH = Path("weights/best.pt")
model = YOLO(str(MODEL_PATH))

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
 
    tmp_name = f"/tmp/{uuid.uuid4()}_{file.filename}"
    with open(tmp_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = model.predict(tmp_name, imgsz=1024, conf=0.25)

    predictions = []
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

    return {"filename": file.filename, "predictions": predictions}
