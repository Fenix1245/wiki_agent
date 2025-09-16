import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def reload_knowledge_base():
    """Полностью перезагружает базу знаний"""
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
        model_kwargs={'device': 'cpu'}
    )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    all_docs = []
    
    # Проходим по всем файлам в папке data
    for filename in os.listdir('data'):
        if filename.endswith('.txt'):
            filepath = os.path.join('data', filename)
            try:
                loader = TextLoader(filepath, encoding='utf-8')
                documents = loader.load()
                doc_splits = text_splitter.split_documents(documents)
                all_docs.extend(doc_splits)
                print(f"✅ Обработан: {filename}")
            except Exception as e:
                print(f"❌ Ошибка в {filename}: {e}")
    
    # Пересоздаем векторную базу
    vector_db = Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    vector_db.persist()
    
    print(f"🎉 База знаний перезагружена! Обработано документов: {len(all_docs)}")

if __name__ == "__main__":
    reload_knowledge_base()
