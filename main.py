import streamlit as st
import os
import sys
from datetime import datetime
import time

# Добавляем текущую директорию в путь
sys.path.append('.')

# Настройка страницы
st.set_page_config(
    page_title="🤖 ИИ-Ассистент команды",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Заголовок приложения
st.title("🤖 ИИ-Ассистент команды")
st.markdown("Задайте вопрос о доступах, системах и процессах команды")

# Импортируем наши утилиты
from utils.simple_chat import ask_gigachat_simple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Боковая панель для добавления новых знаний
with st.sidebar:
    st.header("📤 Добавить новую информацию")
    
    # Поле для ввода фамилии автора
    author = st.text_input("👤 Ваша фамилия:", placeholder="Иванова")
    
    # Выбор типа информации
    info_type = st.selectbox(
        "Тип информации:", 
        ["Процесс/Инструкция", "Проект/Ссылки", "Доступ сотрудника", "Другое"]
    )
    
    if not author:
        st.warning("⚠️ Пожалуйста, укажите вашу фамилию")
    
    # Формы для разных типов информации
    if info_type == "Процесс/Инструкция":
        st.subheader("📋 Добавить процесс")
        process_name = st.text_input("Название процесса:")
        steps = st.text_area("Шаги (по одному на строку):", height=150,
                           placeholder="1. Первый шаг\n2. Второй шаг\n3. Третий шаг")
        tags = st.text_input("Теги (через запятую):", placeholder="#поставка #деплой")
        
        if st.button("✅ Добавить процесс") and author:
            if process_name and steps:
                new_text = f"""[ТИП]: Процесс
[НАЗВАНИЕ]: {process_name}
[ШАГИ]:
{steps}
[ТЕГИ]: {tags}
"""
                try:
                    from utils.knowledge_base import KnowledgeBase
                    kb = KnowledgeBase()
                    if kb.add_document(new_text, f"process_{process_name}.txt", author):
                        st.success("✅ Процесс добавлен в базу знаний!")
                        time.sleep(2)
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
            else:
                st.warning("Заполните название и шаги процесса")
    
    elif info_type == "Проект/Ссылки":
        st.subheader("🔗 Добавить проект")
        project_name = st.text_input("Название проекта:")
        links = st.text_area("Ссылки (название: ссылка):", height=150,
                          placeholder="OpenShift: https://console.openshift.com\nGrafana: https://grafana.com")
        description = st.text_area("Описание проекта:")
        tags = st.text_input("Теги (через запятую):", placeholder="#пром #блок1")
        
        if st.button("✅ Добавить проект") and author:
            if project_name:
                new_text = f"""[ТИП]: Проект  
[НАЗВАНИЕ]: {project_name}
[ССЫЛКИ]:
{links}
[ОПИСАНИЕ]: {description}
[ТЕГИ]: {tags}
"""
                try:
                    from utils.knowledge_base import KnowledgeBase
                    kb = KnowledgeBase()
                    if kb.add_document(new_text, f"project_{project_name}.txt", author):
                        st.success("✅ Проект добавлен в базу знаний!")
                        time.sleep(2)
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
            else:
                st.warning("Введите название проекта")
    
    elif info_type == "Доступ сотрудника":
        st.subheader("👥 Добавить доступ")
        employee = st.text_input("Фамилия сотрудника:")
        system = st.text_input("Система/Ресурс:")
        date = st.text_input("Дата доступа:", placeholder=datetime.now().strftime('%Y-%m-%d'))
        comment = st.text_area("Комментарий:")
        tags = st.text_input("Теги (через запятую):", placeholder="#доступ #crm")
        
        if st.button("✅ Добавить доступ") and author:
            if employee and system:
                new_text = f"""[ТИП]: Доступ
[СОТРУДНИК]: {employee}
[СИСТЕМА]: {system}
[ДАТА]: {date if date else datetime.now().strftime('%Y-%m-%d')}
[КОММЕНТАРИЙ]: {comment}
[ТЕГИ]: {tags}
"""
                try:
                    from utils.knowledge_base import KnowledgeBase
                    kb = KnowledgeBase()
                    if kb.add_document(new_text, f"access_{employee}.txt", author):
                        st.success("✅ Доступ добавлен в базу знаний!")
                        time.sleep(2)
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
            else:
                st.warning("Заполните фамилию сотрудника и систему")
    
    else:
        st.subheader("📝 Произвольная информация")
        title = st.text_input("Заголовок:")
        content = st.text_area("Содержание:", height=200)
        tags = st.text_input("Теги (через запятую):")
        
        if st.button("📝 Добавить информацию") and author:
            if content:
                filename = f"info_{title.lower().replace(' ', '_')}.txt" if title else "user_input.txt"
                new_text = f"""[ТИП]: Информация
[ЗАГОЛОВОК]: {title}
[СОДЕРЖАНИЕ]: {content}
[ТЕГИ]: {tags}
"""
                try:
                    from utils.knowledge_base import KnowledgeBase
                    kb = KnowledgeBase()
                    if kb.add_document(new_text, filename, author):
                        st.success("✅ Информация добавлена в базу знаний!")
                        time.sleep(2)
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка: {e}")
            else:
                st.warning("Введите содержание информации")

# Основной интерфейс
st.header("💬 Задайте вопрос")

# Инициализация базы знаний
@st.cache_resource
def init_knowledge_base():
    """Инициализация векторной базы знаний"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/paraphrase-multilingual-mpnet-base-v2',
            model_kwargs={'device': 'cpu'}
        )
        
        vector_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        
        st.success("✅ База знаний загружена")
        return vector_db
    except Exception as e:
        st.error(f"❌ Ошибка базы знаний: {e}")
        return None

# Загрузка базы знаний
vector_db = init_knowledge_base()

if vector_db is None:
    st.error("Не удалось загрузить базу знаний. Проверьте папку chroma_db/")
    st.stop()

# Создание простой цепочки вопрос-ответ
def create_simple_qa_chain(_vector_db):
    """Простая цепочка для вопросов и ответов"""
    
    def simple_qa(query):
        try:
            # Ищем релевантные документы
            relevant_docs = _vector_db.similarity_search(query, k=3)
            
            # Формируем контекст из найденных документов
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            if not context:
                return {
                    "result": "🤷‍♀️ В базе знаний нет информации по этому вопросу",
                    "source_documents": []
                }
            
            # Используем наш простой адаптер
            answer = ask_gigachat_simple(query, context)
            
            return {
                "result": answer,
                "source_documents": relevant_docs
            }
            
        except Exception as e:
            return {
                "result": f"❌ Ошибка при поиске ответа: {e}",
                "source_documents": []
            }
    
    return simple_qa

# Создаем цепочку
qa_chain = create_simple_qa_chain(vector_db)

# Поле для вопроса
question = st.text_input(
    "Ваш вопрос:",
    placeholder="Например: Как получить доступ к CRM? Или: Какие проекты есть у нас?",
    key="question_input"
)

# Кнопка для отправки вопроса
if st.button("🔍 Найти ответ", type="primary") or question:
    if question:
        with st.spinner("🤔 Ищу ответ..."):
            try:
                # Ищем ответ
                result = qa_chain(question)
                
                # Показываем ответ
                st.success("✅ Ответ найден!")
                st.markdown(f"**Ответ:** {result['result']}")
                
                # Показываем источники
                with st.expander("📚 Источники информации"):
                    if result['source_documents']:
                        for i, doc in enumerate(result['source_documents']):
                            source = doc.metadata.get('source', 'Неизвестный источник')
                            filename = os.path.basename(source)
                            st.markdown(f"**{i+1}. {filename}**")
                            st.caption(doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content)
                            st.markdown("---")
                    else:
                        st.info("Источники не найдены")
                        
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Ошибка: {error_msg}")
    else:
        st.warning("Введите вопрос для поиска")

# Расширенный поиск
with st.expander("🔍 Расширенный поиск", expanded=False):
    st.write("Поиск по конкретным тегам или фразам:")
    exact_search = st.text_input("Точный поиск:", placeholder="#б1 или openshift", key="exact_search")
    
    if st.button("Искать в файлах") and exact_search:
        with st.spinner("🔍 Ищу в файлах..."):
            try:
                import glob
                found_files = []
                
                for filepath in glob.glob("data/*.txt"):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if exact_search.lower() in content.lower():
                            found_files.append((filepath, content))
                
                if found_files:
                    st.success(f"📁 Найдено файлов: {len(found_files)}")
                    for filepath, content in found_files:
                        filename = os.path.basename(filepath)
                        with st.expander(f"📄 {filename}"):
                            st.text(content[:500] + "..." if len(content) > 500 else content)
                else:
                    st.info("🤷‍♀️ По точному запросу ничего не найдено")
                    
            except Exception as e:
                st.error(f"❌ Ошибка поиска: {e}")

# Статус системы в футере
st.sidebar.markdown("---")
st.sidebar.info(f"🔄 Последнее обновление: {datetime.now().strftime('%H:%M:%S')}")

# Информация о системе
with st.sidebar.expander("ℹ️ О системе"):
    st.write("""
    **ИИ-Ассистент команды** v1.0
    
    Используемые технологии:
    - GigaChat API для генерации ответов
    - ChromaDB для векторного поиска
    - SentenceTransformers для эмбеддингов
    - Streamlit для веб-интерфейса
    
    📊 Статус: {"✅ База знаний", "✅ Веб-интерфейс", "✅ API-аутентификация"}
    """)

# Запускаем приложение
if __name__ == "__main__":
    # Эта строка не нужна для Streamlit, но оставляем для совместимости
    pass

