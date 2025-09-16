print("Проверка Python...")
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("✅ HuggingFaceEmbeddings - OK")
except ImportError as e:
    print(f"❌ HuggingFaceEmbeddings: {e}")

try:
    import streamlit
    print("✅ Streamlit - OK")
except ImportError as e:
    print(f"❌ Streamlit: {e}")

print("Проверка завершена")
