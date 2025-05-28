# app.py

import streamlit as st
import google.generativeai as genai

# ================================
# 📌 기본 설정 및 초기화
# ================================

# 🧠 Gemini API 키 설정 (Streamlit Secrets 또는 환경변수로 관리 권장)
GENAI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else "YOUR_API_KEY_HERE"

# 모델 초기화
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Streamlit 페이지 설정
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬")

# ================================
# 🗃️ 대화 세션 상태 관리
# ================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================================
# 🎨 제목 및 설명 표시
# ================================
st.title("💬 Gemini Chatbot Framework")
st.markdown("A simple chatbot template using **Gemini-1.5-Pro** and **Streamlit**. Extend this base to build custom AI assistants.")

# ================================
# 🧾 채팅 UI 구현
# ================================
# 대화 내용 표시
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
user_input = st.chat_input("Ask me anything...")

if user_input:
    # 사용자 메시지 저장 및 표시
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini 응답 생성
    try:
        response = model.generate_content(st.session_state.chat_history)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"❗ Error: {str(e)}"

    # Gemini 응답 저장 및 표시
    st.session_state.chat_history.append({"role": "model", "content": bot_reply})
    with st.chat_message("model"):
        st.markdown(bot_reply)

# ================================
# 📘 용어 정리
# ================================
with st.expander("📘 용어 설명"):
    st.markdown("""
    - **Gemini**: Google의 Generative AI 플랫폼. 여기서는 gemini-1.5-pro 모델을 사용.
    - **st.session_state**: Streamlit 내에서 세션 간 상태(메모리)를 유지하는 기능.
    - **st.chat_input / st.chat_message**: 채팅형 UI를 만드는 Streamlit의 기능.
    """)

