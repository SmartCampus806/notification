# Используем официальный образ Python
FROM python:3.9

# Копируем зависимости внутрь контейнера
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы из текущего каталога внутрь контейнера
COPY . .

# Команда для запуска вашего приложения
CMD ["python", "main.py"]