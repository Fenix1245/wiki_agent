import os
import base64
from gigachat import GigaChat

# Загружаем ключ из .env
with open('.env', 'r') as f:
    api_key = f.read().strip().split('=')[1]

print(f"Длина ключа: {len(api_key)} символов")
print(f"Ключ: {api_key[:50]}...")

try:
    # Пробуем подключиться
    giga = GigaChat(
        credentials=api_key,
        verify_ssl_certs=False,
        model="GigaChat-Pro",
        scope="GIGACHAT_API_PERS"
    )
    
    # Тестовый запрос
    response = giga.chat("Привет! Это тест.")
    print("✅ Подключение успешно!")
    print(f"Ответ: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
