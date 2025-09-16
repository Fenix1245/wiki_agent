import requests

url = "https://api.sberbank.ru/oauth/token"  # Это пример URL. Замените на нужный из документации.
data = {
    "grant_type": "client_credentials",
    "client_id": "bd121db3-5d56-4a56-8087-343e53a76c96",  # Укажите свой client_id
    "client_secret": "ff28160d-0d30-4713-ab96-419855378d92"  # Укажите свой client_secret
}

response = requests.post(url, data=data)  # Отправка POST-запроса
access_token = response.json().get("access_token")  # Извлекаем access_token из ответа
print(access_token)  # Выводим полученный токен
