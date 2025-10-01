# MoscowHack: Автоматизация приёма и выдачи инструментов

## Описание
Сервис позволяет по фотографии автоматически распознавать набор инструментов и сверять их с эталонным списком. Решение состоит из:
- Frontend (HTML/CSS/JS + Nginx)
- Backend (FastAPI, работа с данными и API)
- CV-сервис (YOLOv8 для распознавания изображений)

## Быстрый старт
```bash
git clone https://github.com/KaktusYozhika/MoscowHack
cd MoscowHack
docker compose up --build
```
