# Импортируем необходимые инструменты
import os
from langchain.document_loaders import TextLoader  # Инструмент для загрузки текстовых файлов
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Инструмент для разбивки текста на части (чанки)
from langchain.embeddings import HuggingFaceEmbeddings  # Модель для преобразования текста в числа (векторы)
from langchain.vectorstores import Chroma  # Векторная база данных, где мы будем хранить наши векторы

# -------------------- 1. НАСТРОЙКИ --------------------
# Указываем путь к папке с нашими данными
data_directory = "data"  # Это имя папки, которую мы создали

# Выбираем модель для создания векторных представлений (эмбеддингов).
# 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2' — это умная модель, которая понимает смысл текста на многих языках, включая русский.
embeddings_model_name = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'

# Создаем объект модели, которая будет преобразовывать текст в векторы.
# model_kwargs={'device': 'cpu'} говорит модели работать на центральном процессоре (это нормально для начала).
embeddings = HuggingFaceEmbeddings(
    model_name=embeddings_model_name,
    model_kwargs={'device': 'cpu'}
)

# Настраиваем "резчик текста". Он будет делить большие документы на маленькие, удобные для поиска части.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # Размер одного чанка ~1000 символов.
    chunk_overlap=200   # Перекрытие между чанками 200 символов, чтобы не терять смысл на стыках.
)

# -------------------- 2. ЗАГРУЗКА И ОБРАБОТКА ФАЙЛОВ --------------------
# Создаем пустой список, куда мы сложим все кусочки текста (чанки) из всех файлов.
all_docs_splits = []

print("🔍 Начинаю загрузку данных...")

# Проходим по всем файлам в указанной папке 'data'
for filename in os.listdir(data_directory):
    # Составляем полный путь к файлу
    file_path = os.path.join(data_directory, filename)
    print(f"Обрабатываю файл: {filename}")

    try:
        # Загружаем содержимое текстового файла
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()  # Этот метод возвращает список документов

        # Разбиваем загруженный текст на чанки с помощью нашего "резчика"
        doc_splits = text_splitter.split_documents(documents)

        # Добавляем все полученные чанки из этого файла в общий список
        all_docs_splits.extend(doc_splits)

    except Exception as e:
        # Если с каким-то файлом возникла проблема (например, не тот формат), мы просто сообщим об этом и продолжим работу
        print(f"❌ Не удалось обработать файл {filename}: {e}")

# -------------------- 3. СОЗДАНИЕ БАЗЫ ЗНАНИЙ --------------------
print("📦 Создаю векторную базу знаний...")

# Теперь мы берем все наши текстовые чанки (all_docs_splits) и преобразуем их в векторы с помощью модели (embeddings).
# Эти векторы сохраняются в векторную базу данных Chroma.
# persist_directory="./chroma_db" — указывает, что база должна сохраниться на диск в папку 'chroma_db'.
vector_db = Chroma.from_documents(
    documents=all_docs_splits,
    embedding=embeddings,
    persist_directory="./chroma_db"  # Папка, где будет храниться наша "память"
)

# Фиксируем изменения и сохраняем базу данных на диск.
vector_db.persist()

print("✅ Готово! Векторная база знаний успешно создана и сохранена в папку 'chroma_db'.")
print(f"📊 Обработано чанков: {len(all_docs_splits)}")
