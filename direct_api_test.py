import requests
import base64
import json

# Ваши credentials
client_id = "bd121db3-5d56-4a56-8087-343e53a76c96"
client_secret = "6082bd18-23e3-440d-8357-30e79f7d255b"

# Получаем токен
auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
auth_data = {
    "grant_type": "client_credentials",
    "scope": "GIGACHAT_API_PERS"
}

# Basic auth
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

print("Получаем access token...")
response = requests.post(auth_url, data=auth_data, headers=headers, verify=False)

if response.status_code == 200:
    access_token = response.json()["access_token"]
    print(f"✅ Токен получен: {access_token[:50]}...")
    
    # Тестовый запрос к GigaChat
    chat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    chat_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    chat_data = {
        "model": "GigaChat-Pro",
        "messages": [{"role": "user", "content": "Привет! Это тест."}]
    }
    
    chat_response = requests.post(chat_url, json=chat_data, headers=chat_headers, verify=False)
    if chat_response.status_code == 200:
        print("✅ Чат работает!")
        print(chat_response.json()["choices"][0]["message"]["content"])
    else:
        print(f"❌ Ошибка чата: {chat_response.status_code}")
        print(chat_response.text)
else:
    print(f"❌ Ошибка авторизации: {response.status_code}")
    print(response.text)
