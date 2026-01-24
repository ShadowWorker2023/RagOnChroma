FROM python:3.10-slim
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /RAG_chroma
# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь остальной код приложения
COPY ./chromanew ./chromanew
COPY ./SearchApi ./SearchApi
# "Сообщаем" Docker, что наше приложение будет работать на порту 5000
EXPOSE 5000
# Указываем команду, которая запустится при старте контейнера
CMD ["uvicorn", "SearchApi.main:app", "--host", "0.0.0.0", "--port", "5000"]

