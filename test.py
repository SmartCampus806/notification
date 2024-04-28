import requests

API_BASE_URL = "http://172.28.16.1:8000"  # Замените на ваш базовый URL
username = "notification@bot.ru"
password = "root"

url = f"{API_BASE_URL}/api/auth/login"
data = {"username": username, "password": password}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Успешно выполнен POST запрос")
    print("Ответ сервера:", response.json())
else:
    print("Ошибка при выполнении POST запроса")
    print("Статус код:", response.status_code)
    print("Текст ошибки:", response.text)
    print(response)
