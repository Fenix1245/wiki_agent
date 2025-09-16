import base64

def create_base64_key(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    return base64.b64encode(credentials.encode()).decode()

if __name__ == "__main__":
    client_id = input("Введите client_id: ")
    client_secret = input("Введите client_secret: ")
    
    base64_key = create_base64_key(client_id, client_secret)
    print(f"Base64 ключ: {base64_key}")
    
    # Сохраняем в .env
    with open('.env', 'w') as f:
        f.write(f"GIGA_CHAT_API_KEY={base64_key}")
    
    print("Ключ сохранен в файл .env")
