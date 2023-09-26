#!/bin/bash
source venv/bin/activate
# Запуск FastAPI сервера
uvicorn main:app --host 0.0.0.0 --port 8000
