import streamlit as st
import os
import sys

# Добавляем текущую папку в пути
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="🤖 Тест", layout="wide")
st.title("🤖 Тестовая версия")

# Проверка импортов
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    st.success("✅ HuggingFaceEmbeddings импортирован")
except ImportError as e:
    st.error(f"❌ HuggingFaceEmbeddings: {e}")

try:
    from langchain_community.llms import GigaChat
    st.success("✅ GigaChat импортирован")
except ImportError as e:
    st.error(f"❌ GigaChat: {e}")

try:
    from config import settings
    st.success("✅ Настройки импортированы")
    st.write(f"DATA_DIR: {settings.DATA_DIR}")
except ImportError as e:
    st.error(f"❌ Настройки: {e}")

try:
    from utils.knowledge_base import KnowledgeBase
    st.success("✅ KnowledgeBase импортирован")
except ImportError as e:
    st.error(f"❌ KnowledgeBase: {e}")

# Проверка файла .env
if os.path.exists('.env'):
    st.success("✅ Файл .env найден")
    with open('.env', 'r') as f:
        content = f.read()
        st.text(f"Содержимое: {content[:50]}...")
else:
    st.error("❌ Файл .env не найден")

st.write("---")
st.write("Если все проверки пройдены, можно запускать основное приложение")
