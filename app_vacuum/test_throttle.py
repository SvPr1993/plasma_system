import requests
from concurrent.futures import ThreadPoolExecutor

url = "http://127.0.0.1:8000/ballon/"
params = {
    "volume_liters": 10,
    "pressure_bar": 5,
    "temperature_Celsius": 25
}


def make_request(i):
    try:
        resp = requests.get(url, params=params)
        print(f"Запрос {i}: статус {resp.status_code}, ответ: {resp.json()}")
    except Exception as e:
        print(f"Запрос {i}: ошибка {e}")


# Отправляем 10 запросов параллельно (можно изменить количество)
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(make_request, range(10))
