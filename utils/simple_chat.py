import requests
from gigachat_simple_auth import get_gigachat_token

def ask_gigachat_simple(question, context=None):
    """Самый простой запрос к GigaChat"""
    
    token = get_gigachat_token()
    if not token:
        return "❌ Ошибка аутентификации"
    
    # Формируем промпт
    if context:
        prompt = f"""Ответь на вопрос используя только этот контекст:

{context}

Вопрос: {question}

Ответ:"""
    else:
        prompt = question
    
    # Делаем запрос
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": "GigaChat-Pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, verify=False, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"❌ Ошибка API: {response.status_code}"
            
    except Exception as e:
        return f"❌ Ошибка: {e}"

# Тест
if __name__ == "__main__":
    response = ask_gigachat_simple("Привет! Ответь очень коротко.")
    print(f"Ответ: {response}")
