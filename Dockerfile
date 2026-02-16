FROM python:3.10-slim
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /RAG_chroma
## установим curl
#RUN apt-get update && apt-get install -y curl
# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь остальной код приложения
COPY /chromanew ./chromanew
COPY /SearchApi ./SearchApi
# "Сообщаем" Docker, что наше приложение будет работать на порту 5000
EXPOSE 5000

## Пропишем healthcheck
#HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=20s \
#  CMD curl -f http://localhost:8080/ || exit 1

# Указываем команду, которая запустится при старте контейнера
#CMD ["uvicorn", "SearchApi.main:app", "--host", "0.0.0.0", "--port", "5000"]
ENTRYPOINT ["uvicorn", "SearchApi.main:app", "--host", "0.0.0.0", "--port", "5000"]

