import os
import base64

with open('.env', 'r') as f:
    content = f.read().strip()
    
if '=' in content:
    key = content.split('=')[1]
else:
    key = content

print(f"Текущий ключ: {key}")
print(f"Длина: {len(key)} символов")

# Проверим тип ключа
if key.startswith('sk_'):
    print("✅ Это похоже на API Key")
elif ':' in key:
    print("❌ Это Client Credentials (логин:пароль)")
    print("Нужен API Key, а не Client Credentials!")
elif len(key) > 100:
    print("❌ Это encoded credentials (base64)")
    try:
        decoded = base64.b64decode(key).decode()
        print(f"Декодировано: {decoded}")
        if 'Basic' in decoded or ':' in decoded:
            print("❌ Это Client Credentials в base64")
    except:
        print("Не удалось декодировать base64")
else:
    print("❓ Неизвестный формат ключа")
