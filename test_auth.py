import base64
from gigachat import GigaChat
from gigachat.exceptions import AuthenticationError

def test_authentication():
    # Читаем ключ
    try:
        with open('.env', 'r') as f:
            api_key = f.read().strip().replace('GIGA_CHAT_API_KEY=', '')
    except FileNotFoundError:
        print("❌ Файл .env не найден")
        return
    
    print(f"Длина ключа: {len(api_key)} символов")
    
    try:
        client = GigaChat(
            credentials=api_key,
            verify_ssl_certs=False,
            scope="GIGACHAT_API_PERS"
        )
        
        # Пробуем сделать простой запрос
        response = client.chat("Тестовое сообщение")
        print("✅ Авторизация успешна!")
        print(f"Ответ: {response.choices[0].message.content}")
        
    except AuthenticationError as e:
        print(f"❌ Ошибка авторизации: {e}")
        print("Проверьте правильность ключа и scope")
    except Exception as e:
        print(f"❌ Другая ошибка: {e}")

if __name__ == "__main__":
    test_authentication()
