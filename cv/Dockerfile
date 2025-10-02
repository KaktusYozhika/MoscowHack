FROM ultralytics/ultralytics:latest  

WORKDIR /app

COPY app.py /app
COPY weights /app/weights

RUN pip install fastapi uvicorn python-multipart

RUN apt-get update && apt-get install -y fonts-dejavu-core


EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]

