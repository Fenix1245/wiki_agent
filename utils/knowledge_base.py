import os
from datetime import datetime
import getpass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# Закомментируйте проблемный импорт
# from team_ai_assistant.config.settings import DATA_DIR, CHROMA_DIR, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

# Добавьте временные настройки
import os
from pathlib import Path

# Временные настройки
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

class KnowledgeBase:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
    
    def add_document(self, text, filename, author=None):
        """Добавляет документ в базу знаний"""
        if author is None:
            author = getpass.getuser()
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_text = f"""[ДОБАВЛЕНО]: {current_date}
[АВТОР]: {author}

{text}
"""
        # Сохраняем файл
        filepath = DATA_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(formatted_text)
        
        # Добавляем в векторную базу
        try:
            loader = TextLoader(str(filepath), encoding='utf-8')
            documents = loader.load()
            doc_splits = self.text_splitter.split_documents(documents)
            
            vector_db = Chroma(
                persist_directory=str(CHROMA_DIR),
                embedding_function=self.embeddings
            )
            
            vector_db.add_documents(doc_splits)
            vector_db.persist()
            
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении документа: {e}")
            return False
    
    def get_vector_db(self):
        """Возвращает векторную базу данных"""
        return Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=self.embeddings
        )

