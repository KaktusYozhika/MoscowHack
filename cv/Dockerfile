FROM ultralytics/ultralytics:latest  # готовый образ с YOLO

WORKDIR /app

COPY app.py /app
COPY weights /app/weights

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
