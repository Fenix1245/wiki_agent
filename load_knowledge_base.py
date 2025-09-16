import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def create_knowledge_base():
    """Создает векторную базу знаний из файлов в папке data/"""
    
    print("🔍 Начинаю создание базы знаний...")
    
    # Проверяем существование папки data
    if not os.path.exists('data'):
        print("❌ Папка 'data' не найдена!")
        print("Создайте папку 'data' и добавьте туда .txt файлы с информацией")
        return False
    
    # Получаем список файлов
    data_files = [f for f in os.listdir('data') if f.endswith('.txt')]
    
    if not data_files:
        print("❌ В папке 'data' нет .txt файлов!")
        print("Добавьте файлы с информацией в папку 'data/'")
        return False
    
    print(f"📁 Найдено файлов: {len(data_files)}")
    
    try:
        # Настраиваем модель для эмбеддингов
        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
            model_kwargs={'device': 'cpu'}
        )
        
        # Настраиваем разделитель текста
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Собираем все документы
        all_documents = []
        
        for filename in data_files:
            file_path = os.path.join('data', filename)
            print(f"📄 Обрабатываю: {filename}")
            
            try:
                # Загружаем файл
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
                
                # Разбиваем на чанки
                chunks = text_splitter.split_documents(documents)
                all_documents.extend(chunks)
                
                print(f"   ✅ Добавлено чанков: {len(chunks)}")
                
            except Exception as e:
                print(f"   ❌ Ошибка обработки {filename}: {e}")
                continue
        
        if not all_documents:
            print("❌ Не удалось обработать ни один файл!")
            return False
        
        print(f"📊 Всего чанков для обработки: {len(all_documents)}")
        
        # Создаем векторную базу
        print("🔄 Создаю векторную базу знаний...")
        vector_db = Chroma.from_documents(
            documents=all_documents,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        # Сохраняем базу
        vector_db.persist()
        
        print(f"✅ База знаний успешно создана!")
        print(f"📊 Обработано документов: {len(all_documents)}")
        print(f"💾 Сохранено в: ./chroma_db/")
        
        return True
        
    except Exception as e:
        print(f"❌ Критическая ошибка при создании базы знаний: {e}")
        return False

if __name__ == "__main__":
    create_knowledge_base()
