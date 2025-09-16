import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Создаем папки если их нет
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

# Настройки модели
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
LLM_MODEL = "GigaChat-Pro"
LLM_SCOPE = "GIGACHAT_API_PERS"

# Настройки текста
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
