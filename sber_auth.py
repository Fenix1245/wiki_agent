import requests
import base64
import json

# ЗАМЕНИТЕ на ваши реальные данные из личного кабинета Сбера
client_id = "bd121db3-5d56-4a56-8087-343e53a76c96"
client_secret = "082bd18-23e3-440d-8357-30e79f7d255b"

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

# Попробуем разные scope
scopes_to_try = [
    "GIGACHAT_API_PERS",
    "api",
    "openid",
    "profile",
    "email",
    "GIGACHAT_API_CORP"
]

# Подготовка заголовков
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

print(f"Client ID: {client_id}")
print(f"Encoded credentials: {credentials}")

for scope in scopes_to_try:
    data = {
        "grant_type": "client_credentials",
        "scope": scope
    }
    
    print(f"\n--- Пробуем scope: {scope} ---")
    print(f"Данные: {data}")
    
    try:
        response = requests.post(url, data=data, headers=headers, verify=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ УСПЕХ!")
            print(f"Access Token: {token_data.get('access_token')}")
            print(f"Token Type: {token_data.get('token_type')}")
            print(f"Expires In: {token_data.get('expires_in')}")
            break
        else:
            print(f"❌ Ошибка со scope: {scope}")
            try:
                error_data = response.json()
                print(f"Код ошибки: {error_data.get('code')}")
                print(f"Сообщение: {error_data.get('message')}")
            except:
                print("Не удалось распарсить JSON ошибки")
                
    except Exception as e:
        print(f"🚫 Исключение: {e}")

# Попробуем без scope
print("\n--- Пробуем БЕЗ scope ---")
data_no_scope = {
    "grant_type": "client_credentials"
}

try:
    response = requests.post(url, data=data_no_scope, headers=headers, verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"🚫 Исключение: {e}")
