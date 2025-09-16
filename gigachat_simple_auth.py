import os
import requests
import uuid
import base64
from datetime import datetime, timedelta

class SimpleGigaAuth:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self.token_expires = None
        self.load_credentials()
    
    def load_credentials(self):
        """Загружаем учетные данные из .env"""
        try:
            if not os.path.exists('.env'):
                return False
                
            with open('.env', 'r') as f:
                content = f.read()
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('GIGA_CLIENT_ID='):
                    self.client_id = line.split('=', 1)[1].strip()
                elif line.startswith('GIGA_CLIENT_SECRET='):
                    self.client_secret = line.split('=', 1)[1].strip()
            
            return bool(self.client_id and self.client_secret)
            
        except:
            return False
    
    def get_token(self):
        """Получаем новый токен"""
        if not self.client_id or not self.client_secret:
            return None
            
        try:
            # Кодируем в base64
            credentials = f"{self.client_id}:{self.client_secret}"
            base64_credentials = base64.b64encode(credentials.encode()).decode()
            
            # Делаем запрос
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Authorization': f'Basic {base64_credentials}',
                'RqUID': str(uuid.uuid4()),
            }
            
            data = {'scope': 'GIGACHAT_API_PERS'}
            
            response = requests.post(url, headers=headers, data=data, verify=False, timeout=30)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                self.token_expires = datetime.now() + timedelta(minutes=25)
                return self.access_token
            else:
                print(f"Ошибка: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None

# Глобальный экземпляр
auth = SimpleGigaAuth()

def get_gigachat_token():
    """Простая функция для получения токена"""
    if auth.access_token and auth.token_expires and datetime.now() < auth.token_expires:
        return auth.access_token
    return auth.get_token()
