import streamlit as st
st.title("🎯 Тест интерфейса")
st.write("Боковая панель:")
with st.sidebar:
    st.write("Это боковая панель!")
    st.button("Кнопка")
st.write("Основная область работает!")
