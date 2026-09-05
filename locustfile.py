from locust import HttpUser, task, between
import random


class ApiUser(HttpUser):
    # Задержка между задачами для имитации реального пользователя
    wait_time = between(0.5, 2.0)

    @task(3)  # вес: 3 из 4 запросов будут на /ballon/
    def test_ballon(self):
        # Параметры для /ballon/ – берём случайные значения в разумных пределах
        params = {
            "volume_liters": random.randint(1, 50),
            "pressure_bar": random.randint(1, 10),
            "temperature_Celsius": random.randint(-20, 50)
        }
        with self.client.get("/ballon/", params=params, catch_response=True) as response:
            if response.status_code == 429:
                response.failure("Too Many Requests (throttling works)")
            elif response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                # Можно проверить содержимое ответа
                try:
                    data = response.json()
                    if "result" not in data:
                        response.failure("No 'result' field in response")
                except ValueError:
                    response.failure("Response is not valid JSON")

    @task(1)  # вес: 1 из 4 запросов на вакуумный API
    def test_vacuum(self):
        params = {
            "vacuum_value": round(random.uniform(0.0, 1.0), 3)
        }
        with self.client.get("/vacuum/api/check_vacuum/", params=params, catch_response=True) as response:
            if response.status_code == 429:
                response.failure("Too Many Requests (throttling works)")
            elif response.status_code != 200:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                try:
                    data = response.json()
                    if "status" not in data:
                        response.failure("No 'status' field in response")
                except ValueError:
                    response.failure("Response is not valid JSON")
